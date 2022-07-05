import os
import pathlib
import yaml
import lewagonde
from google.cloud import bigquery
from google.oauth2 import service_account

dbt_profile_path = lewagonde.DBT_PROFILE_PATH
dbt_full_profile_path = os.path.expanduser(dbt_profile_path)

with open(dbt_full_profile_path) as f:
    profile_dict = yaml.safe_load(f)

dev = profile_dict['dbt_lewagon']['outputs']['dev']
bq_dataset = dev['dataset']
bq_project = dev['project']
bq_credentials_path = dev['keyfile']

credentials = service_account.Credentials.from_service_account_file(
  bq_credentials_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
)
client = bigquery.Client(credentials=credentials, project=credentials.project_id)

def sql_query_table_structure(model, bq_dataset):
    query = f"SELECT column_name \
    FROM `{bq_dataset}`.`INFORMATION_SCHEMA`.`COLUMNS` \
    WHERE table_name = '{model}'"
    return query

def test_first_dbt_model():
    output = client.query(sql_query_table_structure('my_first_dbt_model', bq_dataset))
    df = output.to_dataframe()
    assert len(df) >= 1, "my_first_dbt_model has not been created yet in your dataset"

def test_second_dbt_model():
    output = client.query(sql_query_table_structure('my_second_dbt_model', bq_dataset))
    df = output.to_dataframe()
    assert len(df) >= 1, "my_second_dbt_model has not been created yet in your dataset"
