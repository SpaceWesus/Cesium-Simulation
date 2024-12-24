# Server
#### Step 1: Setting Up Python Flask Server with WebSockets

# Prerequisites:
# Make sure you have Python installed (Python 3.8 or later is recommended).
# 1. Open a terminal or command prompt.
# 2. Create a virtual environment (optional but recommended):
#    python -m venv env
#    source env/bin/activate (Linux/MacOS)
#    .\env\Scripts\activate (Windows)
# 3. Install required packages:
#    pip install flask flask-socketio eventlet

# Code:
from flask import Flask, render_template
from flask_socketio import SocketIO
import random
import time
import threading

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'  # Replace 'secret!' with a more secure key
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Serve basic HTML template for testing (this will be replaced with Cesium later)
@app.route('/')
def index():
    return "Server is running! Ready for simulation."  # Basic message to test if server is live

# Sample Data for Pedestrian and Vehicle Movement
agents = {
    'pedestrians': [],
    'vehicles': []
}

# Generate Random Agents
def initialize_agents():
    # Create 10 pedestrians
    for i in range(10):
        agents['pedestrians'].append({
            'id': f'ped_{i}',
            'x': random.uniform(-111.93, -111.92),
            'y': random.uniform(33.417, 33.418)
        })

    # Create 5 vehicles
    for i in range(5):
        agents['vehicles'].append({
            'id': f'veh_{i}',
            'x': random.uniform(-111.93, -111.92),
            'y': random.uniform(33.417, 33.418)
        })

# Broadcast agent updates to the client
def update_positions():
    while True:
        # Move agents slightly for testing
        for ped in agents['pedestrians']:
            ped['x'] += random.uniform(-0.0001, 0.0001)
            ped['y'] += random.uniform(-0.0001, 0.0001)

        for veh in agents['vehicles']:
            veh['x'] += random.uniform(-0.0002, 0.0002)
            veh['y'] += random.uniform(-0.0002, 0.0002)

        # Emit updated positions to all clients
        socketio.emit('update', agents)
        time.sleep(1)  # Send updates every 1 second

# Start position update loop in a separate thread
initialize_agents()
threading.Thread(target=update_positions).start()

# Run the Flask app
if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
