from airflow import DAG
import os
import dagfactory
_cur_path = os.path.dirname(os.path.abspath(__file__))
print(_cur_path)
dag_factory = dagfactory.DagFactory(os.path.join(_cur_path,"dag_mongo_dump.yaml"))

#dag_factory.clean_dags(globals())
#dag_factory.generate_dags(globals())

# dag_factory2 = dagfactory.DagFactory(os.path.join(_cur_path,"yaml_loader_kube_example.yaml"))

# dag_factory2.clean_dags(globals())
# dag_factory2.generate_dags(globals())
# from dagfactory import load_yaml_dags

# load_yaml_dags(globals_dict=globals(), suffix=['.yaml'])