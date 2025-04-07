from flask import Flask, request, jsonify
from node_manager import register_node, update_heartbeat, get_all_nodes
from scheduler import schedule_pod, get_all_pods
from health_monitor import start_heartbeat_monitor

app = Flask(__name__)

# Start heartbeat monitoring in the background
start_heartbeat_monitor()

@app.route('/')
def home():
    return jsonify({"message": "Cluster Simulation API is running."})

@app.route('/register_node', methods=['POST'])
def register_node_route():
    data = request.get_json()
    return register_node(data)

@app.route('/launch_pod', methods=['POST'])
def launch_pod_route():
    data = request.get_json()
    print(f"Received pod launch request: {data}")

    return schedule_pod(data)

@app.route('/heartbeat', methods=['POST'])
def heartbeat_route():
    data = request.get_json()
    return update_heartbeat(data)

@app.route('/nodes', methods=['GET'])
def get_nodes_route():
    return get_all_nodes()

@app.route('/pods', methods=['GET'])
def get_pods_route():
    return get_all_pods()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
