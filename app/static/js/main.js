let selectedFile = null;
let currentFolder = ''; // '' = Raíz global, 'libreria' = subcarpeta modular

// 1. Cargar lista de archivos y subcarpetas desde disco
async function loadFiles() {
    try {
        const url = `/api/files/?folder=${encodeURIComponent(currentFolder)}`;
        const res = await fetch(url);
        const data = await res.json();
        
        // Actualizar selector de subcarpetas en la barra superior
        updateFolderSelect(data.folders || []);

        const list = document.getElementById('filesList');
        list.innerHTML = '';
        if (!data.files || data.files.length === 0) {
            list.innerHTML = `<li style="padding:10px; color:#64748b;">(No hay archivos en ${currentFolder ? currentFolder + '/' : 'la carpeta raíz'})</li>`;
            return;
        }
        data.files.forEach(f => {
            const li = document.createElement('li');
            li.className = 'file-item' + (f === selectedFile ? ' active' : '');
            
            let icon = '📄 ';
            if (f.endsWith('.json')) icon = '📊 ';
            else if (f.endsWith('.html')) icon = '🌐 ';
            else if (f.endsWith('.py')) icon = '🐍 ';
            else if (f.endsWith('.pdf')) icon = '📕 ';
            
            li.innerText = icon + f;
            li.onclick = () => selectFile(f);
            list.appendChild(li);
        });
    } catch (err) {
        console.error("Error al cargar archivos:", err);
    }
}

// Actualizar las opciones del dropdown de carpetas
function updateFolderSelect(folders) {
    const select = document.getElementById('folderSelect');
    if (!select) return;
    
    const previousVal = currentFolder;
    select.innerHTML = '<option value="">📂 Raíz Global (files_storage/)</option>';
    
    folders.forEach(f => {
        const opt = document.createElement('option');
        opt.value = f;
        opt.innerText = `📁 ${f}/`;
        if (f === previousVal) opt.selected = true;
        select.appendChild(opt);
    });
}

// Cambiar de carpeta/módulo de trabajo activo
function changeFolder(folder) {
    currentFolder = folder.trim();
    deselectFile();
    loadFiles();
    loadHistory();
}

// Crear nueva subcarpeta / módulo modular
async function createSubfolderPrompt() {
    const folderName = prompt("Ingresa el nombre del nuevo módulo/subcarpeta (ej: libreria, presupuestos, contabilidad):");
    if (!folderName) return;
    const cleanName = folderName.trim().replace(/[\/\\]/g, '');
    if (!cleanName) return alert("Nombre de subcarpeta inválido.");
    
    const desc = prompt("Descripción del módulo (opcional):", `Módulo ${cleanName}`) || `Módulo ${cleanName}`;

    try {
        const res = await fetch('/api/folders/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({folder_name: cleanName, description: desc})
        });
        const data = await res.json();
        alert(data.message || 'Módulo creado exitosamente.');
        changeFolder(cleanName);
    } catch (err) {
        alert("Error al crear subcarpeta: " + err.message);
    }
}

// 2. Seleccionar un archivo para ver/editar (soporta texto y PDFs nativos)
async function selectFile(filename) {
    selectedFile = filename;
    const isPdf = filename.toLowerCase().endsWith('.pdf');
    document.getElementById('currentFileTitle').innerText = (isPdf ? '📕 Visor PDF: ' : '📝 Editando: ') + filename;
    
    const editor = document.getElementById('fileEditor');
    const pdfViewer = document.getElementById('pdfViewer');
    const downloadBtn = document.getElementById('downloadPdfBtn');
    const saveBtn = document.getElementById('saveBtn');

    if (isPdf) {
        // Modo Visor PDF embebido
        editor.style.display = 'none';
        pdfViewer.style.display = 'block';
        pdfViewer.src = `/api/files/raw/?filename=${encodeURIComponent(filename)}`;
        downloadBtn.style.display = 'inline-block';
        downloadBtn.href = `/api/files/raw/?filename=${encodeURIComponent(filename)}`;
        if (saveBtn) saveBtn.style.display = 'none';
    } else {
        // Modo Editor de Texto / Markdown / JSON / Python / HTML
        pdfViewer.style.display = 'none';
        pdfViewer.src = '';
        editor.style.display = 'block';
        
        const isHtml = filename.toLowerCase().endsWith('.html');
        if (isHtml) {
            downloadBtn.style.display = 'inline-block';
            downloadBtn.innerText = '↗ Abrir Presentación / Web';
            downloadBtn.href = `/api/files/raw/?filename=${encodeURIComponent(filename)}`;
        } else {
            downloadBtn.style.display = 'none';
            downloadBtn.innerText = '↗ Abrir';
        }
        
        if (saveBtn) saveBtn.style.display = 'block';
        
        try {
            const res = await fetch(`/api/files/?filename=${encodeURIComponent(filename)}`);
            const data = await res.json();
            editor.value = data.content || '';
        } catch (err) {
            console.error("Error al leer archivo:", err);
        }
    }
    loadFiles();
}

