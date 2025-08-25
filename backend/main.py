import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# --- App setup ---
app = Flask(__name__)
CORS(app)

# --- Database config ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "contacts.db")

# Prefer Render's DATABASE_URL, fallback to local sqlite
db_url = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# --- Model ---
class Contact(db.Model):
    __tablename__ = "contact"  # Explicit table name to avoid case issues
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
        }

# --- Routes ---
@app.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all()
    return jsonify({"contacts": [c.to_json() for c in contacts]})

@app.route("/contacts", methods=["POST"])
def add_contact():
    data = request.get_json()
    if not data or not all(k in data for k in ("firstName", "lastName", "email")):
        return jsonify({"error": "Missing fields"}), 400

    contact = Contact(
        first_name=data["firstName"],
        last_name=data["lastName"],
        email=data["email"],
    )
    db.session.add(contact)
    db.session.commit()
    return jsonify(contact.to_json()), 201

@app.route("/contacts/<int:id>", methods=["DELETE"])
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    return jsonify({"message": "Contact deleted"})

# --- React frontend serve ---
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists("dist/" + path):
        return send_from_directory("dist", path)
    else:
        return send_from_directory("dist", "index.html")

# --- Run locally only ---
if __name__ == "__main__":
    # Create tables only for SQLite local dev
    if db_url.startswith("sqlite"):
        with app.app_context():
            db.create_all()
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
