import os.path

from airflow.models import DagBag

DAG_BAG = os.path.join(os.path.dirname(__file__), "../dags")

AIRFLOW_HOME = os.getenv('AIRFLOW_HOME')


class TestTasksConfigs:

    dagbag = DagBag(dag_folder=DAG_BAG, include_examples=False)

    def test_tasks(self):
        dag = self.dagbag.get_dag(dag_id="long_track")
        assert list(map(lambda task: task.task_id, dag.tasks)) == [
            'create_comments_table', 'get_and_insert_last_comments'
        ]

    def test_create_comments_task(self):
        dag = self.dagbag.get_dag(dag_id="long_track")
        task = dag.get_task('create_comments_table')

        assert task.__class__.__name__ == 'PostgresOperator'

        assert task.sql == """CREATE TABLE IF NOT EXISTS comments (
                id SERIAL PRIMARY KEY,
                movie_id INTEGER NOT NULL,
                comment VARCHAR NOT NULL,
                rating INTEGER NOT NULL
            );"""
        assert task.postgres_conn_id == 'postgres_connection'

        assert list(map(lambda task: task.task_id, task.upstream_list)) == []
        assert list(map(lambda task: task.task_id,
                        task.downstream_list)) == ['get_and_insert_last_comments']

    def test_get_and_insert_last_comments_task(self):
        dag = self.dagbag.get_dag(dag_id="long_track")
        task = dag.get_task('get_and_insert_last_comments')

        assert task.__class__.__name__ == 'PythonOperator'
        assert task.python_callable.__name__ == 'get_and_insert_last_comments'
        assert list(task.op_kwargs.keys()) == ['hook']
        assert task.op_kwargs['hook'].__class__.__name__ == 'PostgresHook'
        assert task.op_kwargs['hook'].postgres_conn_id == 'postgres_connection'

        assert list(map(lambda task: task.task_id, task.upstream_list)) == ['create_comments_table']
        assert list(
            map(lambda task: task.task_id,
                task.downstream_list)) == []
