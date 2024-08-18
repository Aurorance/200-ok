import prefect
from prefect import flow, task
from prefect.task_runners import SequentialTaskRunner
from prefect.deployments import Deployment
from prefect.client.schemas.schedules import CronSchedule
import subprocess

# Define the tasks that will run your scripts

@task
def run_cellarmasterwines_to_db():
    print("Running cellarmasterwines.py...")
    subprocess.run(["python", "cellarmasterwines.py"], check=True)

@task
def run_historical():
    print("Running historical.py...")
    subprocess.run(["python", "historical.py"], check=True)

@task
def run_historical_upload():
    print("Running historical_upload.py...")
    subprocess.run(["python", "historical_upload.py"], check=True)

# Define the flow with tasks in the desired order
@flow(name="monthly-script-run", task_runner=SequentialTaskRunner())
def my_monthly_flow():
    # The tasks will run in the order they are listed
    run_cellarmasterwines_to_db()
    run_historical()
    run_historical_upload()

# Define a schedule to run every 3 minutes
cron_schedule = CronSchedule(
    cron="*/3 * * * *",  # Every 3 minutes
    timezone="Asia/Singapore"  # UTC+8 timezone
)

# Create and apply a deployment with the schedule
deployment = Deployment.build_from_flow(
    flow=my_monthly_flow,
    name="test-script-run-every-3-minutes",
    schedule=cron_schedule,
    work_queue_name="default"
)

if __name__ == "__main__":
    # Apply the deployment to Prefect Orion (or Prefect Cloud)
    deployment.apply()

    # Optionally run the flow immediately for testing
    print("Running flow for testing...")