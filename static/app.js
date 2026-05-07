// Initialize data
let assets = [];
let isLoggedIn = false;

// ── Settings Menu ─────────────────────────────────────────────────────────────
function toggleSettingsMenu() {
    const dd = document.getElementById('settingsDropdown');
    dd.classList.toggle('open');
}

// Close dropdown when clicking outside
document.addEventListener('click', (e) => {
    const wrapper = document.querySelector('.settings-wrapper');
    if (wrapper && !wrapper.contains(e.target)) {
        document.getElementById('settingsDropdown').classList.remove('open');
    }
});

function showProfileModal() {
    document.getElementById('settingsDropdown').classList.remove('open');
    document.getElementById('profileModal').style.display = 'flex';
}

function showMailConfigModal() {
    document.getElementById('settingsDropdown').classList.remove('open');
    loadMailConfig();
    document.getElementById('mailConfigModal').style.display = 'flex';
}

async function doLogout() {
    document.getElementById('settingsDropdown').classList.remove('open');
    try { await fetch('/api/logout', { method: 'POST' }); } catch (e) {}
    isLoggedIn = false;
    document.getElementById('mainApp').style.display = 'none';
    document.getElementById('loginScreen').style.display = 'flex';
    document.getElementById('loginForm').reset();
}

// ── Mail Config ───────────────────────────────────────────────────────────────
async function loadMailConfig() {
    try {
        const r = await fetch('/api/settings/email');
        const d = await r.json();
        if (d.configured && d.config) {
            document.getElementById('mcEmail').value = d.config.email_address || '';
            document.getElementById('mcPassword').value = '';
            document.getElementById('mcPassword').placeholder = 'Password saved (enter new to change)';
            document.getElementById('mcSmtp').value = d.config.smtp_server || 'smtp.gmail.com';
            document.getElementById('mcSmtpPort').value = d.config.smtp_port || 587;
            document.getElementById('mcImap').value = d.config.imap_server || 'imap.gmail.com';
            document.getElementById('mcTls').checked = d.config.use_tls !== false;
            updateMailDot(true);
        } else {
            updateMailDot(false);
        }
    } catch (e) { console.error('Load mail config error:', e); }
}

function updateMailDot(connected) {
    const dot = document.getElementById('mailStatusDot');
    if (dot) {
        dot.className = 'mail-dot ' + (connected ? 'connected' : 'disconnected');
    }
}

async function testMailConfig() {
    const btn = document.getElementById('mcTestBtn');
    const result = document.getElementById('mcTestResult');
    btn.textContent = 'Testing...'; btn.disabled = true;

    const data = {
        email_address: document.getElementById('mcEmail').value,
        app_password: document.getElementById('mcPassword').value,
        smtp_server: document.getElementById('mcSmtp').value,
        smtp_port: parseInt(document.getElementById('mcSmtpPort').value),
        imap_server: document.getElementById('mcImap').value,
        use_tls: document.getElementById('mcTls').checked,
    };

    try {
        const r = await fetch('/api/settings/email/test', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const d = await r.json();
        let html = '';
        if (d.results.imap) html += '<span style="color:#34d399;">&#10003; IMAP OK</span>';
        else html += `<span style="color:#f87171;">&#10007; IMAP Failed: ${d.results.imap_error}</span>`;
        html += '<br>';
        if (d.results.smtp) html += '<span style="color:#34d399;">&#10003; SMTP OK</span>';
        else html += `<span style="color:#f87171;">&#10007; SMTP Failed: ${d.results.smtp_error}</span>`;
        result.innerHTML = `<div style="background:rgba(255,255,255,0.03);padding:12px;border-radius:8px;font-size:13px;margin-top:8px;">${html}</div>`;
    } catch (e) {
        result.innerHTML = `<div style="color:#f87171;font-size:13px;">Test failed: ${e.message}</div>`;
    }
    btn.textContent = 'Test Connection'; btn.disabled = false;
}

document.getElementById('mailConfigForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        email_address: document.getElementById('mcEmail').value,
        app_password: document.getElementById('mcPassword').value,
        smtp_server: document.getElementById('mcSmtp').value,
        smtp_port: parseInt(document.getElementById('mcSmtpPort').value),
        imap_server: document.getElementById('mcImap').value,
        use_tls: document.getElementById('mcTls').checked,
    };

    if (!data.app_password) {
        alert('Please enter the app password'); return;
    }

    try {
        const r = await fetch('/api/settings/email', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const d = await r.json();
        if (d.success) {
            if (typeof showNotification === 'function') showNotification('Mail configured successfully!');
            else alert('Mail configured!');
            updateMailDot(true);
            document.getElementById('mailConfigModal').style.display = 'none';
        } else {
            alert('Failed: ' + d.message);
        }
    } catch (e) { alert('Error: ' + e.message); }
});

