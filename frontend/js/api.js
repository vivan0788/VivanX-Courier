// Centralized Endpoint Architecture
const API_BASE_URL = "https://your-backend-render-app.onrender.com/api"; // Render Live link se replace karein

const API = {
    // Public Modules
    async bookParcel(bookingData) {
        const response = await fetch(`${API_BASE_URL}/book`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(bookingData)
        });
        return response;
    },

    async trackParcel(awbNumber) {
        const response = await fetch(`${API_BASE_URL}/track/${awbNumber}`);
        return response;
    },

    // Administrative Gateways
    async adminLogin(credentials) {
        const response = await fetch(`${API_BASE_URL}/admin/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(credentials)
        });
        return response;
    },

    async fetchAllBookings(token) {
        const response = await fetch(`${API_BASE_URL}/admin/bookings`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        return response;
    },

    async acceptBookingOrder(id, token) {
        const response = await fetch(`${API_BASE_URL}/admin/bookings/${id}/accept`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        return response;
    }
};
