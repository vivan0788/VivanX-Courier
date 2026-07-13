from flask import Blueprint, request, jsonify
from app.database import bookings_col
from app.utils.email_service import send_admin_notification, send_customer_confirmation
from datetime import datetime

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/api/book', methods=['POST'])
def create_booking():
    data = request.json
    
    # Simple Validation
    required_fields = ['senderName', 'senderMobile', 'senderEmail', 'senderAddress', 
                       'receiverName', 'receiverMobile', 'receiverEmail', 'receiverAddress', 
                       'weight', 'parcelType', 'pickupDate']
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing mandatory fields"}), 400

    booking_doc = {
        "sender": {
            "name": data['senderName'], "mobile": data['senderMobile'],
            "email": data['senderEmail'], "address": data['senderAddress']
        },
        "receiver": {
            "name": data['receiverName'], "mobile": data['receiverMobile'],
            "email": data['receiverEmail'], "address": data['receiverAddress']
        },
        "parcel": {
            "weight": float(data['weight']), "type": data['parcelType'],
            "instructions": data.get('specialInstructions', '')
        },
        "pickupDate": data['pickupDate'],
        "status": "Pending", # Initial workflow status
        "awb": None,
        "createdAt": datetime.utcnow(),
        "ipAddress": request.remote_addr
    }
    
    result = bookings_col.insert_one(booking_doc)
    booking_id = str(result.inserted_id)
    
    # Async background triggers via Mailgun
    send_admin_notification(booking_doc)
    send_customer_confirmation(booking_doc["sender"]["email"], booking_doc["sender"]["name"])
    
    return jsonify({"success": True, "message": "Booking request submitted successfully"}), 201
