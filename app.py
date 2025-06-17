import psutil
import shutil
from flask import Flask, render_template

app = Flask(__name__)

def get_disk_usage():
    usage = shutil.disk_usage("/")
    percent = (usage.used / usage.total) * 100
    return round(percent, 2)

@app.route("/")
def index():
    cpu_percent = psutil.cpu_percent()
    mem_percent = psutil.virtual_memory().percent
    disk_percent = get_disk_usage()

    message = None
    if cpu_percent > 80 or mem_percent > 80 or disk_percent > 80:
        message = "High CPU, memory, or disk utilization detected!"

    return render_template(
        "index.html",
        cpu_percent=cpu_percent,
        mem_percent=mem_percent,
        disk_percent=disk_percent,
        message=message
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)