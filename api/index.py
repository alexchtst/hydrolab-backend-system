# api/index.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World!"

@app.route("/about")
def about():
    return "About Page"

if __name__ == "__main__":
    # Only for local development, Vercel handles production execution
    app.run(debug=True)
