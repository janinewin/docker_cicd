import os

from airflow.hooks.sqlite_hook import SqliteHook
from airflow.models import DagBag
from airflow.models.taskinstance import TaskInstance
from airflow.utils.state import DagRunState
from airflow.utils.types import DagRunType
from pendulum.datetime import DateTime
from pendulum.tz.timezone import Timezone

from dags import transform

DAG_BAG = os.path.join(os.path.dirname(__file__), "../dags")
os.environ["AIRFLOW_HOME"] = "/opt/airflow"


class TestTransformDag:

    hook = SqliteHook(sqlite_conn_id="sqlite_connection")
    start_date = DateTime(2021, 6, 1, 0, 0, 0, tzinfo=Timezone("UTC"))
    dagbag = DagBag(dag_folder=DAG_BAG, include_examples=False)

    def test_dag_config(self):
        assert self.dagbag.import_errors == {}
        dag = self.dagbag.get_dag(dag_id="transform")
        assert dag.schedule_interval == "@monthly"

        assert dag.catchup is True
        assert dag.default_args == {"depends_on_past": True, "start_date": self.start_date, "end_date": DateTime(2021, 12, 31, 0, 0, 0, tzinfo=Timezone("UTC"))}

    def test_tasks(self):
        dag = self.dagbag.get_dag(dag_id="transform")

        assert list(map(lambda task: task.task_id, dag.tasks)) == ["extract_sensor", "is_month_odd", "filter_long_trips", "filter_expensive_trips"]

    def test_extract_sensor_task(self):
        dag = self.dagbag.get_dag(dag_id="transform")
        task = dag.get_task("extract_sensor")

        assert task.__class__.__name__ == "ExternalTaskSensor"
        assert task.external_dag_id == "extract"
        assert task.allowed_states == ["success"]
        assert task.poke_interval == 10
        assert task.timeout == 60 * 10
        assert list(map(lambda task: task.task_id, task.upstream_list)) == []
        assert list(map(lambda task: task.task_id, task.downstream_list)) == ["is_month_odd"]

    def test_is_month_odd_task(self):
        dag = self.dagbag.get_dag(dag_id="transform")
        task = dag.get_task("is_month_odd")

        assert task.__class__.__name__ == "BranchPythonOperator"
        assert task.python_callable.__name__ == "is_month_odd"

        for month in range(6, 7):
            self.hook.run("DELETE FROM dag_run")
            execution_date = DateTime(2021, month, 1, 0, 0, 0, tzinfo=Timezone("UTC"))

            dagrun = dag.create_dagrun(
                state=DagRunState.RUNNING,
                execution_date=execution_date,
                start_date=self.start_date,
                run_type=DagRunType.MANUAL,
                data_interval=(execution_date, self.start_date),
            )

            ti = TaskInstance(task, run_id=dagrun.run_id)
            ti.dry_run()

            assert ti.task.op_kwargs == {"date": f"20210{month}01"}

        assert list(map(lambda task: task.task_id, task.upstream_list)) == ["extract_sensor"]
        downstream_list = list(map(lambda task: task.task_id, task.downstream_list))
        assert len(downstream_list) == 2
        assert "filter_long_trips" in downstream_list
        assert "filter_expensive_trips" in downstream_list

    def test_filter_long_trips_task(self):
        dag = self.dagbag.get_dag(dag_id="transform")
        task = dag.get_task("filter_long_trips")

        assert task.__class__.__name__ == "PythonOperator"
        assert task.python_callable.__name__ == "filter_long_trips"

        for month in range(6, 7):
            self.hook.run("DELETE FROM dag_run")
            execution_date = DateTime(2021, month, 1, 0, 0, 0, tzinfo=Timezone("UTC"))

            dagrun = dag.create_dagrun(
                state=DagRunState.RUNNING,
                execution_date=execution_date,
                start_date=self.start_date,
                run_type=DagRunType.MANUAL,
                data_interval=(execution_date, self.start_date),
            )

            ti = TaskInstance(task, run_id=dagrun.run_id)
            ti.dry_run()

            assert ti.task.op_kwargs == {
                "input_file": f"/opt/airflow/data/bronze/yellow_tripdata_2021-0{month}.parquet",
                "output_file": f"/opt/airflow/data/silver/yellow_tripdata_2021-0{month}.parquet",
                "distance": 100,
            }

        assert list(map(lambda task: task.task_id, task.upstream_list)) == ["is_month_odd"]
        assert list(map(lambda task: task.task_id, task.downstream_list)) == []

    def test_filter_expensive_trips_task(self):
        dag = self.dagbag.get_dag(dag_id="transform")
        task = dag.get_task("filter_expensive_trips")

        assert task.__class__.__name__ == "PythonOperator"
        assert task.python_callable.__name__ == "filter_expensive_trips"

        for month in range(6, 7):
            self.hook.run("DELETE FROM dag_run")
            execution_date = DateTime(2021, month, 1, 0, 0, 0, tzinfo=Timezone("UTC"))

            dagrun = dag.create_dagrun(
                state=DagRunState.RUNNING,
                execution_date=execution_date,
                start_date=self.start_date,
                run_type=DagRunType.MANUAL,
                data_interval=(execution_date, self.start_date),
            )

            ti = TaskInstance(task, run_id=dagrun.run_id)
            ti.dry_run()

            assert ti.task.op_kwargs == {
                "input_file": f"/opt/airflow/data/bronze/yellow_tripdata_2021-0{month}.parquet",
                "output_file": f"/opt/airflow/data/silver/yellow_tripdata_2021-0{month}.parquet",
                "amount": 500,
            }

        assert list(map(lambda task: task.task_id, task.upstream_list)) == ["is_month_odd"]
        assert list(map(lambda task: task.task_id, task.downstream_list)) == []


