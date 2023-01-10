import argparse
import datetime
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import apache_beam.transforms.window as window
import pandas as pd
from apache_beam.io import fileio
import os
from apache_beam.transforms.trigger import AfterProcessingTime,AccumulationMode,Repeatedly,AfterWatermark
from apache_beam.transforms import trigger

def str2timestamp(str_datetime, fmt='%Y-%m-%d %H:%M:%S.%f'):
    """Converts a datetime string into a unix timestamp(number of seconds 1/1/1970 00:00:00)"""
    dt = datetime.datetime.strptime(str_datetime, fmt)
    epoch = datetime.datetime.utcfromtimestamp(0)
    return int((dt - epoch).total_seconds())


def strtime_window_rounded(str_datetime,window=15,fmt='%Y-%m-%d %H:%M:%S.%f'):
    """
    Converts a datetime to rounded datetime with a frequency window in sec
    """
    timestamp = str2timestamp(str_datetime,fmt)
    timestamp_rounded = (timestamp//window+1)*window
    datetime_rounded = datetime.datetime.utcfromtimestamp(timestamp_rounded)
    return datetime_rounded.strftime(fmt)

#$DELETE_BEGIN
class MapSessionWindow(beam.DoFn):
    """Prints per session information"""
    def process(self, element, window=beam.DoFn.WindowParam):
        yield window.end.to_utc_datetime().strftime("%Y-%m-%d %H:%M:%S"),[element[0],float(element[1])]
#$DELETE_END

def aggregate_sensors(timestamp,sensor_values):
    """
    function to return agreggated values by mean within a dictionnary with one value for each sensor
    and the timestamp of the aggregation
    """
    #$CHALLENGIFY_START
    df = pd.DataFrame(sensor_values)
    df.columns = ["Sensor","Value"]
    df["Timestamp"] = timestamp
    df['Value'] = df['Value'].astype('float32')

    df_agg =  df.pivot_table(index="Timestamp",columns="Sensor",values='Value',aggfunc="mean")
    df_agg.reset_index(inplace=True) #reset_index to include Timestamp as a columns

    dict_agg_data = df_agg.iloc[0].to_dict() #only one row is left after aggregation
    #dict_agg_data = df_agg.to_dict(orient='records')[0] #this is equivalent to the previous line

    return dict_agg_data
    #$CHALLENGIFY_END

class interpolateSensors(beam.DoFn):
    def process(self,sensorValues):

        (timestamp, values) =  sensorValues
        df = pd.DataFrame(values)
        df.columns = ["Sensor","Value","raw"]

        json_string =  df.groupby(["Sensor"]).mean().T.iloc[0]
        json_string["Timestamp"] = timestamp
        yield json_string.to_dict()


def run(subscription_name, output_table, interval=15.0, pipeline_args=None):
    schema = 'Timestamp:TIMESTAMP, AtmP:FLOAT, Temp:FLOAT,  Airtight:FLOAT, H2OC:FLOAT'
    with beam.Pipeline(options=PipelineOptions(pipeline_args, streaming=True,
                        save_main_session=True)) as pipeline:

        # pipeline steps to pull the data from pub/sub
        data = (

            pipeline
            #$CHALLENGIFY_BEGIN
            | 'ReadData' >> beam.io.ReadFromPubSub(subscription=subscription_name)
            | "Decode" >> beam.Map(lambda message: message.decode('utf-8'))
            | "Convert to list" >> beam.Map(lambda message: message.split(","))
            #$CHALLENGIFY_END
        )



        # pipeline steps to window the data
        windowing = (
             data
             #$CHALLENGIFY_BEGIN
                | "Attach time" >> beam.Map(
                    lambda element: beam.window.TimestampedValue(element,
                                                str2timestamp(element[2])))
                | "Map Time Rounded Key per Element" >> beam.Map(lambda element: (
                                strtime_window_rounded(element[2]),
                                [element[0], element[1]]))
                | "Time Window of interval secs" >> beam.WindowInto(
                  window.FixedWindows(interval)
                 )
             #$CHALLENGIFY_END
        )

        #$DELETE_BEGIN
        #
        #BONUS Beam Window
        # windowing = (
        #     data
        #     | "to timestamp Values" >> beam.Map(
        #         lambda element: beam.window.TimestampedValue([element[0], float(element[1])],
        #                                                      str2timestamp(element[2])))
        #     | "Time Window of interval secs with trigger" >> beam.WindowInto(
        #         window.FixedWindows(interval),
        #         trigger=Repeatedly(AfterProcessingTime(1 * 15)),
        #         allowed_lateness=1800,
        #         accumulation_mode=AccumulationMode.DISCARDING
        #         )
        #     | "Map Session" >> beam.ParDo(MapSessionWindow())
        # )
        #
        #$DELETE_END

        # pipeline steps to group and aggregate the data
        group = (
            windowing
            # #$CHALLENGIFY_BEGIN
            | "Group" >> beam.GroupByKey()
            | "Average Over Time" >> beam.MapTuple(aggregate_sensors)
            #$CHALLENGIFY_END
        )

        group | "Print debug" >> beam.Map(lambda x: print(x))


        # pipeline steps to write to big query
        out_bq = (
            group
            # #$CHALLENGIFY_BEGIN
            | "Write to Big Query" >> beam.io.gcp.bigquery.WriteToBigQuery(output_table,schema=schema,
                    write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
            #$CHALLENGIFY_END
        )

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--id', dest='project')
    parser.add_argument('--subscription-name', dest='subscription_name')
    parser.add_argument('--interval', dest='agg_interval', default=15)
    parser.add_argument('--output-table',dest='output_table', default=False )

    args, pipeline_args = parser.parse_known_args()

    subscription_name=''
    #$CHALLENGIFY_BEGIN
    subscription_name = f"projects/{args.project}/subscriptions/{args.subscription_name}"
    #$CHALLENGIFY_END

    run(
        subscription_name,
        args.output_table,
        args.agg_interval,
        pipeline_args
      )
