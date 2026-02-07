# api/index.py
from flask import Flask, jsonify, request
import pymongo
from dotenv import load_dotenv
import os

load_dotenv()

DB_URI = os.getenv("MONGODB_URI_CONNECTION")
DB_DOC = "hydrolab-database-v0"

database_client = pymongo.MongoClient(DB_URI)
collection_name = database_client[DB_DOC]

LAT_BINS = [(-90, -30), (-30, 30), (30, 90)]
LON_BINS = [
    (-180, -120), (-120, -60), (-60, 0),
    (0, 60), (60, 120), (120, 180)
]


def find_area(lat, lon):

    area_id = 1

    for lat_min, lat_max in LAT_BINS:
        for lon_min, lon_max in LON_BINS:

            if (
                lat_min <= lat < lat_max and
                lon_min <= lon < lon_max
            ):
                return f"Area_{area_id}"

            area_id += 1

    return None


app = Flask(__name__)


@app.route("/")
def home():
    return "API IS RUNNING WELL"


@app.route("/api/search", methods=["GET"])
def get_contents():
    try:
        data = request.get_json()
        latitude = float(data["lat"])
        longitude = float(data["lon"])
        range = float(data["range"])

        if latitude is None or longitude is None:
            return jsonify({"message": "lat & lon required"}), 400

        area = find_area(latitude, longitude)

        if not area:
            return jsonify({
                "message": "Out of bound",
                "area": "OOB",
                "count": 0,
                "data": []
            }), 404

        collection = collection_name[area]
        
        data = list(collection.find())

        return jsonify({
            "message": "success",
            "area": area,
            "count": len(data),
            "data": data
        }), 200

    except Exception as e:
        return jsonify({
            "message": str(e),
            "area": "OOB",
            "count": 0,
            "data": []
        }), 500


# local development only
if __name__ == "__main__":
    app.run(debug=True)
