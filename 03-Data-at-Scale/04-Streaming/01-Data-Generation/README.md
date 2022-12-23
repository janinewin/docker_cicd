## Objectives
This challenge aim to group data from different IoT with a fix frequency

How -> Beam
Paradigm of Map Group Time Window
Put a schema to explain Map into time key -> Group and reduce by mean

Explain structure of code with different pipeline

## Download the data
put the data in data/sensors_latency.csv

## Read the data with Beam
Go to beam_sample.py
Go to pipeline data and use `ReadFromText` and split data into list

## Save Data to an outputFile
head to out pipeline and use WriteToText

execute python app/beam_sample.py

## Let's map data Now and create a TimeValue key
head to the class MapSessionNoWindow
code the process by giving a
* key: value where the key is a rounded value of the timestamp
* value: sensor name and sensor value

modify pipeline windowing
hint : don't forget beam.ParDo to map the process within MapSessionNoWindow

## Let's reduce the data
First we need to group the data
apply a parDo function that put the data into dataframe and group by data by key (cf exo 1)

## (Bonus) Time Window Session
modify pipeline windowing
create beam.window.TimestampedValue
apply beam.WindowInto
apply a MapSessionWindow by getting the window end time within the function process of the class