// ── Login ─────────────────────────────────────────────────────────────────────
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    const errorDiv = document.getElementById('loginError');

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (data.success) {
            isLoggedIn = true;
            document.getElementById('loginScreen').style.display = 'none';
            document.getElementById('mainApp').style.display = 'block';
            errorDiv.textContent = '';
            await loadAssets();
            renderAssets();
            if (typeof loadTickets === 'function') loadTickets();
            if (typeof loadTicketStats === 'function') loadTicketStats();
            if (typeof loadRequests === 'function') loadRequests();
            // Check mail config status
            loadMailConfig();
        } else {
            errorDiv.textContent = 'Invalid username or password';
        }
    } catch (error) {
        errorDiv.textContent = 'Login failed. Please try again.';
    }
});

// ── Show Add Asset Form Modal ─────────────────────────────────────────────────
function showAddAssetForm() {
    document.getElementById('addAssetModal').style.display = 'flex';
}

function closeAddAssetForm() {
    document.getElementById('addAssetModal').style.display = 'none';
    document.getElementById('assetForm').reset();
    document.getElementById('laptopFields').style.display = 'none';
    document.getElementById('mouseFields').style.display = 'none';
    document.getElementById('firewallFields').style.display = 'none';
    document.getElementById('ramFields').style.display = 'none';
    document.getElementById('laptopAccessories').style.display = 'none';
    document.getElementById('assetIdField').style.display = 'block';
    document.getElementById('modelField').style.display = 'block';
}

// Load assets from server
async function loadAssets() {
    try {
        const response = await fetch('/api/assets');
        if (response.ok) {
            assets = await response.json();
        }
    } catch (error) {
        console.error('Failed to load assets:', error);
    }
}

// Tab switching
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.dataset.tab;
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById(tabName).classList.add('active');
    });
});

// Show/hide type-specific fields
document.getElementById('assetType').addEventListener('change', (e) => {
    const assetType = e.target.value;
    const laptopAccessories = document.getElementById('laptopAccessories');
    const laptopFields = document.getElementById('laptopFields');
    const mouseFields = document.getElementById('mouseFields');
    const firewallFields = document.getElementById('firewallFields');
    const ramFields = document.getElementById('ramFields');
    const assetIdField = document.getElementById('assetIdField');
    const assetIdInput = document.getElementById('assetId');
    const modelField = document.getElementById('modelField');
    const modelInput = document.getElementById('assetModel');

    laptopAccessories.style.display = 'none';
    laptopFields.style.display = 'none';
    mouseFields.style.display = 'none';
    firewallFields.style.display = 'none';
    ramFields.style.display = 'none';

    if (assetType === 'laptop') {
        laptopAccessories.style.display = 'block'; laptopFields.style.display = 'block';
        assetIdField.style.display = 'block'; assetIdInput.required = true;
        modelField.style.display = 'block'; modelInput.required = true;
    } else if (assetType === 'mouse') {
        mouseFields.style.display = 'block';
        assetIdField.style.display = 'none'; assetIdInput.required = false;
        modelField.style.display = 'block'; modelInput.required = true;
    } else if (assetType === 'firewall') {
        firewallFields.style.display = 'block';
        assetIdField.style.display = 'none'; assetIdInput.required = false;
        modelField.style.display = 'none'; modelInput.required = false;
    } else if (assetType === 'ram') {
        ramFields.style.display = 'block';
        assetIdField.style.display = 'none'; assetIdInput.required = false;
        modelField.style.display = 'none'; modelInput.required = false;
    } else {
        laptopFields.style.display = 'block';
        assetIdField.style.display = 'block'; assetIdInput.required = true;
        modelField.style.display = 'block'; modelInput.required = true;
    }
});

