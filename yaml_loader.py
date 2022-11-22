from airflow import DAG
import dagfactory

dag_factory = dagfactory.DagFactory("test.yaml")

dag_factory.clean_dags(globals())
dag_factory.generate_dags(globals())