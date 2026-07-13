from flask import Blueprint, request, jsonify
from app.database import admins_col, bookings_col, tracking_col, counter_col
from bson.objectid import ObjectId
import bcrypt
import jwt
from datetime import datetime, timedelta
from app.config import Config

auth_bp = Blueprint('auth', __name__)

def generate_awb():
    # Format: VX250713000001 -> Change prefix elements cleanly based on date sequence if desired
    # For scale uniformity:
    counter = counter_col.find_one_and_update(
        {"_id": "awb_sequence"},
        {"$inc": {"sequence_value": 1}},
        return_document=True
    )
    seq = str(counter["sequence_value"]).zfill(6)
    current_date = datetime.now().strftime("%y%m%d")
    return f"VX{current_date}{seq}"

@auth_bp.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    admin = admins_col.find_one({"username": data.get('username')})
    
    if admin and bcrypt.checkpw(data.get('password').encode('utf-8'), admin['password']):
        token = jwt.encode({
            'user': admin['username'],
            'exp': datetime.utcnow() + timedelta(hours=8)
        }, Config.JWT_SECRET, algorithm="HS256")
        return jsonify({"token": token}), 200
        
    return jsonify({"error": "Invalid Credentials"}), 401

@auth_bp.route('/api/admin/bookings/<id>/accept', methods=['POST'])
def accept_booking(id):
    booking = bookings_col.find_one({"_id": ObjectId(id)})
    if not booking:
        return jsonify({"error": "Not Found"}), 404
        
    if booking.get('awb'):
        return jsonify({"error": "AWB already assigned"}), 400
        
    awb = generate_awb()
    bookings_col.update_one({"_id": ObjectId(id)}, {"$set": {"status": "Accepted", "awb": awb}})
    
    # Initialize real-time tracking pipeline records
    tracking_col.insert_one({
        "awb": awb,
        "currentLocation": "Main Booking Hub",
        "estimatedDelivery": (datetime.utcnow() + timedelta(days=4)).strftime("%Y-%m-%d"),
        "timeline": [
            {"status": "Manifest Created", "location": "System Hub", "time": datetime.utcnow().strftime("%Y-%m-%d %H:%M")}
        ]
    })
    return jsonify({"success": True, "awb": awb})
