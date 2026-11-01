import socket
import json
import time
import os
import shutil

SERVER_HOST = "10.0.0.2"
SERVER_PORT = 5000
SEND_INTERVAL = 3


def cpu_usage():
    def read_cpu():
        with open("/proc/stat") as f:
            values = list(map(int, f.readline().split()[1:]))
        return sum(values), values[3] + values[4]

    a, idle_a = read_cpu()
    time.sleep(0.2)
    b, idle_b = read_cpu()

    total = b - a
    idle = idle_b - idle_a
    return round((total - idle) * 100 / total, 2) if total else 0


def collect_health_data():
    memory = {}

    with open("/proc/meminfo") as f:
        for line in f:
            key, value = line.split(":", 1)
            memory[key] = int(value.strip().split()[0])

    ram = round(
        (1 - memory["MemAvailable"] / memory["MemTotal"]) * 100, 2
    )

    disk = shutil.disk_usage("/")
    disk_percent = round(disk.used * 100 / disk.total, 2)

    with open("/proc/uptime") as f:
        uptime = int(float(f.read().split()[0]))

    processes = len([
        x for x in os.listdir("/proc") if x.isdigit()
    ])

    sent = 0
    received = 0

    with open("/proc/net/dev") as f:
        for line in f.readlines()[2:]:
            values = line.split(":")[1].split()
            received += int(values[0])
            sent += int(values[8])

    return {
        "cpu_percent": cpu_usage(),
        "ram_percent": ram,
        "disk_percent": disk_percent,
        "uptime_seconds": uptime,
        "process_count": processes,
        "network_sent_bytes": sent,
        "network_received_bytes": received,
        "status": "online"
    }


def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("REMOTE SYSTEM HEALTH MONITORING CLIENT")
    print("Protocol: UDP")
    print(f"Server: {SERVER_HOST}:{SERVER_PORT}")

    try:
        while True:
            data = collect_health_data()
            message = json.dumps(data).encode("utf-8")
            client.sendto(message, (SERVER_HOST, SERVER_PORT))

            print("Health report sent!")
            print("CPU:", data["cpu_percent"], "%")
            print("RAM:", data["ram_percent"], "%")
            print("Disk:", data["disk_percent"], "%")
            print("Processes:", data["process_count"])

            time.sleep(SEND_INTERVAL)

    except KeyboardInterrupt:
        print("Client stopped.")

    finally:
        client.close()


if __name__ == "__main__":
    start_client()
