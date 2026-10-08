import json
import os
import re
from pathlib import Path
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, FileResponse, Http404, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
import anthropic

STORAGE_DIR = Path(settings.STORAGE_DIR)
STORAGE_DIR.mkdir(exist_ok=True)

MAX_HISTORY_MESSAGES = 10

def get_subfolders():
    """Retorna lista de subcarpetas relativas dentro de files_storage/"""
    folders = []
    for p in sorted(STORAGE_DIR.iterdir()):
        if p.is_dir() and not p.name.startswith('.'):
            folders.append(p.name)
    return folders

def init_subfolder(folder_name, description="Módulo / Subcarpeta aislada"):
    """Inicializa una subcarpeta con su propio INDEX.md y MEMORY.md, y la registra en el INDEX.md raíz"""
    fdir = STORAGE_DIR / folder_name
    fdir.mkdir(parents=True, exist_ok=True)
    
    # 1. INDEX.md local de la subcarpeta
    local_index = fdir / 'INDEX.md'
    if not local_index.exists():
        local_index.write_text(
            f"# 🗂️ Índice del Módulo: `{folder_name}/`\n\n"
            f"> {description}. Catálogo local de archivos e instrucciones específicas de este módulo.\n\n"
            f"## 📋 Catálogo de Archivos de `{folder_name}/`\n\n"
            f"| Archivo | Temas y Palabras Clave | Resumen del Contenido | Cuándo Consultar |\n"
            f"| :--- | :--- | :--- | :--- |\n"
            f"| `INDEX.md` | `indice`, `catalogo`, `modulo` | Catálogo local de {folder_name} | Al buscar archivos de este módulo |\n"
            f"| `MEMORY.md` | `memoria`, `lineamientos`, `reglas` | Memoria y reglas específicas de {folder_name} | Al consultar acuerdos de este módulo |\n\n"
            f"## 🏷️ Reglas del Módulo\n- Los archivos aquí creados son autónomos y mantienen este índice al día.\n",
            encoding='utf-8'
        )
    
    # 2. MEMORY.md local de la subcarpeta
    local_memory = fdir / 'MEMORY.md'
    if not local_memory.exists():
        local_memory.write_text(
            f"# 🧠 Memoria y Lineamientos del Módulo: `{folder_name}/`\n\n"
            f"> Base de conocimiento y reglas específicas para el área de {folder_name}.\n\n"
            f"## 🎯 Objetivos y Lineamientos de {folder_name}\n"
            f"- {description}\n\n"
            f"## 📌 Decisiones y Acuerdos\n"
            f"- Módulo inicializado con aislamiento de memoria e índice.\n\n"
            f"## ⏳ Tareas Activas\n"
            f"- [ ] Definir archivos y lógica del módulo.\n",
            encoding='utf-8'
        )

    # 3. Registrar la subcarpeta en el INDEX.md Raíz como router
    update_index_entry(
        f"{folder_name}/",
        f"subcarpeta, modulo, {folder_name}",
        f"Subcarpeta modular: {description}",
        f"Al trabajar específicamente en {folder_name}/",
        target_folder=""
    )

def update_index_entry(filename, keywords, summary, when_to_use, target_folder=""):
    """Actualiza o agrega una entrada en el INDEX.md correspondiente (raíz o subcarpeta)"""
    if target_folder:
        index_file = STORAGE_DIR / target_folder / 'INDEX.md'
    elif "/" in filename:
        parts = filename.split("/", 1)
        subf = parts[0]
        fdir = STORAGE_DIR / subf
        if fdir.is_dir():
            index_file = fdir / 'INDEX.md'
            filename = parts[1] # nombre local
        else:
            index_file = STORAGE_DIR / 'INDEX.md'
    else:
        index_file = STORAGE_DIR / 'INDEX.md'

    header = (
        "# 🗂️ Índice Maestro y Router de Documentos (INDEX.md)\n\n"
        "> Catálogo semántico que la IA consulta primero para decidir qué archivos cargar antes de responder.\n\n"
        "## 📋 Catálogo Semántico de Documentos\n\n"
        "| Archivo | Temas y Palabras Clave | Resumen del Contenido | Cuándo Consultar |\n"
        "| :--- | :--- | :--- | :--- |\n"
    )
    
    if not index_file.exists():
        index_file.write_text(header + f"| `INDEX.md` | `indice`, `catalogo` | Catálogo central | Al agregar archivos |\n", encoding='utf-8')
    
    content = index_file.read_text(encoding='utf-8')
    new_row = f"| `{filename}` | `{keywords}` | {summary} | {when_to_use} |"
    
    pattern = rf"\|\s*`{re.escape(filename)}`\s*\|.*"
    if re.search(pattern, content):
        updated_content = re.sub(pattern, new_row, content)
    else:
        if "## 🏷️ Reglas" in content:
            updated_content = content.replace("## 🏷️ Reglas", f"{new_row}\n\n## 🏷️ Reglas")
        else:
            updated_content = content.rstrip() + f"\n{new_row}\n"
            
    index_file.write_text(updated_content, encoding='utf-8')

