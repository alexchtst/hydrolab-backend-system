from flask import Blueprint, request, jsonify
from services.data_service import *

offline_route = Blueprint("offline_data", __name__)

@offline_route.route("/data", methods=["GET"])
def api_all_data():
    """
    Get all station data
    ---
    responses:
      200:
        description: List of all stations
    """
    return jsonify(get_all_data())

@offline_route.route("/data/paginated", methods=["GET"])
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

@offline_route.route("/data/<int:station_id>", methods=["GET"])
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

@offline_route.route("/search", methods=["GET"])
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

@offline_route.route("/pairing/<string:id>", methods=["GET"])
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

@offline_route.route("/statistical/<string:id>", methods=["GET"])
def api_pairing_statistical(id):
    """
    Get pure statistical data
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Statistical pairing data
    """
    return jsonify(get_statistical_data_by_id(id))
