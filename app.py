import requests
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

JENKINS_URL = "http://localhost:8080"
VIEW_NAME = "QA-Jobs"
USER = "admin"
API_TOKEN = "your-api-token"

def get_jobs_from_view(view):
    url = f"{JENKINS_URL}/view/{view}/api/json"
    response = requests.get(url, auth=(USER, API_TOKEN))
    jobs = response.json().get("jobs", [])
    return jobs

def trigger_rebuild(job_url):
    build_url = job_url + "build"
    requests.post(build_url, auth=(USER, API_TOKEN))

@app.route("/api/jobs")
def api_jobs():
    jobs = get_jobs_from_view(VIEW_NAME)
    job_status = []
    for job in jobs:
        job_detail = requests.get(job["url"] + "api/json", auth=(USER, API_TOKEN)).json()
        status = job_detail.get("color")
        if "red" in status:
            trigger_rebuild(job["url"])  # Self-healing: restart failed job
        job_status.append({
            "name": job["name"],
            "url": job["url"],
            "status": status,
            "buildable": job_detail.get("buildable")
        })
    return jsonify(job_status)

@app.route("/api/restart")
def api_restart():
    job_url = request.args.get('url')
    if job_url:
        trigger_rebuild(job_url)
        return jsonify({"status": "success", "message": f"Triggered restart for job: {job_url}"})
    else:
        return jsonify({"status": "error", "message": "Invalid job URL"}), 400

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)
