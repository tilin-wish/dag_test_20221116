from airflow import DAG
import os
import dagfactory
_cur_path = os.path.dirname(os.path.abspath(__file__))

from dagfactory import load_yaml_dags

files = os.listdir(os.path.join(_cur_path,"yaml"))
for file in files:
    dagfactory.DagFactory(os.path.join(_cur_path, "yaml", file)).generate_dags(globals())