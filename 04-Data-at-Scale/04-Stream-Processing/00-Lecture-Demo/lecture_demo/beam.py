import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import ReadFromPubSub
from apache_beam import Map
import os

PROJECT_ID = os.getenv("PROJECT_ID")
TOPIC_NAME = os.getenv("TOPIC_NAME")

with beam.Pipeline(options=PipelineOptions(streaming=True)) as pipeline:
    subscription_name = f"projects/{PROJECT_ID}/topics/{TOPIC_NAME}"

    data = (
        pipeline
        | "ReadData" >> ReadFromPubSub(topic=subscription_name)
        | "Decode" >> Map(lambda message: message.decode("utf-8"))
        | "Convert to list" >> Map(lambda message: message.split(" "))
    )

    # windowing = (
    #     data
    #     | "Extract Error Code and Timestamp"
    #     >> Map(
    #         lambda element: (
    #             int(
    #                 time.mktime(
    #                     datetime.strptime(element[0], "%d/%b/%Y:%H:%M:%S").timetuple()
    #                 )
    #             ),  # Unix Timestamp
    #             int(element[-1]),  # HTTP Error Code
    #         )
    #     )
    #     | "Map to TimestampedValue"
    #     >> Map(
    #         lambda element: TimestampedValue(
    #             (
    #                 element[0] // 5 * 5,
    #                 element[1],
    #             ),  # (Timestamp 5 second intervals, Error Code)
    #             element[0],  # Actual timestamp
    #         )
    #     )
    #     | "Windowing" >> beam.WindowInto(FixedWindows(5))
    # )

    # count_per_window = (
    #     windowing
    #     | "AddKey" >> Map(lambda x: (x, 1))
    #     | "GroupBy" >> GroupByKey()
    #     | "SumValues" >> Map(lambda element: (element[0], sum(element[1])))
    #     | "Print"
    #     >> Map(
    #         lambda element: print(
    # f"""
    # Timestamp: {element[0][0]},
    # Error Code: {element[0][1]},
    # Count: {element[1]}"""
    #         )
    #     )
    # )
