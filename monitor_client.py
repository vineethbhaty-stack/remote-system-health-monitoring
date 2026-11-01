import socket
import json
import time
import psutil

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000
SEND_INTERVAL = 3


def collect_health_data():
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    network = psutil.net_io_counters()

    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "ram_percent": memory.percent,
        "disk_percent": disk.percent,
        "uptime_seconds": int(time.time() - psutil.boot_time()),
        "process_count": len(psutil.pids()),
        "network_sent_bytes": network.bytes_sent,
        "network_received_bytes": network.bytes_recv,
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

            print("\nHealth report sent!")
            print(f"CPU: {data['cpu_percent']}%")
            print(f"RAM: {data['ram_percent']}%")
            print(f"Disk: {data['disk_percent']}%")
            print(f"Processes: {data['process_count']}")

            time.sleep(SEND_INTERVAL)

    except KeyboardInterrupt:
        print("\nClient stopped.")

    except OSError as error:
        print(f"Network error: {error}")

    finally:
        client.close()


if __name__ == "__main__":
    start_client()