def remove_index_entry(filename, target_folder=""):
    """Elimina la fila correspondiente de INDEX.md"""
    if target_folder:
        index_file = STORAGE_DIR / target_folder / 'INDEX.md'
    elif "/" in filename:
        parts = filename.split("/", 1)
        index_file = STORAGE_DIR / parts[0] / 'INDEX.md'
        filename = parts[1]
    else:
        index_file = STORAGE_DIR / 'INDEX.md'

    if index_file.exists():
        content = index_file.read_text(encoding='utf-8')
        pattern = rf"\|\s*`{re.escape(filename)}`\s*\|.*\n?"
        updated_content = re.sub(pattern, "", content)
        index_file.write_text(updated_content, encoding='utf-8')

@login_required
def index(request):
    """Renderiza la vista principal del panel"""
    return render(request, 'index.html', {'storage_path': str(STORAGE_DIR)})

@login_required
@xframe_options_exempt
def file_raw(request):
    """Sirve archivos binarios y documentos como PDFs y páginas HTML con su MIME type para visualización en el navegador"""
    filename = request.GET.get('filename', '').strip()
    if not filename:
        raise Http404("Archivo no especificado")
    
    filepath = (STORAGE_DIR / filename).resolve()
    if not str(filepath).startswith(str(STORAGE_DIR.resolve())):
        raise Http404("Acceso no permitido")

    if filepath.exists() and filepath.is_file():
        content_type = None
        if filename.lower().endswith('.pdf'):
            content_type = 'application/pdf'
        elif filename.lower().endswith('.html'):
            content_type = 'text/html; charset=utf-8'
        response = FileResponse(open(filepath, 'rb'), content_type=content_type)
        response['Content-Disposition'] = f'inline; filename="{filepath.name}"'
        return response
    raise Http404("Archivo no encontrado")

@login_required
@csrf_exempt
def file_crud(request):
    """CRUD de archivos con soporte para carpetas/subcarpetas y filtrado por ámbito"""
    if request.method == 'GET':
        filename = request.GET.get('filename')
        folder = request.GET.get('folder', '').strip()

        if filename:
            filepath = STORAGE_DIR / filename
            if filepath.exists() and filepath.is_file():
                try:
                    content = filepath.read_text(encoding='utf-8')
                except UnicodeDecodeError:
                    content = f"[📕 Archivo binario generado: {filepath.name} ({filepath.stat().st_size} bytes). Puedes abrirlo o imprimirlo directamente desde tu carpeta local files_storage/{filename}]"
                return JsonResponse({
                    'filename': filename,
                    'content': content
                })
            return JsonResponse({'error': 'Archivo no encontrado'}, status=404)
        
        # Listar archivos según ámbito de carpeta
        files = []
        scan_dir = STORAGE_DIR / folder if folder else STORAGE_DIR
        if scan_dir.exists():
            for p in sorted(scan_dir.rglob('*')):
                if p.is_file():
                    rel_path = p.relative_to(STORAGE_DIR).as_posix()
                    files.append(rel_path)

        return JsonResponse({
            'files': files,
            'folders': get_subfolders(),
            'current_folder': folder,
            'storage_path': str(STORAGE_DIR)
        })

    data = json.loads(request.body.decode('utf-8') or '{}')
    filename = data.get('filename', '').strip()
    content = data.get('content', '')
    folder = data.get('folder', '').strip()

    if not filename:
        return JsonResponse({'error': 'Nombre de archivo requerido'}, status=400)

    # Si hay carpeta activa y el nombre no la incluye, anteponerla
    if folder and not filename.startswith(f"{folder}/"):
        full_rel_path = f"{folder}/{filename}"
    else:
        full_rel_path = filename

    filepath = STORAGE_DIR / full_rel_path

    if request.method in ['POST', 'PUT']:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content, encoding='utf-8')
        if filepath.name not in ['INDEX.md', 'MEMORY.md']:
            update_index_entry(full_rel_path, filepath.stem.replace('_', ' '), f"Documento {filepath.name}", f"Consultas sobre {filepath.name}", target_folder=folder)
        return JsonResponse({
            'status': 'ok',
            'message': f'Archivo {full_rel_path} guardado con éxito en disco.'
        })

    elif request.method == 'DELETE':
        if filepath.exists():
            filepath.unlink()
            remove_index_entry(full_rel_path, target_folder=folder)
            return JsonResponse({
                'status': 'ok',
                'message': f'Archivo {full_rel_path} eliminado correctamente.'
            })
        return JsonResponse({'error': 'Archivo no encontrado'}, status=404)

    return JsonResponse({'error': 'Método no soportado'}, status=405)