def remove_temp_file(temp_file):
    if os.path.isfile(temp_file):
        os.remove(temp_file)


def assert_dataframe_has_all_values(df):
    assert list(df.columns.values) == ["trip_distance", "total_amount"]
    assert list(df["trip_distance"].values) == [1, 2]
    assert list(df["total_amount"].values) == [3, 4]


def assert_dataframe_has_second_values(df):
    assert list(df.columns.values) == ["trip_distance", "total_amount"]
    assert list(df["trip_distance"].values) == [2]
    assert list(df["total_amount"].values) == [4]


def assert_dataframe_has_no_values(df):
    assert list(df.columns.values) == ["trip_distance", "total_amount"]
    assert list(df["trip_distance"].values) == []
    assert list(df["total_amount"].values) == []


def test_is_month_odd():
    assert transform.is_month_odd("20220801") == "filter_long_trips"
    assert transform.is_month_odd("20220802") == "filter_expensive_trips"


def test_read_parquet_file():
    df = transform.read_parquet_file("tests/data/dataframe.parquet")
    assert_dataframe_has_all_values(df)


def test_get_trips_longer_than():
    df = transform.read_parquet_file("tests/data/dataframe.parquet")

    longer_than_0_df = transform.get_trips_longer_than(df, 0)
    assert_dataframe_has_all_values(longer_than_0_df)

    longer_than_1_df = transform.get_trips_longer_than(df, 1)
    assert_dataframe_has_second_values(longer_than_1_df)

    longer_than_2_df = transform.get_trips_longer_than(df, 2)
    assert_dataframe_has_no_values(longer_than_2_df)


def test_get_trips_more_expensive_than():
    df = transform.read_parquet_file("tests/data/dataframe.parquet")
    df = transform.get_trips_more_expensive_than(df, 2)

    more_expensive_than_2_df = transform.get_trips_more_expensive_than(df, 2)
    assert_dataframe_has_all_values(more_expensive_than_2_df)

    more_expensive_than_3_df = transform.get_trips_more_expensive_than(df, 3)
    assert_dataframe_has_second_values(more_expensive_than_3_df)

    more_expensive_than_4_df = transform.get_trips_more_expensive_than(df, 4)
    assert_dataframe_has_no_values(more_expensive_than_4_df)


def test_save_dataframe_to_parquet():
    temp_file = "tests/temp/dataframe.parquet"
    if os.path.isfile(temp_file):
        os.remove(temp_file)

    df = transform.read_parquet_file("tests/data/dataframe.parquet")
    transform.save_dataframe_to_parquet(df, temp_file)
    saved_df = transform.read_parquet_file(temp_file)
    assert_dataframe_has_all_values(saved_df)


def test_filter_long_trips():
    temp_file = "tests/temp/dataframe.parquet"

    remove_temp_file(temp_file)
    transform.filter_long_trips("tests/data/dataframe.parquet", temp_file, 0)
    df = transform.read_parquet_file(temp_file)
    assert_dataframe_has_all_values(df)

    remove_temp_file(temp_file)
    transform.filter_long_trips("tests/data/dataframe.parquet", temp_file, 1)
    df = transform.read_parquet_file(temp_file)
    assert_dataframe_has_second_values(df)

    remove_temp_file(temp_file)
    transform.filter_long_trips("tests/data/dataframe.parquet", temp_file, 2)
    df = transform.read_parquet_file(temp_file)
    assert_dataframe_has_no_values(df)


def test_filter_expensive_trips():
    temp_file = "tests/temp/dataframe.parquet"

    remove_temp_file(temp_file)
    transform.filter_expensive_trips("tests/data/dataframe.parquet", temp_file, 2)
    df = transform.read_parquet_file(temp_file)
    assert_dataframe_has_all_values(df)

    remove_temp_file(temp_file)
    transform.filter_expensive_trips("tests/data/dataframe.parquet", temp_file, 3)
    df = transform.read_parquet_file(temp_file)
    assert_dataframe_has_second_values(df)

    remove_temp_file(temp_file)
    transform.filter_expensive_trips("tests/data/dataframe.parquet", temp_file, 4)
    df = transform.read_parquet_file(temp_file)
    assert_dataframe_has_no_values(df)
