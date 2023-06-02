from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.sensors.http_sensor import HttpSensor

default_args = {"owner": "tilin", "start_date": "2023-04-24"}

with DAG(
    "http_sensor_dag", default_args=default_args, schedule_interval="@daily"
) as dag:
    http_sensor_task = HttpSensor(
        task_id="http_sensor",
        http_conn_id="your_http_connection",
        endpoint="wishflow.wishpost.bjs.i.wish.com/api/experimental/dags/wishpost_payment_dump_daily/dag_runs/2023-06-01/tasks/DumpPurchaseData",
        response_check=lambda response: response.json().get("state") == "success",
        poke_interval=60,  # 每60秒执行一次HTTP请求
        timeout=120,  # 超时时间为120秒
    )
