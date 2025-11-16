# dags/postgres_migration_dag.py

from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 8, 9),
    "retries": 1,
}

with DAG(
    dag_id="postgres_migration_pipeline",
    default_args=default_args,
    description="Backup SQLite → Migrate → Verify in Postgres",
    schedule_interval=None,  # Run manually or set cron
    catchup=False,
) as dag:

    # Step 1: Backup SQLite
    backup_sqlite = BashOperator(
        task_id="backup_sqlite",
        bash_command="python /opt/airflow/scripts/backup.py",
    )

    # Step 2: Run migration
    migrate_to_postgres = BashOperator(
        task_id="migrate_to_postgres",
        bash_command="python /opt/airflow/scripts/migrate.py",
    )

    # Step 3: Verify migration
    verify_migration = BashOperator(
        task_id="verify_migration",
        bash_command="python /opt/airflow/scripts/verify_migration.py",
    )

    # DAG sequence
    backup_sqlite >> migrate_to_postgres >> verify_migration
