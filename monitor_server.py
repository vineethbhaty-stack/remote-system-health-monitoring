import socket
import json
from datetime import datetime

HOST = "0.0.0.0"
PORT = 5000

CPU_THRESHOLD = 80
RAM_THRESHOLD = 80


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((HOST, PORT))

    print("REMOTE SYSTEM HEALTH MONITORING")
    print("Protocol: UDP")
    print(f"Server listening on port {PORT}")
    print("Waiting for health reports...")

    try:
        while True:
            packet, address = server.recvfrom(65535)

            try:
                data = json.loads(packet.decode("utf-8"))

                print("\n" + "-" * 40)
                print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
                print(f"Client: {address[0]}:{address[1]}")
                print(f"CPU Usage: {data.get('cpu_percent', 'N/A')}%")
                print(f"RAM Usage: {data.get('ram_percent', 'N/A')}%")
                print(f"Disk Usage: {data.get('disk_percent', 'N/A')}%")
                print(f"Uptime: {data.get('uptime_seconds', 'N/A')} seconds")
                print(f"Processes: {data.get('process_count', 'N/A')}")
                print(f"Network sent: {data.get('network_sent_bytes', 'N/A')} bytes")
                print(f"Network received: {data.get('network_received_bytes', 'N/A')} bytes")

                if data.get("cpu_percent", 0) >= CPU_THRESHOLD:
                    print("ALERT: HIGH CPU USAGE")

                if data.get("ram_percent", 0) >= RAM_THRESHOLD:
                    print("ALERT: HIGH RAM USAGE")

                print("-" * 40)

            except (json.JSONDecodeError, UnicodeDecodeError):
                print(f"Invalid report received from {address}")

    except KeyboardInterrupt:
        print("\nServer stopped.")

    finally:
        server.close()


if __name__ == "__main__":
    start_server()