// Add asset form
document.getElementById('assetForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const form = e.target;
    const editId = form.dataset.editId;
    const assetType = document.getElementById('assetType').value;

    let assetData = {
        type: assetType,
        assetId: (assetType === 'mouse' || assetType === 'firewall' || assetType === 'ram') ? `${assetType.toUpperCase()}-${Date.now()}` : document.getElementById('assetId').value,
        model: (assetType === 'firewall' || assetType === 'ram') ? '' : document.getElementById('assetModel').value,
        status: document.getElementById('status').value
    };

    if (assetType === 'laptop') {
        assetData.serialNumber = document.getElementById('serialNumber').value;
        assetData.configuration = document.getElementById('configuration').value;
        assetData.officeLocation = document.getElementById('officeLocation').value;
        assetData.year = document.getElementById('year').value;
        assetData.currentCondition = document.getElementById('currentCondition').value;
        assetData.currentUser = document.getElementById('currentUser').value;
        assetData.lastUser = document.getElementById('lastUser').value;
        assetData.accessories = {
            mouse: document.getElementById('mouseName').value,
            headphone: document.getElementById('headphoneName').value,
            charger: document.getElementById('chargerName').value,
            monitor: document.getElementById('monitorName').value
        };
    } else if (assetType === 'mouse') {
        assetData.quantity = document.getElementById('mouseQuantity').value;
        assetData.mouseType = document.getElementById('mouseType').value;
        assetData.location = document.getElementById('mouseLocation').value;
    } else if (assetType === 'firewall') {
        assetData.firewallName = document.getElementById('firewallName').value;
        assetData.serialNumber = document.getElementById('firewallSerial').value;
        assetData.purchaseYear = document.getElementById('firewallYear').value;
        assetData.lastFirmwareUpdate = document.getElementById('lastFirmwareUpdate').value;
        assetData.location = document.getElementById('firewallLocation').value;
    } else if (assetType === 'ram') {
        assetData.ramName = document.getElementById('ramName').value;
        assetData.ramSize = document.getElementById('ramSize').value;
        assetData.ramDDR = document.getElementById('ramDDR').value;
        assetData.ramFrequency = document.getElementById('ramFrequency').value;
        assetData.quantity = document.getElementById('ramQuantity').value;
        assetData.location = document.getElementById('ramLocation').value;
    } else {
        assetData.serialNumber = document.getElementById('serialNumber')?.value || '';
        assetData.configuration = document.getElementById('configuration')?.value || '';
        assetData.officeLocation = document.getElementById('officeLocation')?.value || '';
        assetData.year = document.getElementById('year')?.value || '';
        assetData.currentCondition = document.getElementById('currentCondition')?.value || '';
        assetData.currentUser = document.getElementById('currentUser')?.value || '';
        assetData.lastUser = document.getElementById('lastUser')?.value || '';
    }

    try {
        if (editId) {
            const response = await fetch(`/api/assets/${editId}`, {
                method: 'PUT', headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(assetData)
            });
            if (response.ok) {
                const result = await response.json();
                const index = assets.findIndex(a => a.id == editId);
                if (index !== -1) assets[index] = result.asset;
                alert('Asset updated successfully!');
            }
            delete form.dataset.editId;
        } else {
            const response = await fetch('/api/assets', {
                method: 'POST', headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(assetData)
            });
            if (response.ok) {
                const result = await response.json();
                assets.push(result.asset);
                alert('Asset added successfully!');
            }
        }

        form.reset();
        closeAddAssetForm();
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        document.querySelector('[data-tab="assets"]').classList.add('active');
        document.getElementById('assets').classList.add('active');
        renderAssets();
    } catch (error) {
        alert('Error saving asset. Please try again.');
    }
});

async function saveAssets() {}

