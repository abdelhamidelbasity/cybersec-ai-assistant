// ===== DOM References =====
const chatContainer = document.getElementById('chatContainer');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');

marked.setOptions({ gfm: true, breaks: true });

// ===== Theme Toggle =====
function initTheme() {
    const saved = localStorage.getItem('cyberguard-theme') || 'dark';
    document.documentElement.setAttribute('data-theme', saved);
    updateThemeIcon(saved);
}
function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('cyberguard-theme', next);
    updateThemeIcon(next);
}
function updateThemeIcon(theme) {
    const icon = document.getElementById('themeIcon');
    if (icon) icon.className = theme === 'dark' ? 'fa-solid fa-moon' : 'fa-solid fa-sun';
}
document.getElementById('themeToggle').addEventListener('click', toggleTheme);
initTheme();

// ===== Sidebar Toggle (mobile) =====
document.getElementById('sidebarToggle').addEventListener('click', () => {
    document.getElementById('sidebar').classList.toggle('open');
});

// ===== Panel Switching =====
function switchPanel(name, el) {
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    const panel = document.getElementById('panel-' + name);
    if (panel) panel.classList.add('active');
    if (el) el.classList.add('active');
    // Auto-load data for panels
    if (name === 'files') loadFiles();
    if (name === 'history') renderHistory();
    if (name === 'settings') loadSettings();
    // Close sidebar on mobile
    document.getElementById('sidebar').classList.remove('open');
}

// ===== Toast Notifications =====
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = 'toast ' + type;
    const icons = { success: 'fa-circle-check', error: 'fa-circle-xmark', info: 'fa-circle-info' };
    toast.innerHTML = `<i class="fa-solid ${icons[type] || icons.info}"></i><span>${message}</span>`;
    container.appendChild(toast);
    setTimeout(() => { toast.style.animation = 'toastOut 0.4s ease forwards'; setTimeout(() => toast.remove(), 400); }, 3500);
}

// ===== Chat Functions =====
function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = (textarea.scrollHeight < 200 ? textarea.scrollHeight : 200) + 'px';
}
function checkSubmit(e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
}

