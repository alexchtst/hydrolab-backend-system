from flask import Flask, request, jsonify
from flask_cors import CORS
from flasgger import Swagger
from routes.offline_data_route import offline_route as offline_api
from routes.online_data_route import online_route as online_api

app = Flask(__name__)
swagger = Swagger(app)
CORS(app, origins=["*"])

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

app.register_blueprint(offline_api, url_prefix="/offline-data")
app.register_blueprint(online_api, url_prefix="/online-data")

if __name__ == "__main__":
    app.run(debug=True)