import uuid
from airflow.models.dag import DAG
from datetime import datetime, timedelta
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.operators.dummy import DummyOperator
from kubernetes.client import CoreV1Api, models as k8s
from kubernetes.client import V1ResourceRequirements

from airflow.kubernetes.secret import Secret

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date' : datetime(2023, 2, 5),
    'schedule_interval': "45 1 * * *",
    'email': ['tilin@wish.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'catchup': True,
    'retry_delay': timedelta(minutes=5)
}
dag = DAG(
    'plain_kube20', default_args=default_args)

start = DummyOperator(task_id='start', dag=dag)

simple_kube_task = KubernetesPodOperator(namespace='airflow',
                          image="python:3.6",
                          cmds=["python","-c"],
                          arguments=["print('hello world')"],
                          labels={"foo": "bar"},
                          name="simple-kube-test",
                          task_id="simple-kube-task",
                          get_logs=True,
                          is_delete_operator_pod=True,
                          #volume_mounts=[],
                          env_vars={"DB_SECRETS_FILE":"/opt/vault/secrets/db_credentials"},
                          resources=V1ResourceRequirements(
                            requests={
                                "cpu": 1,
                                'memory': '100Mi'
                            },
                            limits={
                                "cpu": 2,
                                'memory': '200Mi',
                            }),
                          dag=dag
                          )

job_name = "k8s-job"
meta_name = 'k8s-pod-' + uuid.uuid4().hex
metadata = k8s.V1ObjectMeta(name=(meta_name))
full_pod_spec = k8s.V1Pod(
    metadata=metadata,
  )

wishpost_task_test = KubernetesPodOperator(namespace='airflow',
                          #image="harbor.infra.wish-cn.com/wish/wishpost@sha256:d9f0eea2fee8634636f0534d7e03d078be22070480ae71b3060c0be562de6db5",
                          image="harbor.infra.wish-cn.com/wish/wishpost-airflow@sha256:803f50dd630ad4e4d8fb218297ecf9fe05b53bcf8195ffb77377cf0744e42355",
                          #image="harbor.infra.wish-cn.com/wish/wishpost-airflow:bff81de-20221226031202_MKL-68756",
                          #cmds=["python", "/home/app/wishpost/scripts/crons/easy_mongo_etl/easy_mongo2s3.py"],
                          cmds=["python", "-c", "import time;time.sleep(300)"],
                          #arguments=["/home/app/wishpost/scripts/test/heavy_memory_test.py"],
                          #arguments=["import time;time.sleep(300);"],
                        #   arguments=["--date=20221130T000000",
                        #    "--c_name=MerchantOrder",
                        #    "--s3_bucket=wishpost-data",
                        #     "--task_id=MongoDumpMerchantOrderDaily",
                        #     "--s3_uri_prefix=tahoe/wishpost/wishpost_merchant_order",
                        #     "--env=be_qa",
                        #     "--freq=daily"],
                          #labels={"ttt": "eee"},
                          name=job_name,
                          task_id=job_name,
                          full_pod_spec=full_pod_spec,
                          #task_id="mongo_dump-task",
                          get_logs=True,
                          pod_template_file="/opt/airflow/dags/repo/pod_template_files/wishpost_template.yaml",
                          is_delete_operator_pod=False,
                          env_vars={"DB_SECRETS_FILE":"/opt/vault/secrets/db_credentials"},
                          #volume_mounts=[k8s.V1VolumeMount(mount_path="/opt/vault/secrets", name="credential")],
                          secrets=[Secret('volume', '/opt/vault/secrets', 'wishflow-wishpost-credential')],
                          dag=dag
                          )

end = DummyOperator(task_id='end', dag=dag)

simple_kube_task.set_upstream(start)
wishpost_task_test.set_upstream(start)
simple_kube_task.set_downstream(end)
wishpost_task_test.set_downstream(end)