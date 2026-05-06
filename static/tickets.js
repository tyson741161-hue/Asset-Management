let tickets = [];
let autoRefreshInterval = null;

// Load tickets when tickets tab is opened
document.querySelector('[data-tab="tickets"]').addEventListener('click', () => {
    loadTickets();
    startAutoRefresh();
});

// Stop auto-refresh when switching away from tickets tab
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        if (btn.dataset.tab !== 'tickets') {
            stopAutoRefresh();
        }
    });
});

// Start auto-refresh (every 30 seconds)
function startAutoRefresh() {
    // Clear any existing interval
    stopAutoRefresh();
    
    // Set up new interval - refresh every 30 seconds
    autoRefreshInterval = setInterval(() => {
        console.log('Auto-refreshing tickets...');
        refreshTicketsQuietly();
    }, 30000); // 30 seconds
}

// Stop auto-refresh
function stopAutoRefresh() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
        autoRefreshInterval = null;
    }
}

// Refresh tickets quietly (without alert)
async function refreshTicketsQuietly() {
    try {
        const response = await fetch('/api/tickets/refresh', { method: 'POST' });
        const result = await response.json();
        
        if (response.ok) {
            if (result.new_tickets > 0) {
                console.log(`Found ${result.new_tickets} new ticket(s)`);
                // Show a subtle notification
                showNotification(`${result.new_tickets} new ticket(s) received`);
            }
            await loadTickets();
        }
    } catch (error) {
        console.error('Auto-refresh error:', error);
    }
}