// Render assets list
function renderAssets(categoryFilter = 'all', statusFilter = 'all', officeFilter = 'all', search = '') {
    const container = document.getElementById('assetsList');

    let filtered = assets.filter(asset => {
        const matchesCategory = categoryFilter === 'all' || asset.type === categoryFilter;
        const matchesStatus = statusFilter === 'all' || asset.status === statusFilter;
        const assetLocation = asset.officeLocation || asset.location || '';
        const matchesOffice = officeFilter === 'all' || assetLocation === officeFilter;
        const matchesSearch = search === '' ||
            (asset.assetId && asset.assetId.toLowerCase().includes(search.toLowerCase())) ||
            (asset.model && asset.model.toLowerCase().includes(search.toLowerCase())) ||
            (asset.firewallName && asset.firewallName.toLowerCase().includes(search.toLowerCase())) ||
            (asset.currentUser && asset.currentUser.toLowerCase().includes(search.toLowerCase())) ||
            (asset.lastUser && asset.lastUser.toLowerCase().includes(search.toLowerCase()));
        return matchesCategory && matchesStatus && matchesOffice && matchesSearch;
    });

    if (filtered.length === 0) {
        container.innerHTML = '<div class="empty-state"><h3>No assets found</h3><p>Add your first asset to get started</p></div>';
        return;
    }

    container.innerHTML = filtered.map(asset => `
        <div class="asset-card">
            <div class="asset-main-content">
                <div class="asset-info">
                    <h3>${asset.type === 'firewall' && asset.firewallName ? asset.firewallName : (asset.type === 'ram' && asset.ramName ? asset.ramName : (asset.type.charAt(0).toUpperCase() + asset.type.slice(1) + ((asset.type !== 'mouse' && asset.type !== 'firewall' && asset.type !== 'ram') ? ' - ' + asset.assetId : '')))}</h3>
                    ${asset.model ? `<p><strong>Model:</strong> ${asset.model}</p>` : ''}
                    ${asset.currentUser ? `<p><strong>Current User:</strong> ${asset.currentUser}</p>` : ''}
                    ${asset.officeLocation ? `<p><strong>Location:</strong> ${asset.officeLocation}</p>` : ''}
                    ${asset.location ? `<p><strong>Location:</strong> ${asset.location}</p>` : ''}
                    ${asset.quantity ? `<p><strong>Quantity:</strong> ${asset.quantity}</p>` : ''}
                </div>
            </div>
            <div class="asset-actions">
                <span class="status-badge status-${asset.status}">${asset.status}</span>
                <button class="btn-view" onclick="viewAsset(${asset.id})">View</button>
                <button class="btn-edit" onclick="editAsset(${asset.id})">Edit</button>
                <button class="btn-delete" onclick="deleteAsset(${asset.id})">Delete</button>
            </div>
        </div>
    `).join('');
}

// Delete asset
async function deleteAsset(id) {
    const code = prompt('Enter security code to delete:');
    if (code !== '4181') { alert('Invalid security code.'); return; }
    if (confirm('Are you sure you want to delete this asset?')) {
        try {
            const response = await fetch(`/api/assets/${id}`, { method: 'DELETE' });
            if (response.ok) { assets = assets.filter(a => a.id !== id); renderAssets(); alert('Asset deleted!'); }
            else { alert('Failed to delete.'); }
        } catch (e) { alert('Error deleting asset.'); }
    }
}

// Edit asset
async function editAsset(id) {
    const code = prompt('Enter security code to edit:');
    if (code !== '4181') { alert('Invalid security code.'); return; }
    const asset = assets.find(a => a.id === id);
    if (!asset) return;

    showAddAssetForm();
    document.getElementById('assetType').value = asset.type;
    document.getElementById('assetType').dispatchEvent(new Event('change'));

    if (asset.type !== 'mouse' && asset.type !== 'firewall') document.getElementById('assetId').value = asset.assetId || '';
    if (asset.type !== 'firewall') document.getElementById('assetModel').value = asset.model || '';
    document.getElementById('status').value = asset.status;

    if (asset.type === 'laptop') {
        document.getElementById('serialNumber').value = asset.serialNumber || '';
        document.getElementById('configuration').value = asset.configuration || '';
        document.getElementById('officeLocation').value = asset.officeLocation || '';
        document.getElementById('year').value = asset.year || '';
        document.getElementById('currentCondition').value = asset.currentCondition || '';
        document.getElementById('currentUser').value = asset.currentUser || '';
        document.getElementById('lastUser').value = asset.lastUser || '';
        if (asset.accessories) {
            document.getElementById('mouseName').value = asset.accessories.mouse || '';
            document.getElementById('headphoneName').value = asset.accessories.headphone || '';
            document.getElementById('chargerName').value = asset.accessories.charger || '';
            document.getElementById('monitorName').value = asset.accessories.monitor || '';
        }
    }
    if (asset.type === 'mouse') {
        document.getElementById('mouseQuantity').value = asset.quantity || '';
        document.getElementById('mouseType').value = asset.mouseType || '';
        document.getElementById('mouseLocation').value = asset.location || '';
    }
    if (asset.type === 'firewall') {
        document.getElementById('firewallName').value = asset.firewallName || '';
        document.getElementById('firewallSerial').value = asset.serialNumber || '';
        document.getElementById('firewallYear').value = asset.purchaseYear || '';
        document.getElementById('lastFirmwareUpdate').value = asset.lastFirmwareUpdate || '';
        document.getElementById('firewallLocation').value = asset.location || '';
    }
    if (asset.type === 'ram') {
        document.getElementById('ramName').value = asset.ramName || '';
        document.getElementById('ramSize').value = asset.ramSize || '';
        document.getElementById('ramDDR').value = asset.ramDDR || '';
        document.getElementById('ramFrequency').value = asset.ramFrequency || '';
        document.getElementById('ramQuantity').value = asset.quantity || '';
        document.getElementById('ramLocation').value = asset.location || '';
    }

    document.querySelector('#assetForm button[type="submit"]').textContent = 'Update Asset';
    document.getElementById('assetForm').dataset.editId = id;
}

