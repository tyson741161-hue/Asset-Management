// Initialize data
let assets = [];
let isLoggedIn = false;

// Show Add Asset Form Modal
function showAddAssetForm() {
    document.getElementById('addAssetModal').style.display = 'flex';
}

// Close Add Asset Form Modal
function closeAddAssetForm() {
    document.getElementById('addAssetModal').style.display = 'none';
    document.getElementById('assetForm').reset();
    // Hide all conditional fields
    document.getElementById('laptopFields').style.display = 'none';
    document.getElementById('mouseFields').style.display = 'none';
    document.getElementById('firewallFields').style.display = 'none';
    document.getElementById('ramFields').style.display = 'none';
    document.getElementById('laptopAccessories').style.display = 'none';
    document.getElementById('assetIdField').style.display = 'block';
    document.getElementById('modelField').style.display = 'block';
}

// Handle login
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
            // Load tickets since it's now the default tab
            if (typeof loadTickets === 'function') {
                loadTickets();
            }
            // Load requests
            if (typeof loadRequests === 'function') {
                loadRequests();
            }
        } else {
            errorDiv.textContent = 'Invalid username or password';
        }
    } catch (error) {
        errorDiv.textContent = 'Login failed. Please try again.';
    }
});

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

// Show/hide laptop accessories fields
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
    
    // Hide all conditional fields first
    laptopAccessories.style.display = 'none';
    laptopFields.style.display = 'none';
    mouseFields.style.display = 'none';
    firewallFields.style.display = 'none';
    ramFields.style.display = 'none';
    
    if (assetType === 'laptop') {
        laptopAccessories.style.display = 'block';
        laptopFields.style.display = 'block';
        assetIdField.style.display = 'block';
        assetIdInput.required = true;
        modelField.style.display = 'block';
        modelInput.required = true;
    } else if (assetType === 'mouse') {
        mouseFields.style.display = 'block';
        assetIdField.style.display = 'none';
        assetIdInput.required = false;
        modelField.style.display = 'block';
        modelInput.required = true;
    } else if (assetType === 'firewall') {
        firewallFields.style.display = 'block';
        assetIdField.style.display = 'none';
        assetIdInput.required = false;
        modelField.style.display = 'none';
        modelInput.required = false;
    } else if (assetType === 'ram') {
        ramFields.style.display = 'block';
        assetIdField.style.display = 'none';
        assetIdInput.required = false;
        modelField.style.display = 'none';
        modelInput.required = false;
    } else {
        // For other types, show basic fields
        laptopFields.style.display = 'block';
        assetIdField.style.display = 'block';
        assetIdInput.required = true;
        modelField.style.display = 'block';
        modelInput.required = true;
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
    
    // Add type-specific fields
    if (assetType === 'laptop') {
        assetData.serialNumber = document.getElementById('serialNumber').value;
        assetData.configuration = document.getElementById('configuration').value;
        assetData.officeLocation = document.getElementById('officeLocation').value;
        assetData.year = document.getElementById('year').value;
        assetData.currentCondition = document.getElementById('currentCondition').value;
        assetData.currentUser = document.getElementById('currentUser').value;
        assetData.lastUser = document.getElementById('lastUser').value;
        
        // Add laptop accessories
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
        // For other asset types, include basic fields
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
            // Update existing asset
            const response = await fetch(`/api/assets/${editId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(assetData)
            });
            
            if (response.ok) {
                const result = await response.json();
                const index = assets.findIndex(a => a.id == editId);
                if (index !== -1) {
                    assets[index] = result.asset;
                }
                alert('Asset updated successfully!');
            }
            delete form.dataset.editId;
        } else {
            // Add new asset
            const response = await fetch('/api/assets', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(assetData)
            });
            
            if (response.ok) {
                const result = await response.json();
                assets.push(result.asset);
                alert('Asset added successfully!');
            }
        }
        
        // Reset form and close modal
        form.reset();
        closeAddAssetForm();
        
        // Switch to assets tab to see the new/updated asset
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        document.querySelector('[data-tab="assets"]').classList.add('active');
        document.getElementById('assets').classList.add('active');
        
        renderAssets();
    } catch (error) {
        alert('Error saving asset. Please try again.');
    }
});

// Save assets to server
async function saveAssets() {
    // This function is kept for compatibility but actual saving happens in add/update/delete functions
}

// Render assets list
function renderAssets(categoryFilter = 'all', statusFilter = 'all', officeFilter = 'all', search = '') {
    const container = document.getElementById('assetsList');
    
    let filtered = assets.filter(asset => {
        const matchesCategory = categoryFilter === 'all' || asset.type === categoryFilter;
        const matchesStatus = statusFilter === 'all' || asset.status === statusFilter;
        // Check both officeLocation and location fields for office filter
        const assetLocation = asset.officeLocation || asset.location || '';
        const matchesOffice = officeFilter === 'all' || assetLocation === officeFilter;
        const matchesSearch = search === '' || 
            asset.assetId.toLowerCase().includes(search.toLowerCase()) ||
            asset.model.toLowerCase().includes(search.toLowerCase()) ||
            (asset.firewallName && asset.firewallName.toLowerCase().includes(search.toLowerCase())) ||
            (asset.currentUser && asset.currentUser.toLowerCase().includes(search.toLowerCase())) ||
            (asset.lastUser && asset.lastUser.toLowerCase().includes(search.toLowerCase())) ||
            (asset.assignedTo && asset.assignedTo.toLowerCase().includes(search.toLowerCase()));
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
                    ${asset.firewallName && asset.type !== 'firewall' ? `<p><strong>Name:</strong> ${asset.firewallName}</p>` : ''}
                    ${asset.ramSize ? `<p><strong>Size:</strong> ${asset.ramSize}</p>` : ''}
                    ${asset.ramDDR ? `<p><strong>DDR:</strong> ${asset.ramDDR}</p>` : ''}
                    ${asset.ramFrequency ? `<p><strong>Frequency:</strong> ${asset.ramFrequency}</p>` : ''}
                    ${asset.model ? `<p><strong>Model:</strong> ${asset.model}</p>` : ''}
                    ${asset.currentUser ? `<p><strong>Current User:</strong> ${asset.currentUser}</p>` : (asset.type === 'laptop' ? '<p><strong>Current User:</strong> Not Assigned</p>' : '')}
                    ${asset.officeLocation ? `<p><strong>Location:</strong> ${asset.officeLocation}</p>` : ''}
                    ${asset.location ? `<p><strong>Location:</strong> ${asset.location}</p>` : ''}
                    ${asset.quantity ? `<p><strong>Quantity:</strong> ${asset.quantity}</p>` : ''}
                    ${asset.mouseType ? `<p><strong>Type:</strong> ${asset.mouseType}</p>` : ''}
                    ${asset.purchaseYear ? `<p><strong>Year:</strong> ${asset.purchaseYear}</p>` : ''}
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

// Render assignments view
function renderAssignments(search = '') {
    const container = document.getElementById('assignmentsList');
    
    const assigned = assets.filter(asset => asset.currentUser && asset.currentUser !== '');
    
    let filtered = assigned;
    if (search) {
        filtered = assigned.filter(asset => 
            asset.currentUser.toLowerCase().includes(search.toLowerCase())
        );
    }
    
    if (filtered.length === 0) {
        container.innerHTML = '<div class="empty-state"><h3>No assignments found</h3><p>Assign assets to employees to see them here</p></div>';
        return;
    }
    
    // Group by employee
    const grouped = {};
    filtered.forEach(asset => {
        if (!grouped[asset.currentUser]) {
            grouped[asset.currentUser] = [];
        }
        grouped[asset.currentUser].push(asset);
    });
    
    container.innerHTML = Object.keys(grouped).map(employee => `
        <div class="assignment-card">
            <div class="asset-info">
                <h3>${employee}</h3>
                ${grouped[employee].map(asset => `
                    <p>• ${asset.type.charAt(0).toUpperCase() + asset.type.slice(1)}: ${asset.assetId} (${asset.model})</p>
                    ${asset.lastUser ? `<p style="margin-left: 20px; font-size: 13px; color: #999;">Previous: ${asset.lastUser}</p>` : ''}
                    ${asset.accessories ? `
                        <div style="margin-left: 20px; font-size: 13px; color: #777;">
                            ${asset.accessories.mouse ? `<p>  - Mouse: ${asset.accessories.mouse}</p>` : ''}
                            ${asset.accessories.headphone ? `<p>  - Headphone: ${asset.accessories.headphone}</p>` : ''}
                            ${asset.accessories.charger ? `<p>  - Charger: ${asset.accessories.charger}</p>` : ''}
                            ${asset.accessories.monitor ? `<p>  - Monitor: ${asset.accessories.monitor}</p>` : ''}
                        </div>
                    ` : ''}
                `).join('')}
            </div>
        </div>
    `).join('');
}

// Delete asset
async function deleteAsset(id) {
    const code = prompt('Enter security code to delete:');
    if (code !== '4181') {
        alert('Invalid security code. Delete operation cancelled.');
        return;
    }
    
    if (confirm('Are you sure you want to delete this asset?')) {
        try {
            const response = await fetch(`/api/assets/${id}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                assets = assets.filter(asset => asset.id !== id);
                renderAssets();
                alert('Asset deleted successfully!');
            } else {
                alert('Failed to delete asset.');
            }
        } catch (error) {
            alert('Error deleting asset.');
        }
    }
}

