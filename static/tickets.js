let tickets = [];
let autoRefreshInterval = null;

// ── Init ──────────────────────────────────────────────────────────────────────
document.querySelector('[data-tab="tickets"]').addEventListener('click', () => {
    loadTickets(); loadTicketStats(); startAutoRefresh();
});
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => { if (btn.dataset.tab !== 'tickets') stopAutoRefresh(); });
});

function startAutoRefresh() { stopAutoRefresh(); autoRefreshInterval = setInterval(() => refreshTicketsQuietly(), 30000); }
function stopAutoRefresh() { if (autoRefreshInterval) { clearInterval(autoRefreshInterval); autoRefreshInterval = null; } }

async function refreshTicketsQuietly() {
    try {
        const r = await fetch('/api/tickets/refresh', { method: 'POST' });
        const d = await r.json();
        if (r.ok && d.new_tickets > 0) { showNotification(`${d.new_tickets} new ticket(s) received`); await loadTickets(); loadTicketStats(); }
    } catch (e) { console.error('Auto-refresh error:', e); }
}

function showNotification(message) {
    const n = document.createElement('div');
    n.style.cssText = 'position:fixed;top:20px;right:20px;background:#6366f1;color:#fff;padding:14px 20px;border-radius:10px;box-shadow:0 8px 24px rgba(0,0,0,0.4);z-index:10000;font-size:13px;font-weight:500;animation:slideIn .3s ease-out;';
    n.textContent = message;
    if (!document.getElementById('notifStyle')) {
        const s = document.createElement('style'); s.id = 'notifStyle';
        s.textContent = '@keyframes slideIn{from{transform:translateX(300px);opacity:0}to{transform:translateX(0);opacity:1}}@keyframes slideOut{from{opacity:1}to{transform:translateX(300px);opacity:0}}';
        document.head.appendChild(s);
    }
    document.body.appendChild(n);
    setTimeout(() => { n.style.animation = 'slideOut .3s ease-out'; setTimeout(() => n.remove(), 300); }, 3000);
}

// ── Stats Dashboard ───────────────────────────────────────────────────────────
async function loadTicketStats() {
    try {
        const r = await fetch('/api/tickets/stats');
        if (!r.ok) return;
        const s = await r.json();
        document.getElementById('ticketStats').innerHTML = `
            <div class="stat-card open"><div class="stat-value">${s.open}</div><div class="stat-label">Open</div></div>
            <div class="stat-card in-progress"><div class="stat-value">${s.in_progress}</div><div class="stat-label">In Progress</div></div>
            <div class="stat-card resolved"><div class="stat-value">${s.resolved}</div><div class="stat-label">Resolved</div></div>
            <div class="stat-card closed"><div class="stat-value">${s.closed}</div><div class="stat-label">Closed</div></div>
            <div class="stat-card urgent"><div class="stat-value">${s.urgent + s.high}</div><div class="stat-label">Urgent / High</div></div>
        `;
    } catch (e) { console.error('Stats error:', e); }
}

// ── Load Tickets ──────────────────────────────────────────────────────────────
async function loadTickets() {
    try {
        const r = await fetch('/api/tickets');
        if (r.ok) { tickets = await r.json(); tickets.sort((a, b) => new Date(b.date) - new Date(a.date)); renderTickets(); }
    } catch (e) { console.error('Failed to load tickets:', e); }
}

async function refreshTickets() {
    try {
        const r = await fetch('/api/tickets/refresh', { method: 'POST' });
        const d = await r.json();
        if (r.ok) { showNotification(`Refreshed! Found ${d.new_tickets} new ticket(s)`); await loadTickets(); loadTicketStats(); }
        else { alert('Failed to refresh: ' + (d.error || 'Unknown error')); }
    } catch (e) { alert('Failed to refresh: ' + e.message); }
}