// 3. Deseleccionar archivo para volver a modo consulta global
function deselectFile() {
    selectedFile = null;
    document.getElementById('currentFileTitle').innerText = '📝 Visor / Editor';
    const editor = document.getElementById('fileEditor');
    const pdfViewer = document.getElementById('pdfViewer');
    const downloadBtn = document.getElementById('downloadPdfBtn');
    const saveBtn = document.getElementById('saveBtn');
    
    editor.style.display = 'block';
    editor.value = '';
    pdfViewer.style.display = 'none';
    pdfViewer.src = '';
    downloadBtn.style.display = 'none';
    if (saveBtn) saveBtn.style.display = 'block';
    loadFiles();
}

// 4. Guardar cambios manuales en el archivo
async function saveFile() {
    if (!selectedFile) return alert('Por favor selecciona o crea un archivo primero.');
    const content = document.getElementById('fileEditor').value;
    const res = await fetch('/api/files/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({filename: selectedFile, content, folder: currentFolder})
    });
    const data = await res.json();
    alert(data.message || 'Guardado exitoso');
    loadFiles();
}

// 5. Crear un nuevo archivo o ruta manualmente
async function createFile() {
    const input = document.getElementById('newFilename');
    let filename = input.value.trim();
    if (!filename) return alert('Ingresa un nombre o ruta de archivo.');
    
    await fetch('/api/files/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({filename, content: '', folder: currentFolder})
    });
    input.value = '';
    await loadFiles();
    selectFile(currentFolder && !filename.includes('/') ? `${currentFolder}/${filename}` : filename);
}

// 6. Eliminar el archivo actual
async function deleteFile() {
    if (!selectedFile) return alert('No hay ningún archivo seleccionado.');
    if (!confirm(`¿Estás seguro de eliminar '${selectedFile}'?`)) return;
    await fetch('/api/files/', {
        method: 'DELETE',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({filename: selectedFile, folder: currentFolder})
    });
    deselectFile();
    loadFiles();
}

// 7. Cargar Historial Persistente del Servidor (aislado por ámbito de carpeta)
async function loadHistory() {
    try {
        const url = `/api/history/?folder=${encodeURIComponent(currentFolder)}`;
        const res = await fetch(url);
        const data = await res.json();
        renderHistoryView(data.history || []);
    } catch (err) {
        console.error("Error al cargar historial:", err);
    }
}

function formatMarkdown(text) {
    if (typeof marked !== 'undefined' && marked.parse) {
        return marked.parse(text);
    }
    return text.replace(/\n/g, '<br>');
}

function renderHistoryView(history) {
    const output = document.getElementById('aiOutput');
    if (!history || history.length === 0) {
        const scopeLabel = currentFolder ? `en el módulo '${currentFolder}/'` : 'en la raíz';
        output.innerHTML = `<div class="chat-placeholder">Historial limpio ${scopeLabel}. Escribe una consulta o instrucción para comenzar.</div>`;
        return;
    }
    
    output.innerHTML = '';
    history.forEach(item => {
        const msgDiv = document.createElement('div');
        msgDiv.className = `chat-message ${item.role}`;
        
        const authorDiv = document.createElement('div');
        authorDiv.className = `chat-author ${item.role}`;
        authorDiv.innerText = item.role === 'user' ? '👤 Usuario' : '🤖 Agente Claude';
        msgDiv.appendChild(authorDiv);
        
        if (item.actions && item.actions.length > 0) {
            const actionsBadge = document.createElement('div');
            actionsBadge.className = 'chat-actions-badge';
            actionsBadge.innerHTML = '<strong>⚡ Acciones en disco / memoria:</strong><ul>' + 
                item.actions.map(a => `<li>${a}</li>`).join('') + '</ul>';
            msgDiv.appendChild(actionsBadge);
        }
        
        const bodyDiv = document.createElement('div');
        bodyDiv.className = 'chat-body';
        bodyDiv.innerHTML = formatMarkdown(item.content || '');
        msgDiv.appendChild(bodyDiv);
        
        output.appendChild(msgDiv);
    });
    
    output.scrollTop = output.scrollHeight;
}

