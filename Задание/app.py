from flask import Flask, request, jsonify
from models import Crack
from database import Base, engine, SessionLocal
import json

Base.metadata.create_all(bind=engine)
app = Flask(__name__)

@app.route("/")
def root():
    return {"message": "Glass Crack Detection System"}

@app.route("/cracks", methods=["GET"])
def get_cracks():
    db = SessionLocal()
    cracks = db.query(Crack).all()
    db.close()
    return jsonify([{
        "id": c.id,
        "location": c.location,
        "length": c.length,
        "depth": c.depth,
        "status": c.status
    } for c in cracks])

@app.route("/cracks", methods=["POST"])
def add_crack():
    db = SessionLocal()
    data = request.args
    crack = Crack(
        location=data.get("location"),
        length=float(data.get("length")),
        depth=float(data.get("depth")),
        status=data.get("status")
    )
    db.add(crack)
    db.commit()
    db.refresh(crack)
    db.close()
    return jsonify({"id": crack.id})

@app.route("/cracks/<int:crack_id>", methods=["DELETE"])
def delete_crack(crack_id):
    db = SessionLocal()
    crack = db.query(Crack).filter(Crack.id == crack_id).first()
    if crack:
        db.delete(crack)
        db.commit()
        db.close()
        return jsonify({"message": "Deleted"})
    else:
        db.close()
        return jsonify({"error": "Not found"}), 404

@app.route("/cracks/upload_json", methods=["POST"])
def upload_json():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    try:
        data = json.load(file)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON"}), 400

    if not isinstance(data, list):
        return jsonify({"error": "JSON must be a list"}), 400

    db = SessionLocal()
    added = 0
    for entry in data:
        try:
            crack = Crack(
                location=entry["location"],
                length=float(entry["length"]),
                depth=float(entry["depth"]),
                status=entry["status"]
            )
            db.add(crack)
            added += 1
        except:
            continue

    db.commit()
    db.close()
    return jsonify({"added": added})
