from flask import Flask, jsonify, render_template
import psutil

app = Flask(__name__)

def get_system_metrix():
    cpu_usage = psutil.cpu_percent(interval=1)
    mem_usage = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')
    net_info = psutil.net_io_counters()

    return {
        'cpu_usage': cpu_usage,
        'memory_total': mem_usage.local,
        'memory_used': mem_usage.used,
        'memory_free': mem_usage.available,
        'disk_total': disk_usage.total,
        'disk_used': disk_usage.used,
        'disk_free': disk_usage.free,
        'net_sent': net_info.bytes_sent,
        'net_recv': net_info.bytes_recv
    }

@app.route('/metrix', methods=["GET"])
def metrics():
    metrix = get_system_metrix()
    return jsonify(metrix)

@app.route('/')
def index():
    metrix = get_system_metrix()
    return render_template('index.html',metrics=metrics)