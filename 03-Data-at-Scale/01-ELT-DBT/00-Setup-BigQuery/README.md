# BigQuery interface

The source dataset is in a `public` BQ project which is already created : `bigquery-public-data`, in the `hacker_news` dataset. And you'll be working mostly in the `ingka-data-engineering-dev` project. Let's pin those 2 in the BigQuery interface.

1. Go to the BigQuery interface [here](https://console.cloud.google.com/bigquery?orgonly=true&project=ingka-data-engineering-dev&supportedpurview=organizationId)
2. Click on **ADD DATA > Pin a project > Enter project name** on the left hand side. Do this for 2 projects :
  - `ingka-data-engineering-dev`
  - `bigquery-public-data`. Hit **Pin**
3. Your BigQuery interface should now look like this :

<img src='https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W2D1/bigquery_interface_final.png' size=200>

You're done with the BigQuery setup - let's move on to the DBT setup
