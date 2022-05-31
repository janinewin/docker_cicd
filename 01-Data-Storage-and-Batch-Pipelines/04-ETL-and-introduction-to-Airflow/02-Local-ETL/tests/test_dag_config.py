import os.path

from airflow.models import DagBag
from airflow.utils.dates import days_ago

DAG_BAG = os.path.join(os.path.dirname(__file__), "../dags")


class TestDagConfig:

    dagbag = DagBag(dag_folder=DAG_BAG, include_examples=False)

    def test_dag_config(self):
        assert self.dagbag.import_errors == {}
        dag = self.dagbag.get_dag(dag_id="local_etl")
        assert dag.schedule_interval == '@daily'
        assert dag.default_args == {
            'depends_on_past': True,
            'start_date': days_ago(5)
        }
        assert self.dagbag.import_errors == {}
