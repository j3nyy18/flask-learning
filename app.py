from flask import Flask, request, jsonify
import json
import uuid
import os

app = Flask(__name__)


#LOAD USERS
def load_users():
    if not os.path.exists("users.json"):
        return {"users": []}

    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        #File doesn't exist - maybe first run
        return {"users":[]}
    except json.JSONDecodeError:
        #File is corrupted
        return  {"users":[]}
    except Exception as e:
        #Unexpected Error
        print(f"Unexpected error: {e}")
        return {"users": []}



#SAVE USER
def save_users(data):
    with open("users.json", "w") as f:
        json.dump(data, f, indent=2)



#VALIDATE UUID :  Check whether a string is a valid UUID
def is_valid_uuid(value):
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False



#VALIDATE UUID : Validate user_id from URL path parameter
def validate_uuid(user_id):
    if not is_valid_uuid(user_id):
        return "Invalid UUID format"
    return None



#VALIDATE USER DATA (REQUEST BODY)=> POST 
def validate_user_data(data):
    if not data:
        return "Request body is required"

    if "name" not in data:
        return "Missing 'name' field"

    if "email" not in data:
        return "Missing 'email' field"

    if "age" not in data:
        return "Missing 'age' field"

    if not isinstance(data["age"], int):
        return "Age must be an integer"

    return None #no error



#VALIDATE USER UPDATE DATA (REQUEST BODY)=> PATCH 
def validate_update_data(data):
    if not data:
        return "Request body is required"

    if "age" in data and not isinstance(data["age"], int):
        return "Age must be an integer"

    return None



###################################### CREATE USER #######################################
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    error = validate_user_data(data)
    if error:
        return jsonify({"error": error}), 400

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



###################################### GET USER #######################################
@app.route("/users", methods=["GET"])
def get_users():
    users_data = load_users()
    return jsonify(users_data), 200



###################################### GET SPECIFIC USER #######################################
@app.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    error = validate_uuid(user_id)
    if error:
        return jsonify({"error": error}), 400

    users_data = load_users()
    #next(generator, None)
    user = None
    for u in users_data["users"]:
        if u["id"] == user_id:
            user = u
            break
     
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user), 200



###################################### UPDATE USER #######################################
@app.route("/users/<user_id>", methods=["PATCH"])
def update_user(user_id):
    error = validate_uuid(user_id)
    if error:
        return jsonify({"error": error}), 400

    data = request.get_json()
    error = validate_update_data(data)
    if error:
        return jsonify({"error": error}), 400

    users_data = load_users()
    user = None
    for u in users_data["users"]:
        if u["id"] == user_id:
            user = u
            break

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



###################################### DELETE USER #######################################
@app.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    error = validate_uuid(user_id)
    if error:
        return jsonify({"error": error}), 400

    users_data = load_users()
    user = None
    for u in users_data["users"]:
        if u["id"] == user_id:
            user = u
            break
     
    if not user:
        return jsonify({"error": "User not found"}), 404

    users_data["users"].remove(user)
    save_users(users_data)

    return jsonify({"message": "User deleted successfully"}), 200



##################################### RUN APP ######################################
if __name__ == "__main__":
    app.run(debug=True)