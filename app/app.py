from flask import Flask, jsonify
import os

app = Flask(__name__)

ENV = os.environ.get("APP_ENV", "development")
VERSION = os.environ.get("APP_VERSION", "1.0.0")


@app.route("/")
def index():
    return jsonify({
        "message": "devops-ci-cd-demo is running",
        "env": ENV,
        "version": VERSION
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/ready")
def ready():
    return jsonify({"status": "ready"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
