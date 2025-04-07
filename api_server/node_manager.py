from flask import jsonify
from datetime import datetime

# In-memory data stores
nodes = {}  # node_id: {"cpu": int, "last_heartbeat": datetime}
pods = {}   # pod_id: {"cpu": int, "node_id": str}
node_pods = {}  # node_id: list of pod_ids


def register_node(data):
    node_id = data.get('node_id')
    cpu = data.get('cpu')

    if not node_id or cpu is None:
        return jsonify({"error": "node_id and cpu are required"}), 400

    if node_id in nodes:
        return jsonify({"error": f"Node {node_id} already registered"}), 409

    nodes[node_id] = {"cpu": cpu, "last_heartbeat": datetime.utcnow()}
    node_pods[node_id] = []
    return jsonify({"message": f"Node {node_id} registered with {cpu} CPU cores"}), 201


def update_heartbeat(data):
    node_id = data.get('node_id')

    if node_id not in nodes:
        return jsonify({"error": "Node not found"}), 404

    nodes[node_id]['last_heartbeat'] = datetime.utcnow()
    return jsonify({"message": f"Heartbeat received from node {node_id}"}), 200


def get_all_nodes():
    result = []
    for node_id, info in nodes.items():
        result.append({
            "node_id": node_id,
            "cpu": info['cpu'],
            "last_heartbeat": info['last_heartbeat'].isoformat(),
            "running_pods": node_pods[node_id]
        })
    return jsonify(result)


# Export pods and node_pods to be used by other modules
def get_cluster_state():
    return nodes, pods, node_pods

def update_cluster_state(pods_ref, node_pods_ref):
    global pods, node_pods
    pods = pods_ref
    node_pods = node_pods_ref
