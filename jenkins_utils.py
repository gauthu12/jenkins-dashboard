import requests
from requests.auth import HTTPBasicAuth
from config import JENKINS_URL, JENKINS_USER, JENKINS_API_TOKEN

def get_jobs_from_view(view_name):
    url = f"{JENKINS_URL}/view/{view_name}/api/json"
    res = requests.get(url, auth=HTTPBasicAuth(JENKINS_USER, JENKINS_API_TOKEN))
    return res.json().get("jobs", [])

def get_job_status(job_name):
    url = f"{JENKINS_URL}/job/{job_name}/lastBuild/api/json"
    res = requests.get(url, auth=HTTPBasicAuth(JENKINS_USER, JENKINS_API_TOKEN))
    data = res.json()
    return {
        "status": data["result"],
        "timestamp": data["timestamp"]
    }

def restart_job(job_name):
    url = f"{JENKINS_URL}/job/{job_name}/build"
    res = requests.post(url, auth=HTTPBasicAuth(JENKINS_USER, JENKINS_API_TOKEN))
    return res.status_code == 201