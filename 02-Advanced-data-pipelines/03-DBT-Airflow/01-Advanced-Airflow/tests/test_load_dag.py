import datetime
import os

import pytest
from airflow import DAG
from airflow.hooks.sqlite_hook import SqliteHook
from airflow.models import DagBag
from airflow.models.taskinstance import TaskInstance
from airflow.operators.python import PythonOperator
from airflow.utils.state import DagRunState
from airflow.utils.types import DagRunType
from dags import load
from pendulum.datetime import DateTime
from pendulum.tz.timezone import Timezone
from testfixtures import log_capture


DAG_BAG = os.path.join(os.path.dirname(__file__), "../dags")
os.environ["AIRFLOW_HOME"] = "/opt/airflow"


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
        hook = SqliteHook(sqlite_conn_id='sqlite_connection')
        start_date = DateTime(2021, 6, 1, 0, 0, 0, tzinfo=Timezone('UTC'))

        assert task.__class__.__name__ == 'PythonOperator'
        assert task.python_callable.__name__ == 'load_to_database'

        for month in range(6, 7):
            hook.run("DELETE FROM dag_run")
            execution_date = DateTime(2021, month, 1, 0, 0, 0, tzinfo=Timezone('UTC'))

            dagrun = dag.create_dagrun(
                state=DagRunState.RUNNING,
                execution_date=execution_date,
                start_date=start_date,
                run_type=DagRunType.MANUAL,
                data_interval=(execution_date, start_date)
            )

            ti = TaskInstance(task, run_id=dagrun.run_id)
            ti.dry_run()
            filtered_data_file = f"/opt/airflow/data/silver/yellow_tripdata_2021-0{month}.parquet"
            assert list(ti.task.op_kwargs.keys()) == ['input_file', 'hook']
            assert ti.task.op_kwargs['input_file'] == filtered_data_file
            assert ti.task.op_kwargs['hook'].__class__.__name__ == 'PostgresHook'
            assert ti.task.op_kwargs['hook'].postgres_conn_id == 'postgres_connection'

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


@pytest.fixture
def dag():
    start_date = DateTime(2021, 6, 1, 0, 0, 0, tzinfo=Timezone('UTC'))
    hook = SqliteHook(sqlite_conn_id='sqlite_connection')

    with DAG(
        dag_id="load",
        schedule_interval="@monthly",
        default_args={"start_date": start_date},
    ) as dag:

        PythonOperator(
            task_id="load_to_database",
            dag=dag,
            python_callable=load.load_to_database,
            op_kwargs=dict(input_file='tests/data/dataframe.parquet', hook=hook)
        )

        PythonOperator(
            task_id="display_number_of_inserted_rows",
            dag=dag,
            python_callable=load.display_number_of_inserted_rows,
        )

    return dag


@log_capture()
def test_display_number_of_inserted_rows(capture, dag):
    now = datetime.datetime.now(datetime.timezone.utc)
    start_date = DateTime(2021, 6, 1, 0, 0, 0, tzinfo=Timezone('UTC'))
    hook = SqliteHook(sqlite_conn_id='sqlite_connection')

    hook.run("DELETE FROM xcom;")

    dagrun = dag.create_dagrun(
        state=DagRunState.RUNNING,
        execution_date=now,
        start_date=start_date,
        run_type=DagRunType.MANUAL,
        data_interval=(now, start_date)
    )

    ti = dagrun.get_task_instance(task_id='display_number_of_inserted_rows')
    ti.task = dag.get_task(task_id='display_number_of_inserted_rows')

    ti_load = dagrun.get_task_instance(task_id='load_to_database')
    ti_load.task = dag.get_task(task_id='load_to_database')

    ti_load.xcom_push('number_of_inserted_rows', 3)
    ti.run(ignore_ti_state=True)
    capture.check_present(
        ('root', 'INFO', '3 trips have been inserted'),
    )


def test_load_to_database(dag):
    now = datetime.datetime.now(datetime.timezone.utc)
    start_date = DateTime(2021, 6, 1, 0, 0, 0, tzinfo=Timezone('UTC'))
    hook = SqliteHook(sqlite_conn_id='sqlite_connection')

    dagrun = dag.create_dagrun(
        state=DagRunState.RUNNING,
        execution_date=now,
        start_date=start_date,
        run_type=DagRunType.MANUAL,
        data_interval=(now, start_date)
    )

    ti = dagrun.get_task_instance(task_id='load_to_database')
    ti.task = dag.get_task(task_id='load_to_database')

    hook.run("DROP TABLE IF EXISTS trips;")
    hook.run("DELETE FROM task_instance;")
    assert ti.xcom_pull(task_ids=['load_to_database'], key='number_of_inserted_rows') == []
    ti.run(ignore_ti_state=True)

    assert hook.get_records("SELECT COUNT(*) FROM trips;")[0][0] == 2
    assert hook.get_records("SELECT trip_distance FROM trips;") == [(1,), (2,)]
    assert hook.get_records("SELECT total_amount FROM trips;") == [(3,), (4,)]
    assert ti.xcom_pull(task_ids=['load_to_database'], key='number_of_inserted_rows') == [2]
