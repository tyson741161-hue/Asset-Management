let requests = [];

// Show request form modal
function showRequestForm() {
    document.getElementById('requestFormModal').style.display = 'flex';
}

// Close request form modal
function closeRequestForm() {
    document.getElementById('requestFormModal').style.display = 'none';
    document.getElementById('requestForm').reset();
}

// Load requests when request tab is opened
document.querySelector('[data-tab="request"]').addEventListener('click', () => {
    loadRequests();
});

// Load requests from server
async function loadRequests() {
    try {
        const response = await fetch('/api/requests');
        if (response.ok) {
            requests = await response.json();
            // Sort requests by date, newest first
            requests.sort((a, b) => new Date(b.date) - new Date(a.date));
            renderRequests();
        }
    } catch (error) {
        console.error('Failed to load requests:', error);
    }
}

// Render requests list
function renderRequests() {
    const container = document.getElementById('requestsList');
    
    if (requests.length === 0) {
        container.innerHTML = '<div class="empty-state"><h3>No requests submitted yet</h3><p>Click "Submit a Request" to create your first request</p></div>';
        return;
    }
    
    container.innerHTML = requests.map(request => `
        <div class="asset-card">
            <div class="asset-main-content">
                <div class="asset-info">
                    <h3>${request.subject}</h3>
                    <p><strong>To:</strong> ${request.email || 'N/A'}</p>
                    <p><strong>Submitted:</strong> ${new Date(request.date).toLocaleString()}</p>
                    <p style="margin-top: 10px;">${request.description.substring(0, 150)}${request.description.length > 150 ? '...' : ''}</p>
                </div>
            </div>
            <div class="asset-actions">
                <span class="status-badge" style="background: #e3f2fd; color: #004085;">SUBMITTED</span>
                <button class="btn-view" onclick="viewRequest(${request.id})">View Details</button>
            </div>
        </div>
    `).join('');
}

// View request details
function viewRequest(id) {
    const request = requests.find(r => r.id === id);
    if (!request) return;
    
    const modal = document.getElementById('viewModal');
    const modalContent = document.getElementById('modalContent');
    
    modalContent.innerHTML = `
        <h2>${request.subject}</h2>
        <div class="modal-details">
            <div class="detail-section">
                <h3>Request Information</h3>
                <p><strong>Sent To:</strong> ${request.email || 'N/A'}</p>
                <p><strong>Submitted:</strong> ${new Date(request.date).toLocaleString()}</p>
                <p><strong>Status:</strong> <span class="status-badge" style="background: #e3f2fd; color: #004085;">SUBMITTED</span></p>
            </div>
            <div class="detail-section">
                <h3>Description</h3>
                <div style="background: #f8f9fa; padding: 15px; border-radius: 6px;">
                    <p style="white-space: pre-wrap; margin: 0;">${request.description}</p>
                </div>
            </div>
        </div>
    `;
    
    modal.style.display = 'flex';
}

// Handle request form submission
document.getElementById('requestForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('requestEmail').value;
    const subject = document.getElementById('requestSubject').value;
    const description = document.getElementById('requestDescription').value;
    
    try {
        const response = await fetch('/api/send-request', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, subject, description })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            alert('Request submitted successfully!');
            closeRequestForm();
            // Reload requests to show the new one
            await loadRequests();
        } else {
            alert('Failed to submit request. Please try again.');
        }
    } catch (error) {
        alert('Error submitting request. Please try again.');
    }
});