// View asset details
function viewAsset(id) {
    const asset = assets.find(a => a.id === id);
    if (!asset) return;
    const modal = document.getElementById('viewModal');
    const modalContent = document.getElementById('modalContent');
    modal.querySelector('.modal-content').style.maxWidth = '900px';

    let html = `
        <h2>${asset.type === 'firewall' && asset.firewallName ? asset.firewallName : (asset.type === 'ram' && asset.ramName ? asset.ramName : (asset.type.charAt(0).toUpperCase() + asset.type.slice(1) + ((asset.type !== 'mouse' && asset.type !== 'firewall' && asset.type !== 'ram') ? ' - ' + asset.assetId : '')))}</h2>
        <div class="modal-details">
            <div class="detail-section">
                <h3>Basic Information</h3>
                <p><strong>Asset Type:</strong> ${asset.type.charAt(0).toUpperCase() + asset.type.slice(1)}</p>
                ${(asset.type !== 'mouse' && asset.type !== 'firewall' && asset.type !== 'ram') ? `<p><strong>Asset ID:</strong> ${asset.assetId}</p>` : ''}
                ${asset.model ? `<p><strong>Model:</strong> ${asset.model}</p>` : ''}
                ${asset.serialNumber ? `<p><strong>Serial Number:</strong> ${asset.serialNumber}</p>` : ''}
                ${asset.configuration ? `<p><strong>Configuration:</strong> ${asset.configuration}</p>` : ''}
                ${asset.officeLocation ? `<p><strong>Office Location:</strong> ${asset.officeLocation}</p>` : ''}
                ${asset.location ? `<p><strong>Location:</strong> ${asset.location}</p>` : ''}
                <p><strong>Status:</strong> <span class="status-badge status-${asset.status}">${asset.status}</span></p>
            </div>
        </div>`;
    modalContent.innerHTML = html;
    modal.style.display = 'flex';
}

// Close modal
function closeModal() {
    document.getElementById('viewModal').style.display = 'none';
}

// Filters
document.getElementById('categoryFilter').addEventListener('change', (e) => {
    renderAssets(e.target.value, document.getElementById('statusFilter').value, document.getElementById('officeFilter').value, document.getElementById('searchAsset').value);
});
document.getElementById('statusFilter').addEventListener('change', (e) => {
    renderAssets(document.getElementById('categoryFilter').value, e.target.value, document.getElementById('officeFilter').value, document.getElementById('searchAsset').value);
});
document.getElementById('officeFilter').addEventListener('change', (e) => {
    renderAssets(document.getElementById('categoryFilter').value, document.getElementById('statusFilter').value, e.target.value, document.getElementById('searchAsset').value);
});
document.getElementById('searchAsset').addEventListener('input', (e) => {
    renderAssets(document.getElementById('categoryFilter').value, document.getElementById('statusFilter').value, document.getElementById('officeFilter').value, e.target.value);
});

if (isLoggedIn) { loadAssets().then(() => renderAssets()); }
