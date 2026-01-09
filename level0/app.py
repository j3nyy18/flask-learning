from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Hello, Flask!"})

@app.route("/ping")
def ping():
    return jsonify({"pong": True})

if __name__ == "__main__":
    # Development configuration
    app.run(
        host='127.0.0.1',  # Localhost only
        port=5000,          # Default Flask port
        debug=True          # Enable auto-reload and detailed errors
    )
