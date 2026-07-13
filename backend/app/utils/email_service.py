import requests
from app.config import Config

def send_admin_notification(booking):
    url = f"https://api.mailgun.net/v3/{Config.MAILGUN_DOMAIN}/messages"
    auth = ("api", Config.MAILGUN_API_KEY)
    data = {
        "from": f"VivanX System <noreply@{Config.MAILGUN_DOMAIN}>",
        "to": Config.ADMIN_EMAIL,
        "subject": "New Booking Order Alert - Action Required",
        "text": f"""
        New order received.
        Sender: {booking['sender']['name']} ({booking['sender']['mobile']})
        Receiver: {booking['receiver']['name']} ({booking['receiver']['mobile']})
        Weight: {booking['parcel']['weight']} KG
        Type: {booking['parcel']['type']}
        Pickup Window: {booking['pickupDate']}
        IP: {booking['ipAddress']}
        """
    }
    return requests.post(url, auth=auth, data=data)

def send_customer_confirmation(email, name):
    url = f"https://api.mailgun.net/v3/{Config.MAILGUN_DOMAIN}/messages"
    auth = ("api", Config.MAILGUN_API_KEY)
    data = {
        "from": f"VivanX Courier <support@{Config.MAILGUN_DOMAIN}>",
        "to": email,
        "subject": "Booking Request Received",
        "text": f"Hello {name},\n\nThank you for choosing VivanX Courier.\n\nWe have successfully received your parcel request. Our team will contact you within a few hours through Call or WhatsApp for booking confirmation.\n\nThank you."
    }
    return requests.post(url, auth=auth, data=data)
