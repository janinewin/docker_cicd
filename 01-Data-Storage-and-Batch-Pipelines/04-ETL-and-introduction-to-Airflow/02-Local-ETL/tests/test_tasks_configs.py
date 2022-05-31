import os.path

from airflow.models import DagBag

DAG_BAG = os.path.join(os.path.dirname(__file__), "../dags")

AIRFLOW_HOME = os.getenv('AIRFLOW_HOME')
joke_file = f"{AIRFLOW_HOME}/data/bronze/joke_" + "{{ds_nodash}}.json"
swedified_joke_file = f"{AIRFLOW_HOME}/data/silver/swedified_joke_" + "{{ds_nodash}}.json"


class TestTasksConfigs:

    dagbag = DagBag(dag_folder=DAG_BAG, include_examples=False)

    def test_tasks(self):
        dag = self.dagbag.get_dag(dag_id="local_etl")
        assert list(map(lambda task: task.task_id, dag.tasks)) == [
            'create_swedified_jokes_table', 'extract', 'transform', 'load'
        ]

    def test_create_swedified_jokes_task(self):
        dag = self.dagbag.get_dag(dag_id="local_etl")
        task = dag.get_task('create_swedified_jokes_table')

        assert task.__class__.__name__ == 'PostgresOperator'

        assert task.sql == """CREATE TABLE IF NOT EXISTS swedified_jokes (
                id SERIAL PRIMARY KEY,
                joke VARCHAR NOT NULL,
                swedified_joke VARCHAR NOT NULL
            );"""
        assert task.postgres_conn_id == 'postgres_connection'

        assert list(map(lambda task: task.task_id, task.upstream_list)) == []
        assert list(map(lambda task: task.task_id,
                        task.downstream_list)) == ['extract']

    def test_extract_task(self):
        dag = self.dagbag.get_dag(dag_id="local_etl")
        task = dag.get_task('extract')

        assert task.__class__.__name__ == 'BashOperator'
        data_url = 'https://api.chucknorris.io/jokes/random'
        assert task.bash_command == f'curl {data_url} > {joke_file}'

        assert list(map(lambda task: task.task_id,
                        task.upstream_list)) == ['create_swedified_jokes_table']
        assert list(map(lambda task: task.task_id,
                        task.downstream_list)) == ['transform']

    def test_transform_task(self):
        dag = self.dagbag.get_dag(dag_id="local_etl")
        task = dag.get_task('transform')

        assert task.__class__.__name__ == 'PythonOperator'
        assert task.python_callable.__name__ == 'transform'
        assert task.op_kwargs == {
            'joke_file': joke_file,
            'swedified_joke_file': swedified_joke_file
        }
        assert list(map(lambda task: task.task_id, task.upstream_list)) == ['extract']
        assert list(
            map(lambda task: task.task_id,
                task.downstream_list)) == ['load']

    def test_load_task(self):
        dag = self.dagbag.get_dag(dag_id="local_etl")
        task = dag.get_task('load')

        assert task.__class__.__name__ == 'PythonOperator'
        assert task.python_callable.__name__ == 'load'
        assert list(task.op_kwargs.keys()) == ['swedified_joke_file', 'hook']
        assert task.op_kwargs['swedified_joke_file'] == swedified_joke_file
        assert task.op_kwargs['hook'].__class__.__name__ == 'PostgresHook'
        assert task.op_kwargs['hook'].postgres_conn_id == 'postgres_connection'

        assert list(map(lambda task: task.task_id,
                        task.upstream_list)) == ['transform']
        assert list(map(lambda task: task.task_id, task.downstream_list)) == []
