# api/index.py
from flask import Flask, jsonify, request
import pymongo
from dotenv import load_dotenv
import math
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

OFFSET_PAGINATION = 10
MAX_TOTAL_DATA = 600


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

EARTH_RADIUS_KM = 6371

def haversine(lat1, lon1, lat2, lon2):
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lon / 2) ** 2
    )

    return EARTH_RADIUS_KM * 2 * math.asin(math.sqrt(a))


def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc

app = Flask(__name__)


@app.route("/")
def home():
    return "API IS RUNNING WELL"


@app.route("/api/data/<int:pagination>", methods=["GET"])
def get_all(pagination: int):
    try:
        collection = collection_name["full_data"]

        if pagination < 1:
            pagination = 1

        limit = OFFSET_PAGINATION
        skip = (pagination - 1) * limit

        cursor = collection.find().skip(skip).limit(limit)

        data = list(cursor)

        total_data = collection.count_documents({})

        return jsonify({
            "message": "success",
            "page": pagination,
            "per_page": limit,
            "total_data": total_data,
            "total_page": (total_data + limit - 1) // limit,
            "data": data
        }), 200

    except Exception as e:
        return jsonify({
            "message": str(e),
            "count": 0,
            "data": []
        }), 500


@app.route("/api/detail/<id>", methods=["GET"])
def get_cdetail_content(id: str):
    try:
        collection = collection_name["full_data"]
        document = collection.find_one({"_id": id})
        return jsonify({
            "message": "success",
            "data": document
        }), 200
    except Exception as E:
        return jsonify({
            "message": str(E),
            "data": None
        }), 500


@app.route("/api/search", methods=["GET"])
def get_contents():
    try:
        latitude = request.args.get("lat", type=float)
        longitude = request.args.get("lon", type=float)
        radius_km = request.args.get("range", type=float, default=10)

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

        # Ambil semua candidate di area
        candidates = list(collection.find())

        result = []

        for doc in candidates:
            lat2 = doc.get("latitude")
            lon2 = doc.get("longitude")

            if lat2 is None or lon2 is None:
                continue

            distance = haversine(latitude, longitude, lat2, lon2)

            if distance <= radius_km:
                doc["distance"] = distance
                result.append(serialize_doc(doc))

        # Sort berdasarkan jarak
        result.sort(key=lambda x: x["distance"])

        return jsonify({
            "message": "success",
            "area": area,
            "count": len(result),
            "data": result
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
