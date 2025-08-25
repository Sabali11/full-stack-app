import os
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# --- App setup ---
app = Flask(__name__, static_folder="dist")
CORS(app)

# --- Database setup ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# --- Model ---
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email
        }

# --- API routes ---
@app.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all()
    return jsonify({"contacts": [c.to_json() for c in contacts]}), 200

@app.route("/contacts", methods=["POST"])
def create_contacts():
    data = request.json
    first_name = data.get("firstName")
    last_name = data.get("lastName")
    email = data.get("email")

    if not first_name or not last_name or not email:
        return jsonify({"message": "You must fill all fields"}), 400

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
    return jsonify({"message": "User updated"}), 200

@app.route("/contacts/<int:id>", methods=["DELETE"])
def delete_contact(id):
    contact = Contact.query.get(id)
    if not contact:
        return jsonify({"message": "User does not exist"}), 400

    db.session.delete(contact)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200

# --- Serve React frontend ---
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join("dist", path)):
        return send_from_directory("dist", path)
    else:
        return send_from_directory("dist", "index.html")

# --- Run server ---
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # ensures tables exist
    # Use PORT environment variable for Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
