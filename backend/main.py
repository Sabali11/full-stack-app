from flask import request, jsonify, send_from_directory
from config import app, db
import os
from model import Contact
from flask_cors import CORS

CORS(app)

# --- API Routes ---
@app.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all()
    return jsonify({"contacts": [c.to_json() for c in contacts]}), 200

@app.route("/contacts", methods=["POST"])
def create_contacts():
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")
    if not first_name or not last_name or not email:
        return jsonify({"message":"You must fill all fields"}), 400
    new_contact = Contact(first_name=first_name, last_name=last_name, email=email)
    try:
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    return jsonify({"message": "Contact added"}), 201

@app.route("/contacts/<int:id>", methods=["PUT"])
def update_contact(id):
    contact = Contact.query.get(id)
    if not contact:
        return jsonify({"message": "User not found"}), 404
    data = request.json
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)
    db.session.commit()
    return jsonify({"message":"User updated"}), 200

@app.route("/contacts/<int:id>", methods=["DELETE"])
def delete_contact(id):
    contact = Contact.query.get(id)
    if not contact:
        return jsonify({"message":"User does not exist"}), 400
    db.session.delete(contact)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200

# --- Serve React ---
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists("dist/" + path):
        return send_from_directory("dist", path)
    else:
        return send_from_directory("dist", "index.html")

# --- Run server ---
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=False)


