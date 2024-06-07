from flask import Flask, jsonify
import requests
from threading import Timer

app = Flask(__name__)

# Variable to store the data
data = None

# Function to request data from the server
def fetch_data():
    global data
    try:
        response = requests.get("https://api.example.com/data")  # Replace with your URL
        data = response.json()
    except Exception as e:
        data = {"error": str(e)}

    # Schedule the function to run again in 1 hour (3600 seconds)
    Timer(3600, fetch_data).start()

# Initial data fetch
fetch_data()

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=8080)