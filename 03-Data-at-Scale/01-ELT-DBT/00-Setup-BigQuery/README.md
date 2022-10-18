# Prerequisites

_Note : this section is specific to the IKEA bootcamp_

This BigQuery setup should not take long, it simply consists in a few verification steps, and a bit of additional setup / interface congiguration so you're ready for your day.

You'll be sharing a GCP project with the other students. The ID of this project is `ingka-data-engineering-dev`.

1. Make sure you're able to open the BigQuery interface of the project by clicking on [this link](https://console.cloud.google.com/bigquery?project=&supportedpurview=project&ws=!1m0). If you're not, go ask for help to a IKEA TA.
  - If you're a IKEA student : you should be added to the `data-engineering-accelerators-group@ingka.ikea.com` Google Group
  - If you're a Le Wagon TA or teacher : you should be added to the `lewagon@googlegroups.com` Google Group
2. Go to the [Service Account section](https://console.cloud.google.com/iam-admin/serviceaccounts?orgonly=true&project=ingka-data-engineering-dev&supportedpurview=organizationId). Find your service account using the Filter
  - If you don't have a dedicated Service Account, ping the IKEA TA
  - If you do have a Service Account, make sure a key was generated for your service account.

<img src='https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W2D1/gcp_service_account_key.png' size=200>

  - If a key was not generated, click on the Service Account, on the Key Section. Then **Add Key > Create new key > JSON**. And give it a simple name like `lewagon-ikea.json`. Save it on your local (say in the downloads folder).

<img src='https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W2D1/gcp_service_account_key_generation.png' size=200>

3. Make sure you transfer this service account key to your virtual machine, in the `~/.gcp_keys` folder
4. Make sure the IAM member associated to your service account has **Editor** rights to BigQuery (meaning you will be able to create datasets and insert data). Go to the [IAM interface](https://console.cloud.google.com/iam-admin/iam?orgonly=true&project=ingka-data-engineering-dev&supportedpurview=organizationId), filter by your service account. And make sure that the role is **Editor**. If not, contact your TA.

<img src='https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W2D1/gcp_iam_role.png' size=200>


# BigQuery interface

The source dataset is in a `public` BQ project which is already created : `bigquery-public-data`, in the `hacker_news` dataset. And you'll be working mostly in the `ingka-data-engineering-dev` project. Let's pin those 2 in the BigQuery interface.

1. Go to the BigQuery interface [here](https://console.cloud.google.com/bigquery?orgonly=true&project=ingka-data-engineering-dev&supportedpurview=organizationId)
2. Click on **ADD DATA > Pin a project > Enter project name** on the left hand side. Do this for 2 projects :
  - `ingka-data-engineering-dev`
  - `bigquery-public-data`. Hit **Pin**
3. Your BigQuery interface should now look like this :

<img src='https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W2D1/bigquery_interface_final.png' size=200>

You're done with the BigQuery setup - let's move on to the DBT setup
