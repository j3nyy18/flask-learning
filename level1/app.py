from flask import Flask, request, jsonify

app = Flask(__name__)

#Problem: 1
@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    operation = data.get("operation")
    x = data.get("x")
    y = data.get("y")

    if isinstance(operation, str):
        operation = operation.lower()

    if operation is None or x is None or y is None:
        return jsonify({"error": "Missing operation, x, or y"}), 400

    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        return jsonify({"error": "x and y must be numbers"}), 400

    if operation == "add":
        result = x + y
    elif operation == "subtract":
        result = x - y
    elif operation == "multiply":
        result = x * y
    elif operation == "divide":
        if y == 0:
            return jsonify({"error": "Division by zero"}), 400
        result = x / y
    else:
        return jsonify({"error": "Invalid operation"}), 400

    return jsonify({"result": result}), 200

#Problem: 2
@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q")

    if not query:
        return jsonify({"error": "Missing query parameter 'q'"}), 400

    return jsonify({"query": query}), 200

if __name__ == "__main__":
    app.run(debug=True)