// Edit asset
async function editAsset(id) {
    const code = prompt('Enter security code to edit:');
    if (code !== '4181') {
        alert('Invalid security code. Edit operation cancelled.');
        return;
    }
    
    const asset = assets.find(a => a.id === id);
    if (!asset) return;
    
    // Open Add Asset Modal for editing
    showAddAssetForm();
    
    // Populate form with asset data
    document.getElementById('assetType').value = asset.type;
    
    // Trigger the change event to show appropriate fields
    const event = new Event('change');
    document.getElementById('assetType').dispatchEvent(event);
    
    // Populate common fields
    if (asset.type !== 'mouse' && asset.type !== 'firewall') {
        document.getElementById('assetId').value = asset.assetId;
    }
    if (asset.type !== 'firewall') {
        document.getElementById('assetModel').value = asset.model || '';
    }
    document.getElementById('status').value = asset.status;
    
    // Populate laptop-specific fields
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
    
    // Populate mouse-specific fields
    if (asset.type === 'mouse') {
        document.getElementById('mouseQuantity').value = asset.quantity || '';
        document.getElementById('mouseType').value = asset.mouseType || '';
        document.getElementById('mouseLocation').value = asset.location || '';
    }
    
    // Populate firewall-specific fields
    if (asset.type === 'firewall') {
        document.getElementById('firewallName').value = asset.firewallName || '';
        document.getElementById('firewallSerial').value = asset.serialNumber || '';
        document.getElementById('firewallYear').value = asset.purchaseYear || '';
        document.getElementById('lastFirmwareUpdate').value = asset.lastFirmwareUpdate || '';
        document.getElementById('firewallLocation').value = asset.location || '';
    }
    
    // Populate RAM-specific fields
    if (asset.type === 'ram') {
        document.getElementById('ramName').value = asset.ramName || '';
        document.getElementById('ramSize').value = asset.ramSize || '';
        document.getElementById('ramDDR').value = asset.ramDDR || '';
        document.getElementById('ramFrequency').value = asset.ramFrequency || '';
        document.getElementById('ramQuantity').value = asset.quantity || '';
        document.getElementById('ramLocation').value = asset.location || '';
    }
    
    // Change form title and button
    document.querySelector('#add h2').textContent = 'Edit Asset';
    document.querySelector('#assetForm button[type="submit"]').textContent = 'Update Asset';
    
    // Store the ID being edited
    document.getElementById('assetForm').dataset.editId = id;
}

