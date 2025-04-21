import threading
import time
from datetime import datetime, timedelta
from node_manager import get_cluster_state

HEARTBEAT_TIMEOUT_SECONDS = 15
CHECK_INTERVAL_SECONDS = 5
#main monitro nodes
def monitor_nodes():
    while True:
        time.sleep(CHECK_INTERVAL_SECONDS)
        nodes, pods, node_pods = get_cluster_state()
        now = datetime.utcnow()
        stale_nodes = []

        for node_id, info in nodes.items():
            if (now - info['last_heartbeat']) > timedelta(seconds=HEARTBEAT_TIMEOUT_SECONDS):
                stale_nodes.append(node_id)

        for node_id in stale_nodes:
            print(f"[Monitor] Node {node_id} timed out. Removing node and its pods.")
            # Remove pods from stale node
            for pod_id in node_pods[node_id]:
                del pods[pod_id]
            del node_pods[node_id]
            del nodes[node_id]


def start_heartbeat_monitor():
    thread = threading.Thread(target=monitor_nodes, daemon=True)
    thread.start()
