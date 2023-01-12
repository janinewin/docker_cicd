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



def aggregate_sensors(timestamp,sensor_values):
    """
    function to return agreggated values by mean within a dictionnary with one value for each sensor
    and the timestamp of the aggregation
    """
    # $CHALLENGIFY_START
    df = pd.DataFrame(sensor_values)
    df.columns = ["Sensor","Value"]
    df["Timestamp"] = timestamp
    df['Value'] = df['Value'].astype('float32')

    df_agg =  df.pivot_table(index="Timestamp",columns="Sensor",values='Value',aggfunc="mean")
    df_agg.reset_index(inplace=True) #reset_index to include Timestamp as a columns

    dict_agg_data = df_agg.iloc[0].to_dict() #only one row is left after aggregation
    #dict_agg_data = df_agg.to_dict(orient='records')[0] #this is equivalent to the previous line

    return dict_agg_data
    # $CHALLENGIFY_END

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
            pass  # YOUR CODE HERE
        )



        # pipeline steps to window the data
        windowing = (
             data
             pass  # YOUR CODE HERE
        )

        

        # pipeline steps to group and aggregate the data
        group = (
            windowing
            # pass  # YOUR CODE HERE
        )

        group | "Print debug" >> beam.Map(lambda x: print(x))


        # pipeline steps to write to big query
        out_bq = (
            group
            # pass  # YOUR CODE HERE
        )

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--id', dest='project')
    parser.add_argument('--subscription-name', dest='subscription_name')
    parser.add_argument('--interval', dest='agg_interval', default=15)
    parser.add_argument('--output-table',dest='output_table', default=False )

    args, pipeline_args = parser.parse_known_args()

    subscription_name=''
    pass  # YOUR CODE HERE

    run(
        subscription_name,
        args.output_table,
        args.agg_interval,
        pipeline_args
      )
