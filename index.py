from flask import Flask, request, jsonify
from flasgger import Swagger
from services.data_service import *

app = Flask(__name__)
swagger = Swagger(app)

@app.route("/")
def home():
    """
    Home Endpoint
    ---
    responses:
      200:
        description: Return the api system status and documentation
    """
    return jsonify({
        "message": "API IS RUNNING WELL",
        "hosted-api-documentation": "https://hydrolab-backend-system.vercel.app/apidocs",
        "local-api-documentation": "http://localhost:5000/apidocs"
    }), 200

@app.route("/data", methods=["GET"])
def api_all_data():
    """
    Get all station data
    ---
    responses:
      200:
        description: List of all stations
    """
    return jsonify(get_all_data())

@app.route("/data/paginated", methods=["GET"])
def api_paginated():
    """
    Get paginated data
    ---
    parameters:
      - name: page
        in: query
        type: integer
        required: false
      - name: limit
        in: query
        type: integer
        required: false
    responses:
      200:
        description: Paginated result
    """

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 20))

    return jsonify(get_paginated_data(page, limit))

@app.route("/data/<int:station_id>", methods=["GET"])
def api_by_id(station_id):
    """
    Get station by ID
    ---
    parameters:
      - name: station_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Station data
    """
    return jsonify(get_data_by_id(station_id))

@app.route("/search", methods=["GET"])
def api_search():
    """
    Search nearest stations
    ---
    parameters:
      - name: lat
        in: query
        type: number
        required: true
      - name: lon
        in: query
        type: number
        required: true
      - name: radius
        in: query
        type: number
        required: false
    responses:
      200:
        description: Nearest stations
    """

    lat = float(request.args.get("lat"))
    lon = float(request.args.get("lon"))
    radius = float(request.args.get("radius", 1))

    return jsonify(search_nearest(lat, lon, radius))

@app.route("/pairing/<string:id>", methods=["GET"])
def api_pairing(id):
    """
    Get pairing statistical data
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Pairing data
    """
    return jsonify(get_pairing_data_by_id(id))

if __name__ == "__main__":
    app.run(debug=True)