// View asset details
function viewAsset(id) {
    const asset = assets.find(a => a.id === id);
    if (!asset) return;
    
    const modal = document.getElementById('viewModal');
    const modalContent = document.getElementById('modalContent');
    
    let html = `
        <h2>${asset.type === 'firewall' && asset.firewallName ? asset.firewallName : (asset.type === 'ram' && asset.ramName ? asset.ramName : (asset.type.charAt(0).toUpperCase() + asset.type.slice(1) + ((asset.type !== 'mouse' && asset.type !== 'firewall' && asset.type !== 'ram') ? ' - ' + asset.assetId : '')))}</h2>
        <div class="modal-details">
            <div class="detail-section">
                <h3>Basic Information</h3>
                <p><strong>Asset Type:</strong> ${asset.type.charAt(0).toUpperCase() + asset.type.slice(1)}</p>
                ${(asset.type !== 'mouse' && asset.type !== 'firewall' && asset.type !== 'ram') ? `<p><strong>Asset ID:</strong> ${asset.assetId}</p>` : ''}
                ${asset.firewallName && asset.type === 'firewall' ? `<p><strong>Firewall Name:</strong> ${asset.firewallName}</p>` : ''}
                ${asset.ramName ? `<p><strong>RAM Name:</strong> ${asset.ramName}</p>` : ''}
                ${asset.ramSize ? `<p><strong>Size:</strong> ${asset.ramSize}</p>` : ''}
                ${asset.ramDDR ? `<p><strong>DDR Type:</strong> ${asset.ramDDR}</p>` : ''}
                ${asset.ramFrequency ? `<p><strong>Frequency:</strong> ${asset.ramFrequency}</p>` : ''}
                ${asset.model ? `<p><strong>Model:</strong> ${asset.model}</p>` : ''}
                ${asset.serialNumber ? `<p><strong>Serial Number:</strong> ${asset.serialNumber}</p>` : ''}
                ${asset.configuration ? `<p><strong>Configuration:</strong> ${asset.configuration}</p>` : ''}
                ${asset.quantity ? `<p><strong>Quantity:</strong> ${asset.quantity}</p>` : ''}
                ${asset.mouseType ? `<p><strong>Type:</strong> ${asset.mouseType}</p>` : ''}
                ${asset.purchaseYear ? `<p><strong>Purchase Year:</strong> ${asset.purchaseYear}</p>` : ''}
                ${asset.lastFirmwareUpdate ? `<p><strong>Last Firmware Update:</strong> ${asset.lastFirmwareUpdate}</p>` : ''}
                ${asset.location ? `<p><strong>Location:</strong> ${asset.location}</p>` : ''}
                ${asset.officeLocation ? `<p><strong>Office Location:</strong> ${asset.officeLocation}</p>` : ''}
                ${asset.year ? `<p><strong>Year:</strong> ${asset.year}</p>` : ''}
                ${asset.currentCondition ? `<p><strong>Current Condition:</strong> ${asset.currentCondition}</p>` : ''}
                <p><strong>Status:</strong> <span class="status-badge status-${asset.status}">${asset.status}</span></p>
            </div>
            
            ${(asset.type !== 'mouse' && asset.type !== 'firewall') ? `
            <div class="detail-section">
                <h3>Assignment Information</h3>
                ${asset.currentUser ? `<p><strong>Current User:</strong> ${asset.currentUser}</p>` : '<p><strong>Current User:</strong> Not Assigned</p>'}
                ${asset.lastUser ? `<p><strong>Last User:</strong> ${asset.lastUser}</p>` : ''}
            </div>
            ` : ''}
    `;
    
    if (asset.accessories) {
        html += `
            <div class="detail-section">
                <h3>Accessories</h3>
                ${asset.accessories.mouse ? `<p><strong>Mouse:</strong> ${asset.accessories.mouse}</p>` : ''}
                ${asset.accessories.headphone ? `<p><strong>Headphone:</strong> ${asset.accessories.headphone}</p>` : ''}
                ${asset.accessories.charger ? `<p><strong>Charger:</strong> ${asset.accessories.charger}</p>` : ''}
                ${asset.accessories.monitor ? `<p><strong>Monitor:</strong> ${asset.accessories.monitor}</p>` : ''}
            </div>
        `;
    }
    
    html += '</div>';
    modalContent.innerHTML = html;
    modal.style.display = 'flex';
}