// ── Render Ticket List ────────────────────────────────────────────────────────
function renderTickets(statusFilter = 'all', priorityFilter = 'all', search = '') {
    const c = document.getElementById('ticketsList');
    let filtered = tickets.filter(t => {
        const ms = statusFilter === 'all' || t.status === statusFilter;
        const mp = priorityFilter === 'all' || t.priority === priorityFilter;
        const mq = search === '' ||
            t.subject.toLowerCase().includes(search.toLowerCase()) ||
            t.from_email.toLowerCase().includes(search.toLowerCase()) ||
            (t.body && t.body.toLowerCase().includes(search.toLowerCase())) ||
            (t.ticket_number && t.ticket_number.toString().includes(search));
        return ms && mp && mq;
    });

    if (filtered.length === 0) {
        c.innerHTML = '<div class="empty-state"><h3>No tickets found</h3><p>Configure your mail in Settings to start receiving tickets</p></div>';
        return;
    }

    c.innerHTML = filtered.map(t => {
        const priClass = `ticket-card-${t.priority || 'medium'}`;
        const ago = timeAgo(t.date);
        return `
        <div class="asset-card ${priClass}" style="cursor:pointer;" onclick="viewTicket(${t.id})">
            <div class="asset-main-content">
                <div class="asset-info" style="display:flex;gap:12px;align-items:flex-start;">
                    <div style="flex:1;min-width:0;">
                        <div style="display:flex;align-items:center;gap:8px;margin-bottom:5px;flex-wrap:wrap;">
                            <span class="ticket-num">#${t.ticket_number || 'N/A'}</span>
                            <span class="priority-badge priority-${t.priority || 'medium'}">${(t.priority || 'medium').toUpperCase()}</span>
                            ${t.category ? `<span style="font-size:11px;color:#6b7280;background:rgba(255,255,255,0.04);padding:2px 8px;border-radius:4px;">${t.category}</span>` : ''}
                        </div>
                        <h3 style="margin:0 0 4px;">${t.subject}</h3>
                        <p style="margin:0;"><strong>From:</strong> ${t.from_email} &nbsp;&middot;&nbsp; ${ago}</p>
                        ${t.assigned_to ? `<p style="margin:2px 0 0;font-size:12px;"><strong>Assigned:</strong> ${t.assigned_to}</p>` : ''}
                    </div>
                </div>
            </div>
            <div class="asset-actions" onclick="event.stopPropagation();">
                <span class="status-badge status-${t.status}">${t.status.toUpperCase()}</span>
            </div>
        </div>`;
    }).join('');
}

function timeAgo(dateStr) {
    const diff = Date.now() - new Date(dateStr).getTime();
    const m = Math.floor(diff / 60000);
    if (m < 1) return 'Just now';
    if (m < 60) return m + 'm ago';
    const h = Math.floor(m / 60);
    if (h < 24) return h + 'h ago';
    const d = Math.floor(h / 24);
    if (d < 30) return d + 'd ago';
    return new Date(dateStr).toLocaleDateString();
}

