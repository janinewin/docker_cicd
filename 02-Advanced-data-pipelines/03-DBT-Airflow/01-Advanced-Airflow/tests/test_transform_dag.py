import os.path

from airflow.models import DagBag
from dags import transform
from pendulum.datetime import DateTime
from pendulum.tz.timezone import Timezone


DAG_BAG = os.path.join(os.path.dirname(__file__), "../dags")
AIRFLOW_HOME = os.getenv('AIRFLOW_HOME')
SUFFIX_FOR_TRIP_DATA_FILES = "yellow_tripdata_{{ execution_date.strftime(\'%Y-%m\') }}.parquet"


class TestTransformDag:

    input_file = f"{AIRFLOW_HOME}/data/bronze/{SUFFIX_FOR_TRIP_DATA_FILES}"
    output_file = f"{AIRFLOW_HOME}/data/silver/{SUFFIX_FOR_TRIP_DATA_FILES}"
    dagbag = DagBag(dag_folder=DAG_BAG, include_examples=False)

    def test_dag_config(self):
        assert self.dagbag.import_errors == {}
        dag = self.dagbag.get_dag(dag_id='transform')
        assert dag.schedule_interval == '@monthly'

        assert dag.catchup is True
        assert dag.default_args == {
            'depends_on_past': True,
            'start_date': DateTime(2021, 6, 1, 0, 0, 0, tzinfo=Timezone('UTC')),
            'end_date': DateTime(2021, 12, 31, 0, 0, 0, tzinfo=Timezone('UTC'))
        }

    def test_tasks(self):
        dag = self.dagbag.get_dag(dag_id="transform")

        assert list(map(lambda task: task.task_id, dag.tasks)) == [
            'extract_sensor', 'check_if_month_is_odd', 'filter_long_trips',
            'filter_expensive_trips'
        ]

    def test_extract_sensor_task(self):
        dag = self.dagbag.get_dag(dag_id="transform")
        task = dag.get_task('extract_sensor')

        assert task.__class__.__name__ == 'ExternalTaskSensor'
        assert task.external_dag_id == 'extract'
        assert task.allowed_states == ["success"]
        assert task.poke_interval == 10
        assert task.timeout == 60*10
        assert list(map(lambda task: task.task_id, task.upstream_list)) == []
        assert list(
            map(lambda task: task.task_id,
                task.downstream_list)) == ['check_if_month_is_odd']

    def test_check_if_month_is_odd_task(self):
        dag = self.dagbag.get_dag(dag_id="transform")
        task = dag.get_task('check_if_month_is_odd')

        assert task.__class__.__name__ == 'BranchPythonOperator'
        assert task.python_callable.__name__ == 'is_month_odd'
        assert task.op_kwargs == {
            'date': "{{ ds_nodash }}"
        }
        assert list(map(lambda task: task.task_id, task.upstream_list)) == ['extract_sensor']
        downstream_list = list(map(lambda task: task.task_id, task.downstream_list))
        assert len(downstream_list) == 2
        assert 'filter_long_trips' in downstream_list
        assert 'filter_expensive_trips' in downstream_list

    def test_filter_long_trips_task(self):
        dag = self.dagbag.get_dag(dag_id="transform")
        task = dag.get_task('filter_long_trips')

        assert task.__class__.__name__ == 'PythonOperator'
        assert task.python_callable.__name__ == 'filter_long_trips'
        assert task.op_kwargs == {
            'input_file': self.input_file,
            'output_file': self.output_file,
            'distance': 100,
        }
        assert list(map(lambda task: task.task_id, task.upstream_list)) == ['check_if_month_is_odd']
        assert list(
            map(lambda task: task.task_id,
                task.downstream_list)) == []

    def test_filter_expensive_trips_task(self):
        dag = self.dagbag.get_dag(dag_id="transform")
        task = dag.get_task('filter_expensive_trips')

        assert task.__class__.__name__ == 'PythonOperator'
        assert task.python_callable.__name__ == 'filter_expensive_trips'
        assert task.op_kwargs == {
            'input_file': self.input_file,
            'output_file': self.output_file,
            'amount': 500,
        }
        assert list(map(lambda task: task.task_id, task.upstream_list)) == ['check_if_month_is_odd']
        assert list(
            map(lambda task: task.task_id,
                task.downstream_list)) == []


