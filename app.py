from flask import Flask, jsonify, render_template
import speedtest
import psutil
import socket
import requests
import platform
import os

app = Flask(__name__)

# Function to gather system information
def gather_system_info():
    try:
        # Speed test
        download_speed, upload_speed = run_speedtest()

        # System stats
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        total_memory = memory_info.total / (1024 ** 3)
        available_memory = memory_info.available / (1024 ** 3)
        used_memory = memory_info.used / (1024 ** 3)
        memory_percentage = memory_info.percent

        # Network info
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        public_ip = requests.get('https://ipinfo.io/ip').text.strip()
        fqdn = socket.getfqdn()

        # Platform info
        system = platform.system()
        release = platform.release()
        version = platform.version()
        machine = platform.machine()
        processor = platform.processor()
        python_version = platform.python_version()
        node = platform.node()

        # Construct data
        return {
            "speed_info": {
                "download_speed": f"{download_speed:.2f} Mbps",
                "upload_speed": f"{upload_speed:.2f} Mbps",
            },
            "cpu_usage": f"{cpu_usage}%",
            "memory_info": {
                "total_memory": f"{total_memory:.2f} GB",
                "available_memory": f"{available_memory:.2f} GB",
                "used_memory": f"{used_memory:.2f} GB",
                "memory_percentage": f"{memory_percentage}%",
            },
            "network_info": {
                "hostname": hostname,
                "local_ip": local_ip,
                "public_ip": public_ip,
                "fqdn": fqdn,
            },
            "platform_info": {
                "system": system,
                "release": release,
                "version": version,
                "machine": machine,
                "processor": processor,
                "python_version": python_version,
                "node": node,
            },
        }
    except Exception as e:
        print(f"Error gathering system info: {str(e)}")
        return {"error": str(e)}

@app.route('/')
def index():
    # Gather system info and pass to the template
    data = gather_system_info()
    return render_template("index.html", data=data)

@app.route('/speedtest')
def speedtest_results():
    # Provide speed test results as JSON
    data = gather_system_info()
    return jsonify(data)

def run_speedtest():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1_000_000  
        upload_speed = st.upload() / 1_000_000  
        return download_speed, upload_speed
    except Exception as e:
        print(f"Speedtest error: {str(e)}")
        return None, None

if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

