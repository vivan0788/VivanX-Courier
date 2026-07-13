const Auth = {
    // Save token dynamically after verification
    saveSession(token) {
        localStorage.setItem('adminToken', token);
    },

    // Retrieve active tokens
    getToken() {
        return localStorage.getItem('adminToken');
    },

    // Secure guard execution
    checkProtection() {
        const token = this.getToken();
        if (!token) {
            alert("Unauthorized access detected. Redirecting to home portal...");
            window.location.href = 'index.html';
        }
    },

    // Clear session configuration
    destroySession() {
        localStorage.removeItem('adminToken');
        window.location.href = 'index.html';
    }
};