def remove_temp_file(temp_file):
    if os.path.isfile(temp_file):
        os.remove(temp_file)


def assert_dataframe_has_all_values(df):
    assert list(df.columns.values) == ['trip_distance', 'total_amount']
    assert list(df['trip_distance'].values) == [1, 2]
    assert list(df['total_amount'].values) == [3, 4]


def assert_dataframe_has_second_values(df):
    assert list(df.columns.values) == ['trip_distance', 'total_amount']
    assert list(df['trip_distance'].values) == [2]
    assert list(df['total_amount'].values) == [4]


def assert_dataframe_has_no_values(df):
    assert list(df.columns.values) == ['trip_distance', 'total_amount']
    assert list(df['trip_distance'].values) == []
    assert list(df['total_amount'].values) == []


def test_is_month_odd():
    assert transform.is_month_odd('20220801') == "filter_long_trips"
    assert transform.is_month_odd('20220802') == "filter_expensive_trips"


def test_read_parquet_file():
    df = transform.read_parquet_file('tests/data/dataframe.parquet')
    assert_dataframe_has_all_values(df)


def test_get_trips_longer_than():
    df = transform.read_parquet_file('tests/data/dataframe.parquet')

    longer_than_0_df = transform.get_trips_longer_than(df, 0)
    assert_dataframe_has_all_values(longer_than_0_df)

    longer_than_1_df = transform.get_trips_longer_than(df, 1)
    assert_dataframe_has_second_values(longer_than_1_df)

    longer_than_2_df = transform.get_trips_longer_than(df, 2)
    assert_dataframe_has_no_values(longer_than_2_df)


def test_get_trips_more_expensive_than():
    df = transform.read_parquet_file('tests/data/dataframe.parquet')
    df = transform.get_trips_more_expensive_than(df, 2)

    more_expensive_than_2_df = transform.get_trips_more_expensive_than(df, 2)
    assert_dataframe_has_all_values(more_expensive_than_2_df)

    more_expensive_than_3_df = transform.get_trips_more_expensive_than(df, 3)
    assert_dataframe_has_second_values(more_expensive_than_3_df)

    more_expensive_than_4_df = transform.get_trips_more_expensive_than(df, 4)
    assert_dataframe_has_no_values(more_expensive_than_4_df)


def test_save_dataframe_to_parquet():
    temp_file = 'tests/temp/dataframe.parquet'
    if os.path.isfile(temp_file):
        os.remove(temp_file)

    df = transform.read_parquet_file('tests/data/dataframe.parquet')
    transform.save_dataframe_to_parquet(df, temp_file)
    saved_df = transform.read_parquet_file(temp_file)
    assert_dataframe_has_all_values(saved_df)


def test_filter_long_trips():
    temp_file = 'tests/temp/dataframe.parquet'

    remove_temp_file(temp_file)
    transform.filter_long_trips('tests/data/dataframe.parquet', temp_file, 0)
    df = transform.read_parquet_file(temp_file)
    assert_dataframe_has_all_values(df)

    remove_temp_file(temp_file)
    transform.filter_long_trips('tests/data/dataframe.parquet', temp_file, 1)
    df = transform.read_parquet_file(temp_file)
    assert_dataframe_has_second_values(df)

    remove_temp_file(temp_file)
    transform.filter_long_trips('tests/data/dataframe.parquet', temp_file, 2)
    df = transform.read_parquet_file(temp_file)
    assert_dataframe_has_no_values(df)


def test_filter_expensive_trips():
    temp_file = 'tests/temp/dataframe.parquet'

    remove_temp_file(temp_file)
    transform.filter_expensive_trips('tests/data/dataframe.parquet', temp_file, 2)
    df = transform.read_parquet_file(temp_file)
    assert_dataframe_has_all_values(df)

    remove_temp_file(temp_file)
    transform.filter_expensive_trips('tests/data/dataframe.parquet', temp_file, 3)
    df = transform.read_parquet_file(temp_file)
    assert_dataframe_has_second_values(df)

    remove_temp_file(temp_file)
    transform.filter_expensive_trips('tests/data/dataframe.parquet', temp_file, 4)
    df = transform.read_parquet_file(temp_file)
    assert_dataframe_has_no_values(df)
