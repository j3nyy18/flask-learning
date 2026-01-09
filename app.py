from flask import Flask, request, jsonify
import json
import uuid
import os

app = Flask(__name__)

def load_users():
    if not os.path.exists("users.json"):
        return {"users": []}

    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"users": []}

def save_users(data):
    with open("users.json", "w") as f:
        json.dump(data, f, indent=2)

def is_valid_uuid(value):
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False
    
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    if "name" not in data or "email" not in data or "age" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    users_data = load_users()

    new_user = {
        "id": str(uuid.uuid4()),
        "name": data["name"],
        "email": data["email"],
        "age": data["age"]
    }

    users_data["users"].append(new_user)
    save_users(users_data)

    return jsonify({
        "message": "User created successfully",
        "user": new_user
    }), 201


@app.route("/users", methods=["GET"])
def get_users():
    users_data = load_users()
    return jsonify(users_data), 200

@app.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    if not is_valid_uuid(user_id):
        return jsonify({"error": "Invalid UUID format"}), 400

    users_data = load_users()
    user = next((u for u in users_data["users"] if u["id"] == user_id), None)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user), 200

@app.route("/users/<user_id>", methods=["PATCH"])
def update_user(user_id):
    if not is_valid_uuid(user_id):
        return jsonify({"error": "Invalid UUID format"}), 400

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    users_data = load_users()
    user = next((u for u in users_data["users"] if u["id"] == user_id), None)

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Update only provided fields
    for field in ["name", "email", "age"]:
        if field in data:
            user[field] = data[field]

    save_users(users_data)

    return jsonify({
        "message": "User updated successfully",
        "user": user
    }), 200

@app.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    if not is_valid_uuid(user_id):
        return jsonify({"error": "Invalid UUID format"}), 400

    users_data = load_users()
    user = next((u for u in users_data["users"] if u["id"] == user_id), None)

    if not user:
        return jsonify({"error": "User not found"}), 404

    users_data["users"].remove(user)
    save_users(users_data)

    return jsonify({"message": "User deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)