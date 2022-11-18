from airflow.models.dag import DAG
from datetime import datetime, timedelta
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.operators.dummy import DummyOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date' : datetime(2022, 11, 15),
    'schedule_interval': "45 1 * * *",
    'email': ['tilin@wish.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'catchup': False,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'test_air_3', default_args=default_args)

start = DummyOperator(task_id='start', dag=dag)

passing = KubernetesPodOperator(namespace='airflow',
                          image="python:3.6",
                          cmds=["python","-c"],
                          arguments=["print('hello world')"],
                          labels={"foo": "bar"},
                          name="passing-test",
                          task_id="passing-task",
                          get_logs=True,
                          is_delete_operator_pod=False,
                          dag=dag
                          )

wishpost_task_test = KubernetesPodOperator(namespace='airflow',
                          image="harbor.infra.wish-cn.com/wish/wishpost@sha256:d9f0eea2fee8634636f0534d7e03d078be22070480ae71b3060c0be562de6db5",
                          #image="harbor.infra.wish-cn.com/wish/wishpost_payment_pipeline/base@sha256:ed9ee4780189e89c10715327ffe6e6cde7864afe4c35cf412000e7a261619644",
                          cmds=["python"],
                          arguments=["/home/app/wishpost/scripts/test/heavy_memory_test.py"],
                          labels={"foo": "bar"},
                          name="null-test",
                          task_id="wishpost-task-arg",
                          get_logs=True,
                          is_delete_operator_pod=True,
                          dag=dag
                          )

end = DummyOperator(task_id='end', dag=dag)

#passing.set_upstream(start)
wishpost_task_test.set_upstream(start)
#passing.set_downstream(end)
wishpost_task_test.set_downstream(end)