// Main JavaScript file for Telegram AdBot

// Global variables
let socket = null;
let isConnected = false;

// Initialize Socket.IO connection
function initSocket() {
    socket = io();
    
    socket.on('connect', function() {
        console.log('Connected to server');
        isConnected = true;
    });
    
    socket.on('disconnect', function() {
        console.log('Disconnected from server');
        isConnected = false;
    });
    
    socket.on('bot_status', function(data) {
        updateBotStatus(data);
    });
    
    socket.on('forwarding_update', function(data) {
        updateForwardingStatus(data);
    });
}

// Update bot status display
function updateBotStatus(data) {
    const statusElement = document.getElementById('connection-status');
    if (statusElement) {
        if (data.connected) {
            statusElement.className = 'alert alert-success';
            statusElement.innerHTML = `<i class="fas fa-check-circle"></i> ${data.message}`;
        } else {
            statusElement.className = 'alert alert-danger';
            statusElement.innerHTML = `<i class="fas fa-exclamation-triangle"></i> ${data.message}`;
        }
    }
}

// Update forwarding status
function updateForwardingStatus(data) {
    if (data.running) {
        document.getElementById('start-auto-btn').disabled = true;
        document.getElementById('stop-auto-btn').disabled = false;
    } else {
        document.getElementById('start-auto-btn').disabled = false;
        document.getElementById('stop-auto-btn').disabled = true;
    }
}

// Show notification
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Format date
function formatDate(dateString) {
    if (!dateString) return 'Never';
    const date = new Date(dateString);
    return date.toLocaleString();
}

// Format number with commas
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Show loading spinner
function showLoading(element) {
    element.disabled = true;
    element.innerHTML = '<span class="loading"></span> Loading...';
}

// Hide loading spinner
function hideLoading(element, originalText) {
    element.disabled = false;
    element.innerHTML = originalText;
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Socket.IO
    initSocket();
    
    // Add global error handler
    window.addEventListener('error', function(e) {
        console.error('Global error:', e.error);
        showNotification('An error occurred. Please check the console for details.', 'danger');
    });
    
    // Add unhandled promise rejection handler
    window.addEventListener('unhandledrejection', function(e) {
        console.error('Unhandled promise rejection:', e.reason);
        showNotification('An error occurred. Please check the console for details.', 'danger');
    });
});

// Export functions for use in templates
window.showNotification = showNotification;
window.formatDate = formatDate;
window.formatNumber = formatNumber;
window.showLoading = showLoading;
window.hideLoading = hideLoading; 