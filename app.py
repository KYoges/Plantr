from flask import Flask, render_template, jsonify
import threading
import time
import os

# Initialize Flask app with the correct template folder
app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'frontend', 'templates'))

# This prints the current working directory to confirm we're using the right path
print("Current working directory:", os.getcwd())

def generate_data():
    time.sleep(5)  # Simulating a time-consuming task
    # Place your actual data generation code here.

@app.route('/')
def index():
    return render_template('loading-sreen.html')  # Rendering the template

@app.route('/start_task')
def start_task():
    # Start the background task in a separate thread
    thread = threading.Thread(target=generate_data)
    thread.start()
    return jsonify({'status': 'Task started'})

if __name__ == '__main__':
    app.run(debug=True)

