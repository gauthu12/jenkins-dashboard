import smtplib
import requests
from config import TEAMS_WEBHOOK_URL, EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER

def send_email(job_name):
    subject = f"[ALERT] Jenkins job '{job_name}' failed after 3 retries"
    body = f"Self-healing failed for job: {job_name}. Manual intervention needed."
    message = f"Subject: {subject}\n\n{body}"

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, message)

def send_teams_msg(job_name):
    msg = {
        "text": f"🚨 Jenkins job **{job_name}** failed after 3 retries. Manual check required."
    }
    requests.post(TEAMS_WEBHOOK_URL, json=msg)