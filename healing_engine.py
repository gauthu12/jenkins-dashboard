from jenkins_utils import get_jobs_from_view, get_job_status, restart_job
from config import JENKINS_VIEWS
from notifier import send_email, send_teams_msg

retry_counter = {}

def monitor_and_heal():
    result = []
    for view in JENKINS_VIEWS:
        jobs = get_jobs_from_view(view)
        for job in jobs:
            job_name = job['name']
            status_data = get_job_status(job_name)
            status = status_data['status']
            timestamp = status_data['timestamp']

            if status != "SUCCESS":
                retries = retry_counter.get(job_name, 0)
                if retries < 3:
                    restart_job(job_name)
                    retry_counter[job_name] = retries + 1
                else:
                    send_email(job_name)
                    send_teams_msg(job_name)
                    retry_counter[job_name] = 0

            result.append({
                "job": job_name,
                "view": view,
                "status": status,
                "retries": retry_counter.get(job_name, 0),
                "timestamp": timestamp
            })
    return result