// Show notification
function showNotification(message) {
    // Create notification element
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #667eea;
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 10000;
        font-size: 14px;
        font-weight: 500;
        animation: slideIn 0.3s ease-out;
    `;
    notification.textContent = message;
    
    // Add animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(400px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(400px); opacity: 0; }
        }
    `;
    document.head.appendChild(style);
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Load tickets from server
async function loadTickets() {
    try {
        const response = await fetch('/api/tickets');
        if (response.ok) {
            tickets = await response.json();
            // Sort tickets by date, newest first
            tickets.sort((a, b) => new Date(b.date) - new Date(a.date));
            renderTickets();
        }
    } catch (error) {
        console.error('Failed to load tickets:', error);
    }
}

// Refresh tickets (manual - with alert)
async function refreshTickets() {
    try {
        const response = await fetch('/api/tickets/refresh', { method: 'POST' });
        const result = await response.json();
        
        if (response.ok) {
            alert(`Refreshed! Found ${result.new_tickets} new ticket(s)`);
            await loadTickets();
        } else {
            alert(`Failed to refresh tickets: ${result.error || 'Unknown error'}`);
            console.error('Refresh error:', result);
        }
    } catch (error) {
        alert('Failed to refresh tickets: ' + error.message);
        console.error('Refresh error:', error);
    }
}

// Render tickets list
function renderTickets(statusFilter = 'all', search = '') {
    const container = document.getElementById('ticketsList');
    
    let filtered = tickets.filter(ticket => {
        const matchesStatus = statusFilter === 'all' || ticket.status === statusFilter;
        const matchesSearch = search === '' || 
            ticket.subject.toLowerCase().includes(search.toLowerCase()) ||
            ticket.from_email.toLowerCase().includes(search.toLowerCase()) ||
            ticket.body.toLowerCase().includes(search.toLowerCase()) ||
            (ticket.ticket_number && ticket.ticket_number.toString().includes(search));
        return matchesStatus && matchesSearch;
    });
    
    if (filtered.length === 0) {
        container.innerHTML = '<div class="empty-state"><h3>No tickets found</h3><p>Emails sent to tyson741161@gmail.com will appear here as tickets</p></div>';
        return;
    }
    
    container.innerHTML = filtered.map(ticket => `
        <div class="asset-card">
            <div class="asset-main-content">
                <div class="asset-info">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                        <span style="background: #667eea; color: white; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: bold;">
                            #${ticket.ticket_number || 'N/A'}
                        </span>
                        <h3 style="margin: 0;">${ticket.subject}</h3>
                    </div>
                    <p><strong>From:</strong> ${ticket.from_email}</p>
                    <p><strong>Date:</strong> ${new Date(ticket.date).toLocaleString()}</p>
                    <p style="margin-top: 10px;">${ticket.body.substring(0, 150)}${ticket.body.length > 150 ? '...' : ''}</p>
                </div>
            </div>
            <div class="asset-actions">
                <span class="status-badge status-${ticket.status}">${ticket.status.toUpperCase()}</span>
                <button class="btn-view" onclick="viewTicket(${ticket.id})">View</button>
                <button class="btn-edit" onclick="showUpdateStatusModal(${ticket.id})">Update Status</button>
            </div>
        </div>
    `).join('');
}

// View ticket details
function viewTicket(id) {
    const ticket = tickets.find(t => t.id === id);
    if (!ticket) return;
    
    const modal = document.getElementById('viewModal');
    const modalContent = document.getElementById('modalContent');
    
    // Initialize arrays if they don't exist
    if (!ticket.notes) {
        ticket.notes = [];
    }
    if (!ticket.replies) {
        ticket.replies = [];
    }
    
    // Build replies HTML (conversation thread)
    let repliesHtml = '';
    if (ticket.replies && ticket.replies.length > 0) {
        repliesHtml = '<div style="margin-top: 20px;"><h3>Conversation</h3>';
        ticket.replies.forEach((reply, index) => {
            // Check if it's an auto-closure message
            const isAutoClosure = reply.type === 'auto-closure';
            const bgColor = isAutoClosure ? '#d4edda' : '#e3f2fd';
            const borderColor = isAutoClosure ? '#28a745' : '#2196f3';
            const labelColor = isAutoClosure ? '#155724' : '#1976d2';
            const label = isAutoClosure ? '✓ Ticket Closed - Auto Response Sent:' : 'You replied:';
            
            repliesHtml += `
                <div style="background: ${bgColor}; padding: 15px; margin: 10px 0; border-radius: 6px; border-left: 4px solid ${borderColor};">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <strong style="color: ${labelColor};">${label}</strong>
                        <span style="font-size: 13px; color: #666;">${new Date(reply.date).toLocaleString()}</span>
                    </div>
                    <p style="margin: 0; white-space: pre-wrap;">${reply.message}</p>
                </div>
            `;
        });
        repliesHtml += '</div>';
    }
    
    // Build notes HTML
    let notesHtml = '';
    if (ticket.notes && ticket.notes.length > 0) {
        notesHtml = '<div style="margin-top: 20px;"><h3>Internal Notes</h3>';
        ticket.notes.forEach((note, index) => {
            notesHtml += `
                <div style="background: #fff3cd; padding: 12px; margin: 10px 0; border-radius: 6px; border-left: 3px solid #ffc107;">
                    <p style="margin: 0; font-size: 13px; color: #666;">${new Date(note.date).toLocaleString()}</p>
                    <p style="margin: 8px 0 0 0; white-space: pre-wrap;">${note.text}</p>
                </div>
            `;
        });
        notesHtml += '</div>';
    }
    
    modalContent.innerHTML = `
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
            <span style="background: #667eea; color: white; padding: 6px 14px; border-radius: 4px; font-size: 14px; font-weight: bold;">
                Ticket #${ticket.ticket_number || 'N/A'}
            </span>
            <h2 style="margin: 0;">${ticket.subject}</h2>
        </div>
        <div class="modal-details">
            <div class="detail-section">
                <h3>Ticket Information</h3>
                <p><strong>From:</strong> ${ticket.from_email}</p>
                <p><strong>Date:</strong> ${new Date(ticket.date).toLocaleString()}</p>
                <p><strong>Status:</strong> <span class="status-badge status-${ticket.status}">${ticket.status.toUpperCase()}</span></p>
            </div>
            <div class="detail-section">
                <h3>Original Message</h3>
                <div style="background: #f8f9fa; padding: 15px; border-radius: 6px; max-height: 400px; overflow-y: auto;">
                    <p style="white-space: pre-wrap; margin: 0;">${ticket.body}</p>
                </div>
            </div>
            ${repliesHtml}
            ${notesHtml}
            <div style="display: flex; gap: 10px; margin-top: 20px;">
                <button class="btn-primary" onclick="showReplyForm(${ticket.id})" style="flex: 1;">
                    <span style="font-size: 16px;">✉️</span> Reply to Ticket
                </button>
                <button class="btn-edit" onclick="showAddNoteForm(${ticket.id})" style="flex: 1; background: #28a745; border: none;">
                    <span style="font-size: 16px;">📝</span> Add Note
                </button>
            </div>
        </div>
    `;
    
    modal.style.display = 'flex';
}

// Show reply form
function showReplyForm(id) {
    const ticket = tickets.find(t => t.id === id);
    if (!ticket) return;
    
    const modal = document.getElementById('viewModal');
    const modalContent = document.getElementById('modalContent');
    
    modalContent.innerHTML = `
        <h2>Reply to Ticket</h2>
        <div class="modal-details">
            <div class="detail-section">
                <p><strong>To:</strong> ${ticket.from_email}</p>
                <p><strong>Subject:</strong> Re: ${ticket.subject}</p>
            </div>
            <div class="detail-section">
                <h3>Your Reply</h3>
                <textarea id="replyMessage" rows="10" style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; font-family: inherit;" placeholder="Type your reply here..."></textarea>
            </div>
            <div style="display: flex; gap: 10px; margin-top: 20px;">
                <button class="btn-primary" onclick="sendReply(${ticket.id})">Send Reply</button>
                <button class="btn-edit" onclick="viewTicket(${ticket.id})" style="background: #6c757d;">Cancel</button>
            </div>
        </div>
    `;
}

// Send reply
async function sendReply(id) {
    const ticket = tickets.find(t => t.id === id);
    if (!ticket) return;
    
    const replyMessage = document.getElementById('replyMessage').value.trim();
    
    if (!replyMessage) {
        alert('Please enter a reply message');
        return;
    }
    
    try {
        const response = await fetch('/api/tickets/reply', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ticket_id: id,
                to: ticket.from_email,
                subject: `Re: ${ticket.subject}`,
                message: replyMessage
            })
        });
        
        if (response.ok) {
            alert('Reply sent successfully!');
            await loadTickets(); // Reload tickets to get the updated data with the reply
            viewTicket(id);
        } else {
            alert('Failed to send reply. Please try again.');
        }
    } catch (error) {
        alert('Failed to send reply: ' + error.message);
    }
}

