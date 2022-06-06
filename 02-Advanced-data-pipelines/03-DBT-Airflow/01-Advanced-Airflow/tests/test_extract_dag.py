import os.path

from airflow.models import DagBag
from pendulum.datetime import DateTime
from pendulum.tz.timezone import Timezone

DAG_BAG = os.path.join(os.path.dirname(__file__), "../dags")
AIRFLOW_HOME = os.getenv('AIRFLOW_HOME')


class TestExtractDag:

    dagbag = DagBag(dag_folder=DAG_BAG, include_examples=False)

    def test_dag_config(self):
        assert self.dagbag.import_errors == {}
        dag = self.dagbag.get_dag(dag_id='extract')
        assert dag.schedule_interval == '@monthly'
        assert dag.catchup is True
        assert dag.default_args == {
            'depends_on_past': True,
            'start_date': DateTime(2021, 6, 1, 0, 0, 0, tzinfo=Timezone('UTC')),
            'end_date': DateTime(2021, 12, 31, 0, 0, 0, tzinfo=Timezone('UTC'))
        }

    def test_extract_tasks(self):
        dag = self.dagbag.get_dag(dag_id="extract")
        assert list(map(lambda task: task.task_id, dag.tasks)) == [
            'get_parquet_data',
        ]

    def test_get_parquet_data_task(self):
        dag = self.dagbag.get_dag(dag_id="extract")
        task = dag.get_task('get_parquet_data')

        assert task.__class__.__name__ == 'BashOperator'
        url = "https://nyc-tlc.s3.amazonaws.com/trip+data/yellow_tripdata_{{ execution_date.strftime(\'%Y-%m\') }}.parquet"
        file_path = f"{AIRFLOW_HOME}/data/bronze/yellow_tripdata_" + "{{ execution_date.strftime(\'%Y-%m\') }}.parquet"
        assert task.bash_command == f'curl {url} > {file_path}'