@login_required
@csrf_exempt
def folder_crud(request):
    """API para listar y crear subcarpetas modulares"""
    if request.method == 'GET':
        return JsonResponse({'folders': get_subfolders()})
    elif request.method == 'POST':
        data = json.loads(request.body.decode('utf-8') or '{}')
        folder_name = data.get('folder_name', '').strip()
        description = data.get('description', f'Subcarpeta modular {folder_name}')
        if not folder_name:
            return JsonResponse({'error': 'Nombre de subcarpeta requerido'}, status=400)
        
        init_subfolder(folder_name, description)
        return JsonResponse({
            'status': 'ok',
            'message': f'Subcarpeta {folder_name}/ creada con su propio INDEX.md y MEMORY.md.',
            'folders': get_subfolders()
        })
    return JsonResponse({'error': 'Método no soportado'}, status=405)

# Herramientas de Anthropic para ejecución real en disco y memoria modular
ANTHROPIC_TOOLS = [
    {
        "name": "write_file",
        "description": "Crea o sobreescribe un archivo físico en la carpeta activa o ruta especificada y actualiza automáticamente su INDEX.md.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "Nombre o ruta relativa del archivo (ej: catalogo.json o libreria/catalogo.json)"},
                "content": {"type": "string", "description": "Contenido completo del archivo"},
                "summary": {"type": "string", "description": "Resumen de 1 línea para el INDEX.md local"},
                "keywords": {"type": "string", "description": "Palabras clave para el índice"},
                "when_to_use": {"type": "string", "description": "Cuándo consultar este archivo"}
            },
            "required": ["filename", "content"]
        }
    },
    {
        "name": "create_subfolder",
        "description": "Crea una nueva subcarpeta modular aislada (ej: 'libreria', 'presupuestos') con su propio INDEX.md, MEMORY.md e historial de chat independiente para evitar que el proyecto crezca desordenadamente.",
        "input_schema": {
            "type": "object",
            "properties": {
                "folder_name": {"type": "string", "description": "Nombre de la subcarpeta (ej: libreria, contabilidad)"},
                "description": {"type": "string", "description": "Descripción del propósito de esta subcarpeta"}
            },
            "required": ["folder_name"]
        }
    },
    {
        "name": "read_file",
        "description": "Lee el contenido de cualquier archivo de files_storage/ o sus subcarpetas.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "Ruta relativa del archivo a leer"}
            },
            "required": ["filename"]
        }
    },
    {
        "name": "execute_script",
        "description": "Ejecuta un script de Python (.py) en files_storage/ con argumentos (ej: script_path='generar_presupuesto_pdf.py', args=['presupuesto_rossi.json', 'presupuesto_rossi.pdf']) para procesar datos, generar PDFs o reportes reales.",
        "input_schema": {
            "type": "object",
            "properties": {
                "script_path": {"type": "string", "description": "Nombre o ruta del script python a ejecutar (ej: generar_presupuesto_pdf.py)"},
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Lista de argumentos para el script (ej: ['presupuesto_rossi.json', 'presupuesto_rossi.pdf'])"
                }
            },
            "required": ["script_path"]
        }
    },
    {
        "name": "append_memory",
        "description": "Añade un nuevo lineamiento, preferencia del usuario o regla al MEMORY.md de la carpeta activa sin borrar lo existente.",
        "input_schema": {
            "type": "object",
            "properties": {
                "section": {"type": "string", "description": "Sección de la memoria (ej: 'Lineamientos Generales', 'Decisiones Tomadas', 'Reglas del Negocio')"},
                "note": {"type": "string", "description": "El lineamiento, regla o dato clave a recordar"}
            },
            "required": ["section", "note"]
        }
    },
    {
        "name": "update_memory",
        "description": "Reescribe o consolida completamente el archivo MEMORY.md de la carpeta activa.",
        "input_schema": {
            "type": "object",
            "properties": {
                "memory_content": {"type": "string", "description": "Contenido completo en Markdown a guardar en MEMORY.md"}
            },
            "required": ["memory_content"]
        }
    }
]

