import uuid
from airflow.models.dag import DAG
from datetime import datetime, timedelta
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator
from kubernetes.client import CoreV1Api, models as k8s
from kubernetes.client import V1ResourceRequirements

from airflow.kubernetes.secret import Secret

default_args = {
    'owner': 'tilin',
    'depends_on_past': False,
    'start_date' : datetime(2023, 2, 15),
    'schedule_interval': "45 1 * * *",
    'email': ['tilin@wish.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'catchup': True
}

with DAG(dag_id="dag_mongo_dump99", default_args = default_args) as dag:

    task_01 = BashOperator(bash_command="echo {{ ts_nodash }}")
    task_02 = BashOperator(bash_command="echo {{ ts_nodash }}")

    task_dump = KubernetesPodOperator(namespace='airflow',
        cmds=["python", "/home/app/wishpost/scripts/crons/easy_mongo_etl/easy_mongo2s3.py"],
        arguments=["--date=20221230T000000",
        "--c_name=MerchantOrder",
        "--s3_bucket=wishpost-data",
        "--task_id=MongoDumpMerchantOrderDaily",
        "--s3_uri_prefix=qa/mongo2s3_dump/wishpost/wishpost_merchant_order",
        "--env=be_qa",
        "--secrets_file=/opt/vault/secrets/dev_wishpost_secrets.conf",
        "--freq=daily"],
        get_logs=True,
        pod_template_file="/opt/airflow/dags/repo/pod_template_files/wishpost_template.yaml",
        env_vars={"DB_SECRETS_FILE":"/opt/vault/secrets/db_credentials"},
        secrets=[Secret('volume', '/opt/vault/secrets', 'wishflow-wishpost-credential')],
        )

    task_final = BashOperator(bash_command="echo {{ ts_nodash }}")

    [task_01, task_02] >> task_dump >> task_final

    
    