// ── View Ticket Detail (Jira-style) ──────────────────────────────────────────
function viewTicket(id) {
    const t = tickets.find(x => x.id === id);
    if (!t) return;
    const modal = document.getElementById('viewModal');
    const mc = document.getElementById('modalContent');
    modal.querySelector('.modal-content').style.maxWidth = '960px';

    // Build timeline
    let timeline = [];
    timeline.push({ type: 'original', date: t.date, html: `<div class="timeline-item reply"><div class="timeline-meta"><span class="label" style="color:#60a5fa;">Original Message from ${t.from_email}</span><span class="date">${new Date(t.date).toLocaleString()}</span></div><p style="white-space:pre-wrap;color:#b0b5c9;font-size:13px;margin:0;">${t.body || '(No body)'}</p></div>` });
    (t.replies || []).forEach(r => {
        const isClosure = r.type === 'auto-closure';
        const cls = isClosure ? 'closure' : 'reply';
        const lbl = isClosure ? 'Auto-Close Notification' : 'Reply sent to ' + r.to;
        const clr = isClosure ? '#34d399' : '#a5b4fc';
        timeline.push({ type: cls, date: r.date, html: `<div class="timeline-item ${cls}"><div class="timeline-meta"><span class="label" style="color:${clr};">${lbl}</span><span class="date">${new Date(r.date).toLocaleString()}</span></div><p style="white-space:pre-wrap;color:#b0b5c9;font-size:13px;margin:0;">${r.message}</p></div>` });
    });
    (t.notes || []).forEach(n => {
        timeline.push({ type: 'note', date: n.date, html: `<div class="timeline-item note"><div class="timeline-meta"><span class="label" style="color:#fbbf24;">Internal Note</span><span class="date">${new Date(n.date).toLocaleString()}</span></div><p style="white-space:pre-wrap;color:#b0b5c9;font-size:13px;margin:0;">${n.text}</p></div>` });
    });
    timeline.sort((a, b) => new Date(a.date) - new Date(b.date));

    mc.innerHTML = `
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;flex-wrap:wrap;">
            <span class="ticket-num" style="font-size:13px;">#${t.ticket_number || 'N/A'}</span>
            <h2 style="margin:0;flex:1;min-width:200px;">${t.subject}</h2>
        </div>
        <div class="ticket-detail-layout">
            <div class="ticket-detail-main">
                <h3 style="color:#8b8fa3;font-size:13px;text-transform:uppercase;letter-spacing:.5px;margin-bottom:12px;">Conversation</h3>
                ${timeline.map(x => x.html).join('')}
                <div style="display:flex;gap:8px;margin-top:16px;">
                    <button class="btn-primary btn-sm" onclick="showReplyForm(${t.id})">Reply</button>
                    <button class="btn-warn btn-sm" onclick="showAddNoteForm(${t.id})">Add Note</button>
                </div>
            </div>
            <div class="ticket-detail-sidebar">
                <div class="ticket-sidebar-card">
                    <div class="sidebar-row"><span class="sidebar-label">Status</span>
                        <select onchange="quickUpdate(${t.id},'status',this.value)" style="background:#1a1d2e;border:1px solid rgba(255,255,255,0.08);color:#c4c9f2;padding:4px 8px;border-radius:6px;font-size:12px;">
                            ${['open','in-progress','resolved','closed'].map(s => `<option value="${s}" ${t.status === s ? 'selected' : ''}>${s.charAt(0).toUpperCase()+s.slice(1)}</option>`).join('')}
                        </select>
                    </div>
                    <div class="sidebar-row"><span class="sidebar-label">Priority</span>
                        <select onchange="quickUpdate(${t.id},'priority',this.value)" style="background:#1a1d2e;border:1px solid rgba(255,255,255,0.08);color:#c4c9f2;padding:4px 8px;border-radius:6px;font-size:12px;">
                            ${['low','medium','high','urgent'].map(p => `<option value="${p}" ${t.priority === p ? 'selected' : ''}>${p.charAt(0).toUpperCase()+p.slice(1)}</option>`).join('')}
                        </select>
                    </div>
                    <div class="sidebar-row"><span class="sidebar-label">Category</span>
                        <select onchange="quickUpdate(${t.id},'category',this.value)" style="background:#1a1d2e;border:1px solid rgba(255,255,255,0.08);color:#c4c9f2;padding:4px 8px;border-radius:6px;font-size:12px;">
                            ${['','Hardware','Software','Network','Access','Other'].map(c => `<option value="${c}" ${t.category === c ? 'selected' : ''}>${c || 'None'}</option>`).join('')}
                        </select>
                    </div>
                    <div class="sidebar-row" style="flex-direction:column;align-items:stretch;gap:4px;">
                        <span class="sidebar-label">Assigned To</span>
                        <input type="text" value="${t.assigned_to || ''}" placeholder="Agent name"
                            onchange="quickUpdate(${t.id},'assigned_to',this.value)"
                            style="background:#1a1d2e;border:1px solid rgba(255,255,255,0.08);color:#c4c9f2;padding:6px 8px;border-radius:6px;font-size:12px;width:100%;">
                    </div>
                    <div class="sidebar-row" style="flex-direction:column;align-items:stretch;gap:4px;">
                        <span class="sidebar-label">Requester</span>
                        <span style="font-size:13px;color:#c4c9f2;word-break:break-all;">${t.from_email}</span>
                    </div>
                    <div class="sidebar-row" style="flex-direction:column;align-items:stretch;gap:4px;">
                        <span class="sidebar-label">Created</span>
                        <span style="font-size:12px;color:#8b8fa3;">${new Date(t.date).toLocaleString()}</span>
                    </div>
                </div>
            </div>
        </div>`;
    modal.style.display = 'flex';
}