function appendMessage(role, content, sources = []) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${role}-message`;
    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.innerHTML = role === 'ai' ? '<i class="fa-solid fa-robot"></i>' : '<i class="fa-solid fa-user"></i>';
    msgDiv.appendChild(avatar);
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    msgDiv.appendChild(contentDiv);

    if (content === 'loading') {
        contentDiv.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';
        msgDiv.id = 'loadingMessage';
    } else {
        contentDiv.innerHTML = role === 'ai' ? marked.parse(content) : `<p>${content}</p>`;
        if (role === 'ai' && sources && sources.length > 0) {
            const sourceDiv = document.createElement('div');
            sourceDiv.className = 'rag-sources';
            let html = '<strong><i class="fa-solid fa-book-bookmark"></i> Sourced Context:</strong><ul>';
            sources.forEach(s => { html += `<li>${s.split('\\').pop().split('/').pop()}</li>`; });
            html += '</ul>';
            sourceDiv.innerHTML = html;
            contentDiv.appendChild(sourceDiv);
        }
    }
    chatContainer.appendChild(msgDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function removeLoading() {
    const el = document.getElementById('loadingMessage');
    if (el) el.remove();
}

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;
    userInput.value = '';
    userInput.style.height = 'auto';
    sendBtn.disabled = true;
    appendMessage('user', text);
    appendMessage('ai', 'loading');
    try {
        const res = await fetch('/api/chat', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });
        const data = await res.json();
        removeLoading();
        if (data.error) {
            appendMessage('ai', `**Error:** ${data.answer}`);
        } else {
            appendMessage('ai', data.answer, data.sources);
        }
    } catch (err) {
        removeLoading();
        appendMessage('ai', '**Network Error:** Cannot reach the local RAG subsystem.');
    }
    sendBtn.disabled = false;
    userInput.focus();
}

function clearMessages() {
    const genesis = document.querySelector('.genesis-message');
    chatContainer.innerHTML = '';
    if (genesis) chatContainer.appendChild(genesis);
    showToast('Chat cleared', 'info');
}

// ===== Chat History =====
function getChatHistory() {
    return JSON.parse(localStorage.getItem('cyberguard-history') || '[]');
}
function saveChatHistory(history) {
    localStorage.setItem('cyberguard-history', JSON.stringify(history));
}

function saveCurrentChat() {
    const messages = chatContainer.querySelectorAll('.message:not(.genesis-message)');
    if (messages.length === 0) { showToast('No messages to save', 'error'); return; }
    const chatData = [];
    messages.forEach(m => {
        const role = m.classList.contains('user-message') ? 'user' : 'ai';
        const content = m.querySelector('.message-content').innerText;
        chatData.push({ role, content: content.substring(0, 500) });
    });
    const firstMsg = chatData.find(m => m.role === 'user');
    const title = firstMsg ? firstMsg.content.substring(0, 60) + (firstMsg.content.length > 60 ? '...' : '') : 'Untitled Chat';
    const entry = {
        id: Date.now(),
        title: title,
        date: new Date().toLocaleString(),
        messages: chatData
    };
    const history = getChatHistory();
    history.unshift(entry);
    if (history.length > 50) history.pop();
    saveChatHistory(history);
    showToast('Chat saved to history', 'success');
}

function renderHistory() {
    const list = document.getElementById('historyList');
    const history = getChatHistory();
    if (history.length === 0) {
        list.innerHTML = '<div class="files-empty"><i class="fa-solid fa-inbox"></i><p>No saved chats yet.</p></div>';
        return;
    }
    list.innerHTML = '';
    history.forEach((entry, idx) => {
        const item = document.createElement('div');
        item.className = 'history-item';
        item.innerHTML = `
            <div class="history-icon"><i class="fa-solid fa-message"></i></div>
            <div class="history-info" onclick="restoreChat(${idx})">
                <h4>${entry.title}</h4>
                <span>${entry.date} &mdash; ${entry.messages.length} messages</span>
            </div>
            <button class="history-delete" onclick="event.stopPropagation();deleteHistory(${idx})"><i class="fa-solid fa-xmark"></i></button>`;
        list.appendChild(item);
    });
}

function restoreChat(idx) {
    const history = getChatHistory();
    const entry = history[idx];
    if (!entry) return;
    clearMessages();
    entry.messages.forEach(m => appendMessage(m.role, m.content));
    switchPanel('chat', document.querySelector('[data-panel="chat"]'));
    showToast('Chat restored', 'success');
}

function deleteHistory(idx) {
    const history = getChatHistory();
    history.splice(idx, 1);
    saveChatHistory(history);
    renderHistory();
    showToast('Chat deleted', 'info');
}

function clearAllHistory() {
    localStorage.removeItem('cyberguard-history');
    renderHistory();
    showToast('All history cleared', 'info');
}

// ===== File Upload =====
const uploadZone = document.getElementById('uploadZone');
const fileInput = document.getElementById('fileInput');

uploadZone.addEventListener('dragover', e => { e.preventDefault(); uploadZone.classList.add('dragover'); });
uploadZone.addEventListener('dragleave', () => uploadZone.classList.remove('dragover'));
uploadZone.addEventListener('drop', e => {
    e.preventDefault();
    uploadZone.classList.remove('dragover');
    if (e.dataTransfer.files.length) uploadFiles(e.dataTransfer.files);
});
uploadZone.addEventListener('click', e => {
    if (e.target.tagName !== 'BUTTON' && e.target.tagName !== 'INPUT') fileInput.click();
});
fileInput.addEventListener('change', () => { if (fileInput.files.length) uploadFiles(fileInput.files); });

async function uploadFiles(files) {
    const progressEl = document.getElementById('uploadProgress');
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');
    
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        progressEl.style.display = 'block';
        progressFill.style.width = '30%';
        progressText.textContent = `Uploading "${file.name}"...`;
        
        const formData = new FormData();
        formData.append('file', file);
        try {
            progressFill.style.width = '60%';
            progressText.textContent = `Ingesting "${file.name}" into RAG...`;
            const res = await fetch('/api/upload', { method: 'POST', body: formData });
            const data = await res.json();
            progressFill.style.width = '100%';
            if (data.success) {
                showToast(data.message, 'success');
            } else {
                showToast(data.message, 'error');
            }
        } catch (err) {
            showToast('Upload failed: ' + err.message, 'error');
        }
    }
    setTimeout(() => { progressEl.style.display = 'none'; progressFill.style.width = '0%'; }, 1500);
    fileInput.value = '';
    loadFiles();
}

// ===== Files List =====
async function loadFiles() {
    try {
        const res = await fetch('/api/files');
        const data = await res.json();
        const list = document.getElementById('filesList');
        const badge = document.getElementById('fileCountBadge');
        
        badge.textContent = data.count;
        badge.style.display = data.count > 0 ? 'inline' : 'none';

        if (data.files.length === 0) {
            list.innerHTML = '<div class="files-empty"><i class="fa-solid fa-file-circle-question"></i><p>No documents found. Upload some files to get started.</p></div>';
            return;
        }
        list.innerHTML = '';
        data.files.forEach(f => {
            const ext = f.name.split('.').pop().toLowerCase();
            const icon = ext === 'pdf' ? 'fa-file-pdf' : 'fa-file-lines';
            const item = document.createElement('div');
            item.className = 'file-item';
            item.innerHTML = `
                <div class="file-icon"><i class="fa-solid ${icon}"></i></div>
                <div class="file-info"><h4>${f.name}</h4><span>${f.size_display}</span></div>
                <div class="file-actions">
                    <a href="/api/files/download/${encodeURIComponent(f.name)}" class="file-action-btn" title="Download"><i class="fa-solid fa-download"></i></a>
                    <button class="file-action-btn delete" title="Delete" onclick="deleteFile('${f.name}')"><i class="fa-solid fa-trash"></i></button>
                </div>`;
            list.appendChild(item);
        });
    } catch (err) {
        console.error('Failed to load files:', err);
    }
}

async function deleteFile(name) {
    if (!confirm(`Delete "${name}"? This won't remove it from the existing vector database.`)) return;
    try {
        const res = await fetch('/api/files/delete', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filename: name })
        });
        const data = await res.json();
        showToast(data.message, data.success ? 'success' : 'error');
        loadFiles();
    } catch (err) {
        showToast('Delete failed', 'error');
    }
}

