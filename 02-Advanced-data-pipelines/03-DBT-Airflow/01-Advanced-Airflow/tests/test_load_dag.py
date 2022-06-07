import datetime
import os.path

from airflow import DAG
from airflow.hooks.sqlite_hook import SqliteHook
from airflow.models import DagBag
from airflow.operators.python import PythonOperator
from airflow.utils.state import DagRunState
from airflow.utils.types import DagRunType
from dags import load
from pendulum.datetime import DateTime
from pendulum.tz.timezone import Timezone


DAG_BAG = os.path.join(os.path.dirname(__file__), "../dags")
AIRFLOW_HOME = os.getenv('AIRFLOW_HOME')


class TestLoadDag:

    dagbag = DagBag(dag_folder=DAG_BAG, include_examples=False)

    def test_dag_config(self):
        assert self.dagbag.import_errors == {}
        dag = self.dagbag.get_dag(dag_id='load')

        assert dag.schedule_interval == '@monthly'
        assert dag.catchup is True
        assert dag.default_args == {
            'depends_on_past': True,
            'start_date': DateTime(2021, 6, 1, 0, 0, 0, tzinfo=Timezone('UTC')),
            'end_date': DateTime(2021, 12, 31, 0, 0, 0, tzinfo=Timezone('UTC'))
        }

    def test_tasks(self):
        dag = self.dagbag.get_dag(dag_id="load")

        assert list(map(lambda task: task.task_id, dag.tasks)) == [
            'transform_sensor', 'load_to_database', 'display_number_of_inserted_rows'
        ]

    def test_transform_sensor_task(self):
        dag = self.dagbag.get_dag(dag_id="load")
        task = dag.get_task('transform_sensor')

        assert task.__class__.__name__ == 'ExternalTaskSensor'
        assert task.external_dag_id == 'transform'
        assert task.allowed_states == ["success"]
        assert task.poke_interval == 10
        assert task.timeout == 60*10
        assert list(map(lambda task: task.task_id, task.upstream_list)) == []
        assert list(
            map(lambda task: task.task_id,
                task.downstream_list)) == ['load_to_database']

    def test_load_to_database_task(self):
        dag = self.dagbag.get_dag(dag_id="load")
        task = dag.get_task('load_to_database')

        assert task.__class__.__name__ == 'PythonOperator'
        assert task.python_callable.__name__ == 'load_to_database'

        filtered_data_file = f"{AIRFLOW_HOME}/data/silver/yellow_tripdata_" + "{{ execution_date.strftime(\'%Y-%m\') }}.parquet"
        assert list(task.op_kwargs.keys()) == ['input_file', 'hook']
        assert task.op_kwargs['input_file'] == filtered_data_file
        assert task.op_kwargs['hook'].__class__.__name__ == 'PostgresHook'
        assert task.op_kwargs['hook'].postgres_conn_id == 'postgres_connection'

        assert list(map(lambda task: task.task_id, task.upstream_list)) == ['transform_sensor']
        assert list(
            map(lambda task: task.task_id,
                task.downstream_list)) == ['display_number_of_inserted_rows']

    def test_display_number_of_inserted_rows_task(self):
        dag = self.dagbag.get_dag(dag_id="load")
        task = dag.get_task('display_number_of_inserted_rows')

        assert task.__class__.__name__ == 'PythonOperator'
        assert task.python_callable.__name__ == 'display_number_of_inserted_rows'

        assert list(map(lambda task: task.task_id, task.upstream_list)) == ['load_to_database']
        assert list(
            map(lambda task: task.task_id,
                task.downstream_list)) == []


def test_display_number_of_inserted_rows():
    pass


def test_load_to_database():
    now = datetime.datetime.now(datetime.timezone.utc)
    start_date = DateTime(2021, 6, 1, 0, 0, 0, tzinfo=Timezone('UTC'))

    with DAG(
        dag_id="load",
        schedule_interval="@monthly",
        default_args={"start_date": start_date},
    ) as dag:

        hook = SqliteHook(sqlite_conn_id='sqlite_connection')
        PythonOperator(
            task_id="load_to_database",
            dag=dag,
            python_callable=load.load_to_database,
            op_kwargs=dict(input_file='tests/data/dataframe.parquet', hook=hook)
        )

        dagrun = dag.create_dagrun(
            state=DagRunState.RUNNING,
            execution_date=now,
            start_date=start_date,
            run_type=DagRunType.MANUAL,
        )

        ti = dagrun.get_task_instance(task_id='load_to_database')
        ti.task = dag.get_task(task_id='load_to_database')
        connection = hook.get_conn()
        cursor = connection.cursor()

        hook.run(sql="DROP TABLE IF EXISTS trips;")
        assert ti.xcom_pull(task_ids=['load_to_database'], key='number_of_inserted_rows') == []
        ti.run(ignore_ti_state=True)

        assert cursor.execute("SELECT COUNT(*) FROM trips;").fetchall()[0][0] == 2
        assert cursor.execute("SELECT trip_distance FROM trips;").fetchall() == [(1,), (2,)]
        assert cursor.execute("SELECT total_amount FROM trips;").fetchall() == [(3,), (4,)]
        assert ti.xcom_pull(task_ids=['load_to_database'], key='number_of_inserted_rows') == [2]