// Close modal
function closeModal() {
    document.getElementById('viewModal').style.display = 'none';
}

// Filters
document.getElementById('categoryFilter').addEventListener('change', (e) => {
    const statusFilter = document.getElementById('statusFilter').value;
    const officeFilter = document.getElementById('officeFilter').value;
    const search = document.getElementById('searchAsset').value;
    renderAssets(e.target.value, statusFilter, officeFilter, search);
});

document.getElementById('statusFilter').addEventListener('change', (e) => {
    const categoryFilter = document.getElementById('categoryFilter').value;
    const officeFilter = document.getElementById('officeFilter').value;
    const search = document.getElementById('searchAsset').value;
    renderAssets(categoryFilter, e.target.value, officeFilter, search);
});

document.getElementById('officeFilter').addEventListener('change', (e) => {
    const categoryFilter = document.getElementById('categoryFilter').value;
    const statusFilter = document.getElementById('statusFilter').value;
    const search = document.getElementById('searchAsset').value;
    renderAssets(categoryFilter, statusFilter, e.target.value, search);
});

document.getElementById('searchAsset').addEventListener('input', (e) => {
    const categoryFilter = document.getElementById('categoryFilter').value;
    const statusFilter = document.getElementById('statusFilter').value;
    const officeFilter = document.getElementById('officeFilter').value;
    renderAssets(categoryFilter, statusFilter, officeFilter, e.target.value);
});

document.getElementById('searchEmployee').addEventListener('input', (e) => {
    renderAssignments(e.target.value);
});

// Initial render - only if logged in
if (isLoggedIn) {
    loadAssets().then(() => {
        renderAssets();
    });
}