// Show add note form
function showAddNoteForm(id) {
    const ticket = tickets.find(t => t.id === id);
    if (!ticket) return;
    
    const modal = document.getElementById('viewModal');
    const modalContent = document.getElementById('modalContent');
    
    modalContent.innerHTML = `
        <h2>Add Note to Ticket</h2>
        <div class="modal-details">
            <div class="detail-section">
                <p><strong>Ticket:</strong> ${ticket.subject}</p>
            </div>
            <div class="detail-section">
                <h3>Note</h3>
                <textarea id="noteText" rows="8" style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; font-family: inherit;" placeholder="Add internal notes about this ticket..."></textarea>
                <p style="font-size: 12px; color: #666; margin-top: 8px;">Notes are internal and will not be sent to the customer.</p>
            </div>
            <div style="display: flex; gap: 10px; margin-top: 20px;">
                <button class="btn-primary" onclick="saveNote(${ticket.id})">Save Note</button>
                <button class="btn-edit" onclick="viewTicket(${ticket.id})" style="background: #6c757d;">Cancel</button>
            </div>
        </div>
    `;
}

// Save note
async function saveNote(id) {
    const noteText = document.getElementById('noteText').value.trim();
    
    if (!noteText) {
        alert('Please enter a note');
        return;
    }
    
    try {
        const response = await fetch(`/api/tickets/${id}/note`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ note: noteText })
        });
        
        if (response.ok) {
            alert('Note added successfully!');
            await loadTickets();
            viewTicket(id);
        } else {
            alert('Failed to add note. Please try again.');
        }
    } catch (error) {
        alert('Failed to add note: ' + error.message);
    }
}

// Show update status modal with dropdown
function showUpdateStatusModal(id) {
    const ticket = tickets.find(t => t.id === id);
    if (!ticket) return;
    
    const modal = document.getElementById('viewModal');
    const modalContent = document.getElementById('modalContent');
    
    modalContent.innerHTML = `
        <h2>Update Ticket Status</h2>
        <div class="modal-details">
            <div class="detail-section">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                    <span style="background: #667eea; color: white; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: bold;">
                        #${ticket.ticket_number || 'N/A'}
                    </span>
                    <h3 style="margin: 0;">${ticket.subject}</h3>
                </div>
                <p><strong>From:</strong> ${ticket.from_email}</p>
                <p><strong>Current Status:</strong> <span class="status-badge status-${ticket.status}">${ticket.status.toUpperCase()}</span></p>
            </div>
            <div class="detail-section">
                <h3>Select New Status</h3>
                <div class="form-group">
                    <label>Status</label>
                    <select id="newTicketStatus" style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px;">
                        <option value="open" ${ticket.status === 'open' ? 'selected' : ''}>Open</option>
                        <option value="in-progress" ${ticket.status === 'in-progress' ? 'selected' : ''}>In Progress</option>
                        <option value="resolved" ${ticket.status === 'resolved' ? 'selected' : ''}>Resolved</option>
                        <option value="closed" ${ticket.status === 'closed' ? 'selected' : ''}>Closed</option>
                    </select>
                </div>
                <button class="btn-primary" onclick="updateTicketStatus(${ticket.id})" style="margin-top: 15px;">Update Status</button>
            </div>
        </div>
    `;
    
    modal.style.display = 'flex';
}

// Update ticket status
async function updateTicketStatus(id) {
    const newStatus = document.getElementById('newTicketStatus').value;
    
    try {
        const response = await fetch(`/api/tickets/${id}/status`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: newStatus })
        });
        
        if (response.ok) {
            if (newStatus === 'closed') {
                alert('Status updated successfully!\n\nAn automatic closure email has been sent to the customer.');
            } else {
                alert('Status updated successfully!');
            }
            document.getElementById('viewModal').style.display = 'none';
            await loadTickets();
        }
    } catch (error) {
        alert('Failed to update status');
    }
}

// Ticket filters
document.getElementById('ticketStatusFilter').addEventListener('change', (e) => {
    const search = document.getElementById('searchTicket').value;
    renderTickets(e.target.value, search);
});

document.getElementById('searchTicket').addEventListener('input', (e) => {
    const statusFilter = document.getElementById('ticketStatusFilter').value;
    renderTickets(statusFilter, e.target.value);
});