def get_persisted_history(folder=""):
    """Lee el historial persistente de conversaciones en disco para la carpeta activa"""
    hfile = (STORAGE_DIR / folder / 'CHAT_HISTORY.json') if folder else (STORAGE_DIR / 'CHAT_HISTORY.json')
    if hfile.exists():
        try:
            return json.loads(hfile.read_text(encoding='utf-8'))
        except Exception:
            return []
    return []

def save_persisted_history(history, folder=""):
    """Guarda el historial en disco (mantiene los últimos 50 intercambios) para la carpeta activa"""
    hfile = (STORAGE_DIR / folder / 'CHAT_HISTORY.json') if folder else (STORAGE_DIR / 'CHAT_HISTORY.json')
    hfile.parent.mkdir(parents=True, exist_ok=True)
    trimmed = history[-50:]
    hfile.write_text(json.dumps(trimmed, indent=2, ensure_ascii=False), encoding='utf-8')

def append_to_memory(section_title, note, folder=""):
    """Añade una nota o lineamiento a la sección correspondiente de MEMORY.md de la carpeta activa"""
    mfile = (STORAGE_DIR / folder / 'MEMORY.md') if folder else (STORAGE_DIR / 'MEMORY.md')
    if not mfile.exists():
        mfile.write_text(f"# 🧠 Memoria Persistente ({folder or 'Raíz'})\n\n", encoding='utf-8')
    content = mfile.read_text(encoding='utf-8')
    
    header_match = re.search(rf"(##\s*.*{re.escape(section_title)}.*)", content, re.IGNORECASE)
    if header_match:
        header = header_match.group(1)
        content = content.replace(header, f"{header}\n- {note}")
    else:
        content = content.rstrip() + f"\n\n## 📌 {section_title}\n- {note}\n"
    mfile.write_text(content, encoding='utf-8')

@login_required
@csrf_exempt
def chat_history_api(request):
    """API para consultar o reiniciar el historial persistente de conversaciones por ámbito/carpeta"""
    folder = request.GET.get('folder', '').strip() if request.method == 'GET' else json.loads(request.body.decode('utf-8') or '{}').get('folder', '').strip()

    if request.method == 'GET':
        return JsonResponse({'history': get_persisted_history(folder), 'folder': folder})
    elif request.method == 'DELETE':
        save_persisted_history([], folder)
        return JsonResponse({'status': 'ok', 'message': f'Historial de conversaciones ({folder or "Raíz"}) reiniciado.'})
    return JsonResponse({'error': 'Método no soportado'}, status=405)

