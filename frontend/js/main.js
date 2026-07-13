document.addEventListener("DOMContentLoaded", () => {
    // Initialize standard icon engines if present in layout framework
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
    
    console.log("VivanX Logistics Frontend Client Interlinked Successfully.");
});

// UI Helper Utility Functions
const UI = {
    showLoadingSpinner(elementId) {
        const el = document.getElementById(elementId);
        if(el) el.innerHTML = `<div class="spinner" style="border: 4px solid #f3f3f3; border-top: 4px solid var(--primary); border-radius: 50%; width: 30px; height: 30px; animation: spin 1s linear infinite; margin: 1rem auto;"></div>`;
    },
    
    clearElement(elementId) {
        const el = document.getElementById(elementId);
        if(el) el.innerHTML = '';
    }
};

// Global CSS Keyframe Injector for Loaders
const styleElement = document.createElement("style");
styleElement.innerHTML = `@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }`;
document.head.appendChild(styleElement);