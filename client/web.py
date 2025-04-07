from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
API_URL = "http://localhost:5000"  # Update if API server runs elsewhere

@app.route('/')
def index():
    try:
        nodes = requests.get(f"{API_URL}/nodes").json()
        pods = requests.get(f"{API_URL}/pods").json()
    except Exception as e:
        return f"Error connecting to API server: {e}", 500

    return render_template("index.html", nodes=nodes, pods=pods)

@app.route('/launch_pod', methods=['POST'])
def launch_pod():
    pod_id = request.form['pod_id']
    cpu = int(request.form['cpu'])

    response = requests.post(f"{API_URL}/launch_pod", json={"pod_id": pod_id, "cpu": cpu})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=8000)
