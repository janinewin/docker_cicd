import argparse
import datetime
import apache_beam as beam
import apache_beam.transforms.window as window
import pandas as pd
from apache_beam.io import ReadFromText,WriteToText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.runners.interactive import interactive_beam as ib
import os
from apache_beam.runners.interactive.display.pipeline_graph import PipelineGraph

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

#$DELETE_BEGIN
#DoFn implementation of aggregate_sensors
class AggregateSensors(beam.DoFn):
    def process(self,sensorValues):

        dict_agg_data={}
        (timestamp, values) =  sensorValues

        df = pd.DataFrame(values)
        df.columns = ["Sensor","Value"]
        df["Timestamp"] = timestamp
        df['Value'] = df['Value'].astype('float32')

        df_agg =  df.pivot_table(index="Timestamp",columns="Sensor",values='Value',aggfunc="mean")
        df_agg.reset_index(inplace=True) #reset_index to include Timestamp as a columns

        dict_agg_data = df_agg.iloc[0].to_dict() #only one row is left after aggregation
        #dict_agg_data = df_agg.to_dict(orient='records')[0] #this is equivalent to the previous line

        yield dict_agg_data
#$DELETE_END

def run(file_path,output_fps_prefix,interval=15,bool_output_bq=False, pipeline_args=None):

    schema = 'Timestamp:TIMESTAMP, AtmP:FLOAT, Temp:FLOAT, Airtight:FLOAT, H2OC:FLOAT'
    with beam.Pipeline(options=PipelineOptions(pipeline_args)) as pipeline:

        # data section
        data = (
            pipeline
            #$CHALLENGIFY_BEGIN
            | 'ReadData' >> ReadFromText(file_path,skip_header_lines=1)
            | "Convert to list" >>beam.Map(lambda x: x.split(","))
            #$CHALLENGIFY_END
        )

        #$DELETE_BEGIN
        # FOR DEBUGING IN TERMINAL
        #data | 'Print in Terminal' >> beam.Map(lambda x: print(x))
        #
        #$DELETE_END


        windowing = (
            data
            #$CHALLENGIFY_BEGIN
            | "Map Time Rounded Key per Element" >> beam.Map(
                lambda element:
                        (strtime_window_rounded(element[2], interval),
                        [element[0],float(element[1])])
                    )
            #$CHALLENGIFY_END
        )

        #$DELETE_BEGIN
        #
        #BONUS Beam Window
        # windowing=(
        #    data
        #    | "to timestamp Values" >> beam.Map(lambda x: beam.window.TimestampedValue(x,str2timestamp(x[2])))
        #    | "Window to 15 secs" >> beam.WindowInto(window.FixedWindows(interval))
        #    | "Map Session" >> beam.ParDo(MapSessionWindow())
        # )
        #
        #$DELETE_END

        grouping = (
            windowing
            #$CHALLENGIFY_BEGIN
            | "Group By Key" >> beam.GroupByKey()
            | "Average within interval" >> beam.MapTuple(lambda time,values: aggregate_sensors(time,values))
            #$CHALLENGIFY_END
            #$DELETE_BEGIN
            #| "Average within interval" >>beam.ParDo(AggregateSensors()) #Alternation with ParDo
            #$DELETE_END
        )

        out = (
            grouping
            #$CHALLENGIFY_BEGIN
            | "Write to CSV" >> WriteToText(output_fps_prefix)
            #$CHALLENGIFY_END
        )


        if bool_output_bq :

            output_bq_table = os.environ.get("BQ_TABLE","")
            output_gcs_temp = os.environ.get("GCS_TEMP","")

            out_bq = (
                 grouping
                 #$CHALLENGIFY_BEGIN
                 | "Write to Big Query" >> beam.io.gcp.bigquery.WriteToBigQuery(output_bq_table,
                                                                                schema=schema,
                                                                                write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                                                                                custom_gcs_temp_location=output_gcs_temp)
                #$CHALLENGIFY_END
             )



if __name__ == "__main__":



    parser = argparse.ArgumentParser()

    parser.add_argument('--input', dest='file_path', default='data/sensors_latency.csv')
    parser.add_argument('--output', dest='output_prefix', default='data/output.txt')
    parser.add_argument('--interval', dest='agg_interval', default=15)
    parser.add_argument('--out-bq',dest='bool_out_bq', default=False )

    args, pipeline_args = parser.parse_known_args()


    run(file_path=args.file_path,
        output_fps_prefix=args.output_prefix,
        interval=args.agg_interval,
        bool_output_bq=args.bool_out_bq,
        pipeline_args = pipeline_args)
