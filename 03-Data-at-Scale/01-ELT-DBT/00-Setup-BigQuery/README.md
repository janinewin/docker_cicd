# BigQuery interface

BigQuery enables you to query data stored in different locations / projects. In this exercice, we'll be interacting with 2 projects :
- The project where the source data is stored. It's a project made public by Google to enable Data Scientists to play around with data. The project is called `bigquery-public-data`, and the name of the dataset is `hacker_news`
- Your own project, that you created during the Data Engineering Setup.

Let's pin those 2 in the BigQuery interface.

1. Go to the BigQuery interface [here](https://console.cloud.google.com/bigquery)
2. Star the `bigquery-public-data` project so you can more easily interact with it :
  - Click on **ADD DATA > Star a project by name**, type : `bigquery-public-data`. Hit **STAR**
3. Do the same thing with your own project : in the example / screenshot below, the "personal" project is called `ingka-data-engineering-dev`
4. Your BigQuery interface should now look like this (except that instead of `ingka-data-engineering-dev`, it will be your project name):

<img src='https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W2D1/bigquery_interface_final.png' size=200>

You're done with the BigQuery setup - let's move on to the DBT setup