@login_required
@csrf_exempt
def ai_chat(request):
    """
    Endpoint del Agente Autónomo con Soporte para Subcarpetas Modulares, Memoria Aislada y Tool Calling
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método POST requerido'}, status=405)

    data = json.loads(request.body.decode('utf-8') or '{}')
    user_prompt = data.get('prompt', '').strip()
    selected_filename = data.get('filename', None)
    active_folder = data.get('folder', '').strip()

    if not user_prompt:
        return JsonResponse({'error': 'El prompt no puede estar vacío.'}, status=400)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key or api_key.startswith("tu_api_key"):
        return JsonResponse({'error': 'Configura una ANTHROPIC_API_KEY válida en tu archivo .env'}, status=400)

    model_name = os.environ.get("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
    client = anthropic.Anthropic(api_key=api_key)

    # 1. Leer claude.md (System Prompt)
    system_prompt = "Eres un Agente Autónomo con memoria modular y capacidad de crear subcarpetas con sus propios índices y memorias."
    if settings.CLAUDE_MD_PATH.exists():
        system_prompt = settings.CLAUDE_MD_PATH.read_text(encoding='utf-8')

    # 2. Cargar INDEX.md y MEMORY.md del ámbito activo (y global de la raíz)
    subfolders_list = get_subfolders()
    scope_desc = f"ÁMBITO / CARPETA ACTIVA: '{active_folder or 'Raíz (files_storage/)'}'"
    subfolders_desc = f"Subcarpetas existentes: {', '.join(subfolders_list) if subfolders_list else '(ninguna)'}"

    # Index y Memoria de la carpeta activa
    active_dir = (STORAGE_DIR / active_folder) if active_folder else STORAGE_DIR
    local_index_file = active_dir / 'INDEX.md'
    local_index_text = local_index_file.read_text(encoding='utf-8') if local_index_file.exists() else ""
    
    local_memory_file = active_dir / 'MEMORY.md'
    local_memory_text = local_memory_file.read_text(encoding='utf-8') if local_memory_file.exists() else ""

    # Index Raíz (si estamos en subcarpeta, para visión global)
    root_index_file = STORAGE_DIR / 'INDEX.md'
    root_index_text = root_index_file.read_text(encoding='utf-8') if (active_folder and root_index_file.exists()) else ""

    system_context = (
        f"{system_prompt}\n\n"
        f"[{scope_desc} | {subfolders_desc}]\n\n"
        f"[ÍNDICE LOCAL DEL ÁMBITO ACTIVO ({active_folder or 'Raíz'})]:\n{local_index_text}\n\n"
        f"[MEMORIA A LARGO PLAZO DEL ÁMBITO ACTIVO ({active_folder or 'Raíz'})]:\n{local_memory_text}"
    )
    if root_index_text:
        system_context += f"\n\n[ÍNDICE MAESTRO GLOBAL RAÍZ]:\n{root_index_text}"

    # 3. Contexto de archivo seleccionado en pantalla
    file_context = ""
    if selected_filename:
        fpath = STORAGE_DIR / selected_filename
        if fpath.exists() and fpath.is_file():
            try:
                content = fpath.read_text(encoding='utf-8')
                file_context = f"\n\n[ARCHIVO SELECCIONADO EN PANTALLA: '{selected_filename}']:\n{content}"
            except UnicodeDecodeError:
                file_context = f"\n\n[ARCHIVO SELECCIONADO EN PANTALLA: '{selected_filename}' (Archivo binario/PDF de {fpath.stat().st_size} bytes)]"

    # 4. Historial Persistente del ámbito activo
    persisted_history = get_persisted_history(active_folder)
    messages = []
    
    recent_history = persisted_history[-MAX_HISTORY_MESSAGES:]
    for msg in recent_history:
        messages.append({"role": msg["role"], "content": msg["content"]})

    current_user_message = f"{user_prompt}{file_context}"
    messages.append({"role": "user", "content": current_user_message})

    actions_executed = []

    try:
        response = client.messages.create(
            model=model_name,
            max_tokens=4096,
            system=system_context,
            tools=ANTHROPIC_TOOLS,
            messages=messages
        )

        iteration_count = 0
        while iteration_count < 8:
            tool_use_blocks = [block for block in response.content if getattr(block, "type", None) == "tool_use"]
            if not tool_use_blocks:
                break
            iteration_count += 1

            tool_results = []
            for tool_use_block in tool_use_blocks:
                tool_name = tool_use_block.name
                tool_input = tool_use_block.input
                tool_result_content = ""

                if tool_name == "create_subfolder":
                    fname = tool_input.get("folder_name", "").strip().replace("/", "").replace("\\", "")
                    fdesc = tool_input.get("description", f"Módulo {fname}")
                    init_subfolder(fname, fdesc)
                    actions_executed.append(f"📁 Subcarpeta '{fname}/' creada con su propio INDEX.md y MEMORY.md.")
                    tool_result_content = f"Subcarpeta '{fname}/' creada exitosamente con su propio INDEX.md y MEMORY.md, y registrada en el índice raíz."

                elif tool_name == "write_file":
                    fname = tool_input.get("filename", "").strip()
                    fcontent = tool_input.get("content", "")
                    fsummary = tool_input.get("summary", f"Documento {fname}")
                    fkeywords = tool_input.get("keywords", fname.replace('.', ' ').replace('_', ' '))
                    fwhen = tool_input.get("when_to_use", f"Consultas sobre {fname}")

                    # Si estamos en subcarpeta y no tiene prefijo, agregarlo
                    if active_folder and not fname.startswith(f"{active_folder}/") and "/" not in fname:
                        target_rel_path = f"{active_folder}/{fname}"
                    else:
                        target_rel_path = fname

                    target_path = STORAGE_DIR / target_rel_path
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    target_path.write_text(fcontent, encoding='utf-8')
                    
                    target_folder_scope = active_folder if active_folder else (target_rel_path.split("/")[0] if "/" in target_rel_path else "")
                    update_index_entry(target_rel_path, fkeywords, fsummary, fwhen, target_folder=target_folder_scope)
                    
                    actions_executed.append(f"✍️ Archivo '{target_rel_path}' guardado e indexado en su módulo.")
                    tool_result_content = f"Éxito: Archivo '{target_rel_path}' guardado físicamente en disco y registrado en su INDEX.md."

                elif tool_name == "read_file":
                    fname = tool_input.get("filename", "").strip()
                    target_path = STORAGE_DIR / fname
                    if not target_path.exists() and active_folder:
                        target_path = STORAGE_DIR / active_folder / fname

                    if target_path.exists() and target_path.is_file():
                        try:
                            tool_result_content = target_path.read_text(encoding='utf-8')
                        except UnicodeDecodeError:
                            tool_result_content = f"Archivo binario '{fname}' ({target_path.stat().st_size} bytes). No contiene texto plano."
                        actions_executed.append(f"📖 Archivo '{fname}' leído desde disco.")
                    else:
                        tool_result_content = f"Error: El archivo '{fname}' no existe."

                elif tool_name == "execute_script":
                    spath = tool_input.get("script_path", "").strip()
                    raw_args = tool_input.get("args", [])
                    args = [str(a) for a in raw_args]
                    
                    full_script_path = STORAGE_DIR / spath
                    if not full_script_path.exists() and active_folder:
                        full_script_path = STORAGE_DIR / active_folder / spath

                    if not full_script_path.exists():
                        tool_result_content = f"Error: El script '{spath}' no existe en disco."
                    else:
                        import subprocess
                        import sys
                        cmd = [sys.executable, str(full_script_path)] + args
                        work_dir = STORAGE_DIR / active_folder if active_folder else STORAGE_DIR
                        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(work_dir))
                        
                        if proc.returncode == 0:
                            actions_executed.append(f"⚙️ Script '{spath} {' '.join(args)}' ejecutado exitosamente.")
                            tool_result_content = f"Salida exitosa:\n{proc.stdout}"
                        else:
                            actions_executed.append(f"⚠️ Script '{spath}' falló con código {proc.returncode}.")
                            tool_result_content = f"Error en la ejecución:\n{proc.stderr or proc.stdout}"

                elif tool_name == "append_memory":
                    section = tool_input.get("section", "Lineamientos Generales")
                    note = tool_input.get("note", "")
                    append_to_memory(section, note, active_folder)
                    actions_executed.append(f"🧠 Aprendizaje guardado en MEMORY.md ({active_folder or 'Raíz'}): [{section}] {note}")
                    tool_result_content = f"Nota agregada a MEMORY.md en ámbito '{active_folder or 'Raíz'}'."

                elif tool_name == "update_memory":
                    mcontent = tool_input.get("memory_content", "")
                    mfile = (STORAGE_DIR / active_folder / 'MEMORY.md') if active_folder else (STORAGE_DIR / 'MEMORY.md')
                    mfile.write_text(mcontent, encoding='utf-8')
                    actions_executed.append(f"🧠 Memoria persistente completa ({active_folder or 'Raíz'}) actualizada.")
                    tool_result_content = f"Memoria reestructurada en ámbito '{active_folder or 'Raíz'}'."

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_use_block.id,
                    "content": tool_result_content
                })

            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})

            response = client.messages.create(
                model=model_name,
                max_tokens=4096,
                system=system_context,
                tools=ANTHROPIC_TOOLS,
                messages=messages
            )

        ai_reply = ""
        for block in response.content:
            if hasattr(block, "text"):
                ai_reply += block.text

        persisted_history.append({"role": "user", "content": user_prompt})
        persisted_history.append({"role": "assistant", "content": ai_reply, "actions": actions_executed})
        save_persisted_history(persisted_history, active_folder)

        return JsonResponse({
            'status': 'ok',
            'response': ai_reply,
            'actions_executed': actions_executed,
            'folder': active_folder
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@xframe_options_exempt
def presentacion_clase8(request):
    """Sirve la presentación interactiva HTML de la Clase 8 (10-skill)"""
    pres_path = Path(settings.BASE_DIR) / 'clase8' / '10-skill' / 'presentacion_clase8.html'
    if pres_path.exists():
        return HttpResponse(pres_path.read_text(encoding='utf-8'), content_type='text/html; charset=utf-8')
    raise Http404("Presentación de Clase 8 no encontrada.")


