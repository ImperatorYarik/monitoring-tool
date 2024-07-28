from flask import Flask, jsonify, render_template
import psutil
import socket

app = Flask(__name__)


def bytes_to_megabytes(bytes):
    return int(bytes / (1024 * 1024))

def bytes_to_gigabytes(bytes):
    return int(bytes / (1024 * 1024 * 1024))

def get_system_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    mem_usage = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')
    net_info = psutil.net_io_counters()
    hostname = socket.gethostname()
    return {
        'hostname': hostname,
        'cpu_usage': cpu_usage,
        'memory_total': bytes_to_megabytes(mem_usage.total),
        'memory_used': bytes_to_megabytes(mem_usage.used),
        'memory_free': bytes_to_megabytes(mem_usage.available),
        'disk_total': bytes_to_gigabytes(disk_usage.total),
        'disk_used': bytes_to_gigabytes(disk_usage.used),
        'disk_free': bytes_to_gigabytes(disk_usage.free),
        'net_sent': bytes_to_gigabytes(net_info.bytes_sent),
        'net_recv': bytes_to_gigabytes(net_info.bytes_recv)
    }

@app.route('/metrix', methods=["GET"])
def metrics():
    metrix = get_system_metrics()
    return jsonify(metrix)

@app.route('/')
def index():
    metrics = get_system_metrics()
    return render_template('index.html', metrics=metrics)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)