from flask import Flask, render_template
from healing_engine import monitor_and_heal

app = Flask(__name__)

@app.route('/')
def dashboard():
    job_data = monitor_and_heal()
    return render_template('dashboard.html', jobs=job_data)

if __name__ == "__main__":
    app.run(debug=True)