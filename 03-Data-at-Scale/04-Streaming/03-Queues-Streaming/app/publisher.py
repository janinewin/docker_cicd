import argparse
import os
import sys
import random
from scipy import stats
import datetime
import time
from google.cloud import pubsub_v1
import pandas as pd
import time


def publish_data(publisher,topic_path,sensor_name,sensor_center_lines,sensor_standard_deviation):

    reading = stats.truncnorm.rvs(-1,1,loc = sensor_center_lines, scale = sensor_standard_deviation)
    latency = abs(random.gauss(0,0.1))
    time.sleep(latency)
    timeStamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    message = sensor_name+','+str(reading)+ ',' + timeStamp

    publisher.publish(topic_path, data=message.encode('utf-8'))




def run(TOPIC_NAME, PROJECT_ID, INTERVAL = 200):



    sensor_names = ['AtmP','Temp','Airtight','H2OC']
    sensor_center_lines = [989.21,9.45,1216.02,9.64]
    standard_deviation = [8.35,8.42,39.98,4.23]

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID,TOPIC_NAME)



    c=0
    while True:

        for i in range(len(sensor_names)):
            publish_data(publisher,topic_path,sensor_names[i],sensor_center_lines[i],standard_deviation[i])
            c+=1

        if c == 100:
            print("Published 100 Messages")
            c=0


if __name__ == "__main__":

    project_id=os.environ["PROJECT_ID"]
    topic_name = os.environ["TOPIC_NAME"]
    interval = 200
    try:
        run(
        topic_name,
        project_id,
        interval
    	)
    except KeyboardInterrupt:
        print('Interrupted : Stopped Publishing messages')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
