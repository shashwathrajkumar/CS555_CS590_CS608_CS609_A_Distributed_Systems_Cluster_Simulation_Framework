from flask import jsonify
from node_manager import get_cluster_state

def schedule_pod(data):
    pod_id = data.get('pod_id')
    cpu_needed = data.get('cpu')
    print(f"Trying to schedule pod {pod_id} with {cpu_needed} CPU...")

    if not pod_id or cpu_needed is None:
        return jsonify({"error": "pod_id and cpu are required"}), 400

    nodes, pods, node_pods = get_cluster_state()

    if pod_id in pods:
        return jsonify({"error": f"Pod {pod_id} already exists"}), 409

    # First-Fit Scheduling
    for node_id, info in nodes.items():
        used_cpu = sum(pods[pid]['cpu'] for pid in node_pods[node_id])
        available_cpu = info['cpu'] - used_cpu

        if available_cpu >= cpu_needed:
            pods[pod_id] = {"cpu": cpu_needed, "node_id": node_id}
            node_pods[node_id].append(pod_id)
            return jsonify({"message": f"Pod {pod_id} scheduled on node {node_id}"}), 201

    return jsonify({"error": "Insufficient CPU resources to schedule pod"}), 503


def get_all_pods():
    _, pods, _ = get_cluster_state()
    result = []
    for pod_id, info in pods.items():
        result.append({
            "pod_id": pod_id,
            "cpu": info['cpu'],
            "node_id": info['node_id']
        })
    return jsonify(result)
