import requests
import time
import os
import uuid
import argparse

# --- Parse command-line arguments ---
parser = argparse.ArgumentParser(description="Simulate a cluster node.")
parser.add_argument('--cpu', type=int, default=4, help='Number of CPU cores (default: 4)')
parser.add_argument('--api-server', type=str, default="http://localhost:5000", help='API server URL')
args = parser.parse_args()

# --- Configuration ---
API_SERVER = args.api_server
NODE_ID = os.getenv("NODE_ID", f"node-{uuid.uuid4().hex[:6]}")
CPU_CORES = args.cpu

REGISTER_ENDPOINT = f"{API_SERVER}/register_node"
HEARTBEAT_ENDPOINT = f"{API_SERVER}/heartbeat"

def register_node():
    try:
        response = requests.post(REGISTER_ENDPOINT, json={
            "node_id": NODE_ID,
            "cpu": CPU_CORES
        })
        print(f"[Register] Status {response.status_code}: {response.json()}")
    except Exception as e:
        print(f"[Register] Error: {e}")

def send_heartbeat():
    try:
        response = requests.post(HEARTBEAT_ENDPOINT, json={
            "node_id": NODE_ID
        })
        print(f"[Heartbeat] Status {response.status_code}: {response.json()}")
    except Exception as e:
        print(f"[Heartbeat] Error: {e}")

if __name__ == "__main__":
    print(f"[Init] Starting node {NODE_ID} with {CPU_CORES} CPU cores, targeting {API_SERVER}")
    register_node()

    while True:
        send_heartbeat()
        time.sleep(5)
