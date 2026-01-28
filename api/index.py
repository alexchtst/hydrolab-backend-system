# api/index.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "API IS RUNNING WELL"

@app.route("/about")
def about():
    return "About Page"

# Dummy data
DATA_CONTENT = [
    {
        "id": "1",
        "name": "Lokasi A",
        "description": "Ini adalah lokasi A",
        "long": 106.84513,
        "lat": -6.21462
    },
    {
        "id": "2",
        "name": "Lokasi B",
        "description": "Ini adalah lokasi B",
        "long": 107.61912,
        "lat": -6.91746
    },
    {
        "id": "3",
        "name": "Lokasi C",
        "description": "Ini adalah lokasi C",
        "long": 110.36949,
        "lat": -7.79558
    }
]

@app.route("/api/contents", methods=["GET"])
def get_contents():
    return jsonify({
        "status": "success",
        "data": DATA_CONTENT
    })

@app.route("/api/contents/<string:content_id>", methods=["GET"])
def get_content_by_id(content_id):
    content = next((item for item in DATA_CONTENT if item["id"] == content_id), None)
    
    if content is None:
        return jsonify({
            "status": "error",
            "message": "Data not found"
        }), 404

    return jsonify({
        "status": "success",
        "data": content
    })

# local development only
if __name__ == "__main__":
    app.run(debug=True)