// ── Quick Update (inline edits) ───────────────────────────────────────────────
async function quickUpdate(id, field, value) {
    try {
        const body = {}; body[field] = value;
        const r = await fetch(`/api/tickets/${id}`, {
            method: 'PUT', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        if (r.ok) {
            const d = await r.json();
            const idx = tickets.findIndex(t => t.id === id);
            if (idx !== -1 && d.ticket) tickets[idx] = d.ticket;
            renderTickets(
                document.getElementById('ticketStatusFilter').value,
                document.getElementById('ticketPriorityFilter').value,
                document.getElementById('searchTicket').value
            );
            loadTicketStats();
            if (field === 'status' && value === 'closed') showNotification('Ticket closed. Closure email sent.');
        }
    } catch (e) { alert('Update failed: ' + e.message); }
}

// ── Reply Form ────────────────────────────────────────────────────────────────
function showReplyForm(id) {
    const t = tickets.find(x => x.id === id); if (!t) return;
    const mc = document.getElementById('modalContent');
    mc.innerHTML = `
        <h2>Reply to Ticket #${t.ticket_number}</h2>
        <div class="detail-section"><p><strong>To:</strong> ${t.from_email}</p><p><strong>Subject:</strong> Re: ${t.subject}</p></div>
        <div class="form-group"><label>Your Reply</label><textarea id="replyMessage" rows="8" placeholder="Type your reply here..."></textarea></div>
        <div style="display:flex;gap:10px;">
            <button class="btn-primary" onclick="sendReply(${t.id})">Send Reply</button>
            <button class="btn-outline" onclick="viewTicket(${t.id})">Cancel</button>
        </div>`;
}

async function sendReply(id) {
    const t = tickets.find(x => x.id === id); if (!t) return;
    const msg = document.getElementById('replyMessage').value.trim();
    if (!msg) { alert('Please enter a reply'); return; }
    try {
        const r = await fetch('/api/tickets/reply', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ticket_id: id, to: t.from_email, subject: `Re: ${t.subject}`, message: msg })
        });
        if (r.ok) { showNotification('Reply sent!'); await loadTickets(); viewTicket(id); }
        else { alert('Failed to send reply.'); }
    } catch (e) { alert('Error: ' + e.message); }
}

// ── Add Note ──────────────────────────────────────────────────────────────────
function showAddNoteForm(id) {
    const t = tickets.find(x => x.id === id); if (!t) return;
    const mc = document.getElementById('modalContent');
    mc.innerHTML = `
        <h2>Add Note to Ticket #${t.ticket_number}</h2>
        <p style="color:#8b8fa3;font-size:13px;margin-bottom:16px;">Notes are internal and will not be sent to the customer.</p>
        <div class="form-group"><label>Note</label><textarea id="noteText" rows="6" placeholder="Internal notes..."></textarea></div>
        <div style="display:flex;gap:10px;">
            <button class="btn-primary" onclick="saveNote(${t.id})">Save Note</button>
            <button class="btn-outline" onclick="viewTicket(${t.id})">Cancel</button>
        </div>`;
}

async function saveNote(id) {
    const text = document.getElementById('noteText').value.trim();
    if (!text) { alert('Please enter a note'); return; }
    try {
        const r = await fetch(`/api/tickets/${id}/note`, {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ note: text })
        });
        if (r.ok) { showNotification('Note added!'); await loadTickets(); viewTicket(id); }
        else { alert('Failed to add note.'); }
    } catch (e) { alert('Error: ' + e.message); }
}

// ── Create Ticket Modal ───────────────────────────────────────────────────────
function showCreateTicketModal() { document.getElementById('createTicketModal').style.display = 'flex'; }

document.getElementById('createTicketForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const body = {
        from_email: document.getElementById('ctEmail').value,
        subject: document.getElementById('ctSubject').value,
        body: document.getElementById('ctBody').value,
        priority: document.getElementById('ctPriority').value,
        category: document.getElementById('ctCategory').value,
    };
    try {
        // We'll create ticket via the existing add mechanism (need a server endpoint)
        // For now reuse the ticket refresh or direct POST
        const r = await fetch('/api/tickets/create', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        if (r.ok) {
            showNotification('Ticket created!');
            document.getElementById('createTicketModal').style.display = 'none';
            document.getElementById('createTicketForm').reset();
            await loadTickets(); loadTicketStats();
        } else { alert('Failed to create ticket'); }
    } catch (e) { alert('Error: ' + e.message); }
});

// ── Status update modal (legacy compat) ───────────────────────────────────────
function showUpdateStatusModal(id) { viewTicket(id); }

// ── Filters ───────────────────────────────────────────────────────────────────
document.getElementById('ticketStatusFilter').addEventListener('change', applyTicketFilters);
document.getElementById('ticketPriorityFilter').addEventListener('change', applyTicketFilters);
document.getElementById('searchTicket').addEventListener('input', applyTicketFilters);

function applyTicketFilters() {
    renderTickets(
        document.getElementById('ticketStatusFilter').value,
        document.getElementById('ticketPriorityFilter').value,
        document.getElementById('searchTicket').value
    );
}
