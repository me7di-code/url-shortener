const API_BASE = 'http://127.0.0.1:8000';

// DOM Elements
const form = document.getElementById('shorten-form');
const urlInput = document.getElementById('url-input');
const formMessage = document.getElementById('form-message');
const linksContainer = document.getElementById('links-container');
const emptyState = document.getElementById('empty-state');
const refreshBtn = document.getElementById('refresh-btn');
const toast = document.getElementById('toast');

// Event Listeners
form.addEventListener('submit', handleShorten);
refreshBtn.addEventListener('click', fetchLinks);

// Initial Load
fetchLinks();

// API Functions
async function fetchLinks() {
    refreshBtn.classList.add('spinning'); // Add animation if desired
    try {
        const response = await fetch(`${API_BASE}/all`);
        if (!response.ok) throw new Error('Failed to fetch links');
        
        const links = await response.json();
        renderLinks(links);
    } catch (error) {
        console.error('Error fetching links:', error);
        showToast('Failed to load links', 'error');
    } finally {
        refreshBtn.classList.remove('spinning');
    }
}

async function handleShorten(e) {
    e.preventDefault();
    const url = urlInput.value.trim();
    if (!url) return;

    // Optional: Add https:// if no scheme is provided, though backend handles some of this
    let finalUrl = url;
    if (!finalUrl.startsWith('http://') && !finalUrl.startsWith('https://')) {
        finalUrl = 'https://' + finalUrl;
    }

    try {
        const response = await fetch(`${API_BASE}/shorten`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: finalUrl })
        });
        
        const data = await response.json();
        
        if (typeof data === 'string') {
            // Backend returns string message if already assigned or error
            showMessage(data, 'error');
        } else {
            // Success
            showMessage('URL successfully shortened!', 'success');
            urlInput.value = '';
            fetchLinks(); // Refresh list
        }
    } catch (error) {
        showMessage('Error connecting to server', 'error');
    }
}

async function updateCode(code) {
    try {
        const response = await fetch(`${API_BASE}/update/${code}`, {
            method: 'POST'
        });
        const data = await response.json();
        if (typeof data === 'string') {
            showToast(data, 'error');
        } else {
            showToast('Code regenerated', 'success');
            fetchLinks(); // Refresh list
        }
    } catch (error) {
        showToast('Error updating code', 'error');
    }
}

async function deleteLink(code) {
    if (!confirm('Are you sure you want to delete this link?')) return;
    
    try {
        const response = await fetch(`${API_BASE}/delete/${code}`, {
            method: 'DELETE'
        });
        const data = await response.json();
        showToast(data, 'success');
        fetchLinks(); // Refresh list
    } catch (error) {
        showToast('Error deleting link', 'error');
    }
}

// UI Functions
function renderLinks(links) {
    if (!links || links.length === 0) {
        linksContainer.innerHTML = '';
        emptyState.classList.remove('hidden');
        return;
    }

    emptyState.classList.add('hidden');
    linksContainer.innerHTML = '';

    // Sort by created date descending
    links.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));

    links.forEach(link => {
        const card = document.createElement('div');
        card.className = 'link-card';
        
        const shortUrl = `${API_BASE}/${link.code}`;
        const createdDate = new Date(link.createdAt).toLocaleDateString(undefined, {
            month: 'short', day: 'numeric', year: 'numeric'
        });

        card.innerHTML = `
            <div class="card-header">
                <div class="short-code">
                    ${link.code}
                    <button class="copy-btn" onclick="copyToClipboard('${shortUrl}')" title="Copy link">
                        <i class="ph ph-copy"></i>
                    </button>
                </div>
                <div class="card-actions">
                    <button class="action-btn" onclick="updateCode('${link.code}')" title="Regenerate code">
                        <i class="ph ph-arrows-clockwise"></i>
                    </button>
                    <button class="action-btn delete" onclick="deleteLink('${link.code}')" title="Delete link">
                        <i class="ph ph-trash"></i>
                    </button>
                </div>
            </div>
            <a href="${link.url}" target="_blank" class="original-url" title="${link.url}">
                ${link.url}
            </a>
            <div class="card-stats">
                <div class="stat-item">
                    <i class="ph ph-calendar-blank"></i>
                    ${createdDate}
                </div>
                <div class="stat-item">
                    <i class="ph ph-cursor-click"></i>
                    ${link.clickCount} clicks
                </div>
            </div>
        `;
        linksContainer.appendChild(card);
    });
}

function showMessage(msg, type) {
    formMessage.textContent = msg;
    formMessage.className = `message ${type}`;
    formMessage.classList.remove('hidden');
    
    // Auto hide after 3 seconds
    setTimeout(() => {
        formMessage.classList.add('hidden');
    }, 3000);
}

function showToast(msg, type = 'success') {
    const toastMsg = toast.querySelector('.toast-message');
    const toastIcon = toast.querySelector('.toast-icon');
    
    toastMsg.textContent = msg;
    
    if (type === 'error') {
        toastIcon.className = 'ph ph-warning-circle toast-icon';
        toastIcon.style.color = 'var(--danger)';
    } else {
        toastIcon.className = 'ph ph-check-circle toast-icon';
        toastIcon.style.color = 'var(--success)';
    }
    
    toast.classList.remove('hidden');
    
    setTimeout(() => {
        toast.classList.add('hidden');
    }, 3000);
}

async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showToast('Link copied to clipboard!');
    } catch (err) {
        // Fallback for older browsers
        const textArea = document.createElement("textarea");
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            showToast('Link copied to clipboard!');
        } catch (err) {
            showToast('Failed to copy', 'error');
        }
        document.body.removeChild(textArea);
    }
}
