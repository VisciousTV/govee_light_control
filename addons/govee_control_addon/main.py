import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Retrieve configuration from environment variables set by Home Assistant
API_KEY = os.environ.get("api_key", "")
PORT = int(os.environ.get("port", 5000))
GOVEE_API_BASE_URL = "https://developer-api.govee.com/v1"

if not API_KEY:
    print("Error: No Govee API key provided. Please set 'api_key' in the add-on options.")
    exit(1)

# Common headers for Govee API requests
headers = {
    "Govee-API-Key": API_KEY,
    "Content-Type": "application/json"
}


@app.route("/")
def index():
    return "Govee Control Add-on is running."


@app.route("/devices", methods=["GET"])
def get_devices():
    """
    Retrieve a list of your Govee devices.
    """
    url = f"{GOVEE_API_BASE_URL}/devices"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": response.text}), response.status_code


@app.route("/devices/<device_id>/control", methods=["PUT"])
def control_device(device_id):
    """
    Control a specific Govee device.
    Expected JSON payload:
    {
      "model": "<device_model>",
      "cmd": {
         "name": "<command_name>",
         "value": <command_value>
      }
    }
    Example: To turn a device on, you might send:
    {
      "model": "H6003",
      "cmd": { "name": "turn", "value": "on" }
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload."}), 400

    payload = {
        "device": device_id,
        "model": data.get("model"),
        "cmd": data.get("cmd")
    }

    url = f"{GOVEE_API_BASE_URL}/devices/control"
    response = requests.put(url, headers=headers, json=payload)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": response.text}), response.status_code


if __name__ == "__main__":
    # Listen on all interfaces so the add-on is reachable via ingress.
    app.run(host="0.0.0.0", port=PORT)
