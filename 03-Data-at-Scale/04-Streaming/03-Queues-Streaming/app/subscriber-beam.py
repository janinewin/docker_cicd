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

class MapSessionWindow(beam.DoFn):
    """Prints per session information"""
    def process(self, element, window=beam.DoFn.WindowParam):
        yield window.end.to_utc_datetime().strftime("%Y-%m-%d %H:%M:%S"),[element[0],float(element[1]),element[2]]

class MapSessionWindow2(beam.DoFn):
    """Prints per session information"""
    def process(self, element, window=beam.DoFn.WindowParam):
        yield (window.end.to_utc_datetime().strftime("%Y-%m-%d %H:%M:%S"),element[0]),float(element[1])


class MapDict(beam.DoFn):
    """Prints per session information"""
    def process(self, element):
        key,value = element
        dict_temp = dict(value)
        dict_temp["timestamp"]=key
        yield dict_temp


def roundTime(dt=None, roundTo=1):
    if dt == None : dt = datetime.datetime.now()
    seconds = (dt.replace(tzinfo=None) - dt.min).seconds
    rounding = (seconds+roundTo/2) // roundTo * roundTo
    return str(dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond))

def str2timestamp(s, fmt='%Y-%m-%d %H:%M:%S.%f'):
    """Converts a string into a unix timestamp."""
    dt = datetime.datetime.strptime(s, fmt)
    epoch = datetime.datetime.utcfromtimestamp(0)
    return int((dt - epoch).total_seconds())

def strtime_window_rounded(s,window=15,fmt='%Y-%m-%d %H:%M:%S.%f'):
    timestamp = str2timestamp(s)
    timestamp_rounded = (timestamp//window+1)*window
    datetime_rounded = datetime.datetime.utcfromtimestamp(timestamp_rounded)
    return datetime_rounded.strftime(fmt)

def aggregate_sensors(timestamp,sensor_values):
    df = pd.DataFrame(sensor_values)
    df.columns = ["Sensor","Value","raw"]
    df["Timestamp"] = timestamp
    df['Value'] = df['Value'].astype('float32')

    df_agg =  df.pivot_table(index="Timestamp",columns="Sensor",values='Value',aggfunc="mean")
    df_agg.reset_index(inplace=True) #reset_index to include Timestamp as a columns

    dict_agg_data = df_agg.iloc[0].to_dict() #only one row is left after aggregation
    #dict_agg_data = df_agg.to_dict(orient='records')[0] #this is equivalent to the previous line

    #$CHALLENGIFY_END
    return dict_agg_data

class interpolateSensors(beam.DoFn):
    def process(self,sensorValues):

        (timestamp, values) =  sensorValues
        df = pd.DataFrame(values)
        df.columns = ["Sensor","Value","raw"]

        json_string =  df.groupby(["Sensor"]).mean().T.iloc[0]
        json_string["Timestamp"] = timestamp
        yield json_string.to_dict()

def isMissing(jsonData):
    return len(jsonData.values()) == 5

def run(subscription_name, output_table, interval=1.0, pipeline_args=None):
    schema = 'Timestamp:TIMESTAMP, AtmP:FLOAT, Temp:FLOAT,  Airtight:FLOAT, H2OC:FLOAT'

    with beam.Pipeline(options=PipelineOptions( pipeline_args, streaming=True, save_main_session=True)) as p:

        data = (
            p
            | 'ReadData' >>
            beam.io.ReadFromPubSub(subscription=subscription_name,)
            | "Decode" >> beam.Map(lambda x: x.decode('utf-8'))
            | "Convert to list" >> beam.Map(lambda x: x.split(","))
        )
        #data | 'Print in Terminal data' >> beam.Map(lambda x: print(x))

        # windowing = (
        #      data
        #      |"Map Session" >> beam.Map(
        #          lambda element: (strtime_window_rounded(element[2])
        #                           , [element[0], float(element[1]),element[2]]
        #                           )
        #          )
        #      | "Window to 15 secs" >> beam.WindowInto(
        #           window.FixedWindows(interval),
        #           trigger=Repeatedly(AfterProcessingTime(2*interval)),
        #           allowed_lateness=15,
        #           accumulation_mode=AccumulationMode.ACCUMULATING)
        #      )

        windowing = (
            data
            | "to timestamp Values" >> beam.Map(
                lambda x: beam.window.TimestampedValue(x, str2timestamp(x[2])))
            | "Window to 15 secs" >> beam.WindowInto(
                window.FixedWindows(interval),
                trigger=Repeatedly(AfterProcessingTime(2*interval)),
                allowed_lateness=15,
                accumulation_mode=AccumulationMode.DISCARDING)
            | "Map Session" >> beam.ParDo(MapSessionWindow())
        )
        #windowing | 'Print in Terminal' >> beam.Map(lambda x: print(x))

        group = (
            windowing
            | "Group" >> beam.GroupByKey()
            # | "Mean" >> beam.combiners.Mean.PerKey()
            # | "Average Over Time" >> beam.MapTuple(lambda key,mean: (key[0],[key[1],mean]))
            # | "Group" >> beam.GroupByKey()
            # | "Dict" >> beam.ParDo(MapDict())
            | "Average Over Time" >> beam.MapTuple(lambda time,values: aggregate_sensors(time,values))
        )

        group | "Print" >> beam.Map(lambda x: print(x))

        out = (
            group
            | "Write to Big Query" >> beam.io.WriteToBigQuery(output_table,schema=schema, write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
        )

if __name__ == "__main__":


    #subscription_name = f"projects/{os.environ['PROJECT_ID']}/subscriptions/{os.environ['SUBSCRIPTION_NAME']}"
    #output_table = os.environ["BQ_TABLE"]
    #agg_interval = 15

    parser = argparse.ArgumentParser()
    parser.add_argument('--id', dest='project')
    parser.add_argument('--subscription-name', dest='subscription_name')
    parser.add_argument('--interval', dest='agg_interval', default=15)
    parser.add_argument('--output-table',dest='output_table', default=False )

    args, pipeline_args = parser.parse_known_args()
    print(pipeline_args)
    subscription_name = f"projects/{args.project}/subscriptions/{args.subscription_name}"

    run(
        subscription_name,
        args.output_table,
        args.agg_interval,
        pipeline_args
      )
