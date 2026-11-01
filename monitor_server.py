import socket
import json
import time
from datetime import datetime

HOST = "0.0.0.0"
PORT = 5000

CPU_THRESHOLD = 80
RAM_THRESHOLD = 80

OFFLINE_TIMEOUT = 10

def start_server():

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((HOST, PORT))

    # Check for incoming packets every second
    server.settimeout(1)

    # Store the last report time of each client
    clients = {}

    # Track clients already marked offline
    offline_clients = set()

    print("REMOTE SYSTEM HEALTH MONITORING")
    print("Protocol: UDP")
    print(f"Server listening on port {PORT}")
    print("Waiting for health reports...")

    try:
        while True:

            try:
                packet, address = server.recvfrom(65535)

                data = json.loads(packet.decode("utf-8"))

                client_ip = address[0]
                current_time = time.time()

                # Check whether this client is new or has returned
                if client_ip not in clients:
                    print(f"\nCLIENT ONLINE: {client_ip}")

                elif client_ip in offline_clients:
                    print(f"\nCLIENT BACK ONLINE: {client_ip}")
                    offline_clients.remove(client_ip)

                # Update last received report time
                clients[client_ip] = current_time

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

                # CPU threshold alert
                if data.get("cpu_percent", 0) >= CPU_THRESHOLD:
                    print("ALERT: HIGH CPU USAGE")

                # RAM threshold alert
                if data.get("ram_percent", 0) >= RAM_THRESHOLD:
                    print("ALERT: HIGH RAM USAGE")

                print("-" * 40)

            except socket.timeout:

                # Check whether any client has stopped sending reports
                current_time = time.time()

                for client_ip, last_seen in clients.items():

                    if current_time - last_seen > OFFLINE_TIMEOUT:

                        if client_ip not in offline_clients:
                            print(f"\nALERT: CLIENT OFFLINE - {client_ip}")
                            offline_clients.add(client_ip)

            except (json.JSONDecodeError, UnicodeDecodeError):
                print(f"Invalid report received from {address}")

    except KeyboardInterrupt:
        print("\nServer stopped.")

    finally:
        server.close()


if __name__ == "__main__":
    start_server()

               