// ===== Settings =====
async function loadSettings() {
    try {
        const res = await fetch('/api/settings');
        const s = await res.json();
        document.getElementById('tempSlider').value = s.temperature;
        document.getElementById('tempValue').textContent = s.temperature;
        document.getElementById('kSlider').value = s.k;
        document.getElementById('kValue').textContent = s.k;
    } catch (err) { console.error('Failed to load settings'); }
}

async function saveSettings() {
    const temp = parseFloat(document.getElementById('tempSlider').value);
    const k = parseInt(document.getElementById('kSlider').value);
    try {
        const res = await fetch('/api/settings', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ temperature: temp, k: k })
        });
        const data = await res.json();
        if (data.success) showToast('Settings saved', 'success');
    } catch (err) {
        showToast('Failed to save settings', 'error');
    }
}

// ===== RAG Ingestion =====
async function ingestAllDocuments() {
    const btn = document.getElementById('ingestBtn');
    const originalHTML = btn.innerHTML;
    btn.disabled = true;
    btn.classList.add('processing');
    btn.innerHTML = '<i class="fa-solid fa-spinner"></i><div><strong>Processing documents...</strong><span>Loading, splitting, embedding — this may take a minute...</span></div>';

    try {
        const res = await fetch('/api/ingest', { method: 'POST' });
        const data = await res.json();
        if (data.success) {
            showToast(data.message, 'success');
        } else {
            showToast(data.message, 'error');
        }
    } catch (err) {
        showToast('Ingestion failed: ' + err.message, 'error');
    }

    btn.disabled = false;
    btn.classList.remove('processing');
    btn.innerHTML = originalHTML;
}

// ===== Init =====
userInput.focus();
loadFiles();