// 8. Consultar al Agente con Ámbito Modular, Memoria Continua y Tool Calling
async function askAI() {
    const input = document.getElementById('aiPrompt');
    const prompt = input.value.trim();
    if (!prompt) return alert('Escribe una consulta, lineamiento o instrucción para el agente.');
    
    const output = document.getElementById('aiOutput');
    
    if (output.querySelector('.chat-placeholder')) {
        output.innerHTML = '';
    }
    
    const userMsg = document.createElement('div');
    userMsg.className = 'chat-message user';
    userMsg.innerHTML = `<div class="chat-author user">👤 Usuario</div><div class="chat-body">${formatMarkdown(prompt)}</div>`;
    output.appendChild(userMsg);
    
    const loadingMsg = document.createElement('div');
    loadingMsg.className = 'chat-message assistant temp-loading';
    const scopeLabel = currentFolder ? `módulo ${currentFolder}/` : 'raíz';
    loadingMsg.innerHTML = `<div class="chat-author assistant">🤖 Agente Claude</div><div class="chat-body"><em>⏳ Procesando en ${scopeLabel}, consultando memoria local y ejecutando herramientas...</em></div>`;
    output.appendChild(loadingMsg);
    output.scrollTop = output.scrollHeight;
    input.value = '';
    
    try {
        const res = await fetch('/api/ai-chat/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                prompt: prompt,
                filename: selectedFile,
                folder: currentFolder
            })
        });
        
        let data;
        const rawText = await res.text();
        try {
            data = JSON.parse(rawText);
        } catch (e) {
            throw new Error(`Error en el servidor (${res.status}): ${rawText.slice(0, 120)}`);
        }
        
        if (data.status === 'ok') {
            await loadHistory();
            await loadFiles();
            if (selectedFile) {
                await selectFile(selectedFile);
            }
        } else {
            loadingMsg.innerHTML = `<div class="chat-author assistant" style="color:#ef4444;">❌ Error del Agente</div><div class="chat-body" style="color:#fca5a5;">${data.error || 'Ocurrió un error inesperado.'}</div>`;
        }
    } catch (err) {
        loadingMsg.innerHTML = `<div class="chat-author assistant" style="color:#ef4444;">❌ Error de conexión</div><div class="chat-body" style="color:#fca5a5;">${err.message}</div>`;
    }
}

// 9. Limpiar solo la ventana visual (pantalla)
function clearWindow() {
    const output = document.getElementById('aiOutput');
    const scopeLabel = currentFolder ? `en '${currentFolder}/'` : 'en la raíz';
    output.innerHTML = `<div class="chat-placeholder">Ventana visual limpiada (${scopeLabel}).</div>`;
    document.getElementById('aiPrompt').value = '';
}

// 10. Borrar historial completo persistente del servidor para la carpeta activa
async function clearFullHistory() {
    const scopeLabel = currentFolder ? `del módulo '${currentFolder}/'` : 'de la raíz';
    if (!confirm(`¿Deseas eliminar permanentemente el historial de conversaciones ${scopeLabel}?`)) return;
    try {
        const res = await fetch('/api/history/', {
            method: 'DELETE',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({folder: currentFolder})
        });
        const data = await res.json();
        clearWindow();
        alert(data.message || 'Historial borrado al completo.');
    } catch (err) {
        alert('Error al borrar historial: ' + err.message);
    }
}

// 11. Expandir y contraer paneles a pantalla completa
function toggleExpand(panelId) {
    const panel = document.getElementById(panelId);
    if (!panel) return;
    const isFull = panel.classList.toggle('fullscreen');
    const btn = panel.querySelector('.btn-expand');
    if (btn) {
        btn.innerText = isFull ? '🗗' : '⛶';
        btn.title = isFull ? 'Contraer a tamaño normal' : 'Expandir a pantalla completa';
    }
}

// 12. Enviar con tecla Enter (Shift+Enter para salto de línea)
const promptInput = document.getElementById('aiPrompt');
if (promptInput) {
    promptInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            askAI();
        }
    });
}

// Cargar estado inicial
loadFiles();
loadHistory();





