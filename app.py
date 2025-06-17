import psutil
import shutil
import smtplib
from flask import Flask, render_template
from email.message import EmailMessage

app = Flask(__name__)

def get_disk_usage():
    usage = shutil.disk_usage("/")
    percent = (usage.used / usage.total) * 100
    return round(percent, 2)

def send_email_alert(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = "devisysadm@gmail.com"
    msg['To'] = "devisingh447@gmail.com"

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login("devisysadm@gmail.com", "YOUR_APP_PASSWORD")  # use App Password
            smtp.send_message(msg)
            print("Email alert sent!")
    except Exception as e:
        print(f"Failed to send email: {e}")

@app.route("/")
def index():
    cpu_percent = psutil.cpu_percent()
    mem_percent = psutil.virtual_memory().percent
    disk_percent = get_disk_usage()

    message = None
    if cpu_percent > 80 or mem_percent > 80 or disk_percent > 80:
        message = "High CPU, memory, or disk utilization detected!"
        alert_msg = f"CPU: {cpu_percent}%\nMemory: {mem_percent}%\nDisk: {disk_percent}%"
        send_email_alert("System Alert: Resource Usage High", alert_msg)

    return render_template(
        "index.html",
        cpu_percent=cpu_percent,
        mem_percent=mem_percent,
        disk_percent=disk_percent,
        message=message
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
