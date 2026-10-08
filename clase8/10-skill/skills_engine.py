"""
Skills Engine: Motor de Habilidades Especializadas para Agentes de IA
Clase 8: Arquitectura de Skills, Router Jerárquico, Búsqueda SQL y Memoria Adaptativa
"""

import os
import re
import sys
import json
import sqlite3
from typing import Dict, Any, List, Optional
from pathlib import Path

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

try:
    from .catalogo_db import init_database, describe_schema, query_catalogo, find_cheapest_product, DB_PATH
except (ImportError, ValueError):
    from catalogo_db import init_database, describe_schema, query_catalogo, find_cheapest_product, DB_PATH

class BaseSkill:
    """Clase base para todas las habilidades del agente."""
    name: str = "base_skill"
    description: str = "Habilidad base abstracta"
    version: str = "1.0.0"

    def match(self, prompt: str, context: Dict[str, Any]) -> bool:
        """Determina si la habilidad debe activarse según el prompt y contexto."""
        raise NotImplementedError

    def execute(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta la habilidad y devuelve los resultados."""
        raise NotImplementedError

class RouterJerarquicoSkill(BaseSkill):
    """
    Habilidad de Enrutamiento Jerárquico de Carpetas e Índices.
    Navega desde el índice general (raíz) hacia el índice específico de la subcarpeta.
    """
    name: str = "router_jerarquico"
    description: str = "Navega índices Markdown estructurados para localizar módulos e insumos."
    version: str = "1.2.0"

    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or Path(__file__).parent / "sample_storage"

    def match(self, prompt: str, context: Dict[str, Any]) -> bool:
        keywords = ["donde", "carpeta", "indice", "modulo", "estructura", "rubro", "catalogo", "listar", "ver"]
        prompt_lower = prompt.lower()
        return any(kw in prompt_lower for kw in keywords)

    def route_query(self, query: str) -> Dict[str, Any]:
        """
        1. Lee el índice general (INDEX.md raíz).
        2. Encuentra la subcarpeta más adecuada por palabras clave.
        3. Carga el INDEX.md local de esa subcarpeta.
        """
        root_index_path = self.base_dir / "INDEX.md"
        if not root_index_path.exists():
            return {"error": f"No se encontró el índice general en {root_index_path}"}

        root_content = root_index_path.read_text(encoding="utf-8")
        query_words = set(re.findall(r"\w+", query.lower()))

        # Módulos conocidos y mapeo semántico
        matched_folder = None
        for folder in ["libreria", "indumentaria", "carniceria"]:
            if folder in query.lower():
                matched_folder = folder
                break

        if not matched_folder:
            # Búsqueda por palabras clave en el índice raíz
            lines = root_content.splitlines()
            for line in lines:
                if "|" in line and not line.startswith("#") and not "---" in line:
                    parts = [p.strip() for p in line.split("|") if p.strip()]
                    if len(parts) >= 3:
                        folder_name = parts[0].replace("`", "").replace("/", "").strip()
                        keywords = parts[1].replace("`", "").lower()
                        if any(kw.strip() in query.lower() for kw in keywords.split(",")):
                            matched_folder = folder_name
                            break

        if not matched_folder:
            matched_folder = "libreria" # Fallback predeterminado

        # Cargar índice del módulo correspondiente
        subfolder_index_path = self.base_dir / matched_folder / "INDEX.md"
        sub_content = subfolder_index_path.read_text(encoding="utf-8") if subfolder_index_path.exists() else "Índice no disponible"

        return {
            "modulo_identificado": matched_folder,
            "ruta_modulo": str(self.base_dir / matched_folder),
            "indice_local": sub_content,
            "explicacion_ruteo": f"Ruteado al módulo '{matched_folder}' según análisis de palabras clave."
        }

    def execute(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        result = self.route_query(prompt)
        return {
            "skill": self.name,
            "success": True,
            "data": result
        }

class CatalogoSQLSkill(BaseSkill):
    """
    Habilidad de Consulta y Búsqueda en Base de Datos de Catálogo.
    Analiza consultas como 'cuál es el cuaderno más barato' y genera el SQL óptimo:
    SELECT * FROM insumos WHERE ... ORDER BY precio ASC LIMIT 1
    """
    name: str = "catalogo_sql"
    description: str = "Genera y ejecuta consultas SQL optimizadas sobre la base de datos de insumos."
    version: str = "2.0.0"

    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        init_database(self.db_path)

    def match(self, prompt: str, context: Dict[str, Any]) -> bool:
        terms = ["barato", "precio", "stock", "cuanto", "insumo", "sql", "ordenar", "mas caro", "cuaderno", "remera", "pollo", "milanesa"]
        prompt_lower = prompt.lower()
        return any(t in prompt_lower for t in terms)

    def get_schema(self) -> dict:
        return describe_schema(self.db_path)

    def execute(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        prompt_lower = prompt.lower()
        categoria = None
        if "libreria" in prompt_lower:
            categoria = "libreria"
        elif "indumentaria" in prompt_lower or "ropa" in prompt_lower:
            categoria = "indumentaria"
        elif "carniceria" in prompt_lower or "carne" in prompt_lower:
            categoria = "carniceria"

        # Extraer palabra clave del insumo
        keywords = ["cuaderno", "lapiz", "lapices", "lapicera", "resma", "remera", "pantalon", "buzo", "pollo", "asado", "milanesa"]
        target_keyword = "cuaderno"
        for kw in keywords:
            if kw in prompt_lower:
                target_keyword = kw
                break

        # Búsqueda del producto más barato o consulta general
        is_asking_cheapest = any(w in prompt_lower for w in ["barat", "economic", "menor preci", "mas barat", "más barat", "menor cost", "accesibl"])
        
        if is_asking_cheapest:
            product = find_cheapest_product(target_keyword, categoria, self.db_path)
            sql_utilizado = f"SELECT * FROM insumos WHERE (nombre LIKE '%{target_keyword}%' OR palabras_relacionadas LIKE '%{target_keyword}%') ORDER BY precio ASC LIMIT 1;"
            return {
                "skill": self.name,
                "success": True,
                "tipo_consulta": "producto_mas_barato",
                "sql": sql_utilizado,
                "producto": product,
                "mensaje": f"El producto más barato de tipo '{target_keyword}' es '{product['nombre']}' a ${product['precio']} (Stock: {product['stock']})" if product else "No se encontraron productos coincidentes."
            }
        else:
            # Consulta general de insumos
            query = """
            SELECT i.id, i.nombre, i.descripcion, i.precio, i.stock, c.nombre AS categoria
            FROM insumos i
            LEFT JOIN categorias c ON i.categoria_id = c.id
            WHERE LOWER(i.nombre) LIKE ? OR LOWER(i.palabras_relacionadas) LIKE ?
            """
            rows = query_catalogo(query, (f"%{target_keyword}%", f"%{target_keyword}%"), self.db_path)
            return {
                "skill": self.name,
                "success": True,
                "tipo_consulta": "listado_insumos",
                "sql": query,
                "productos": rows,
                "cantidad": len(rows)
            }

class AsesorVentasSkill(BaseSkill):
    """
    Habilidad de Asesor de Ventas con Adaptación Léxica y Persistencia de Permisos.
    - Analiza el estilo y vocabulario del usuario (Mirroring).
    - Registra permisos otorgados (ej: no volver a preguntar por confirmaciones ya aceptadas).
    - Conecta con el Router Jerárquico y CatalogoSQL para emitir presupuestos y recomendaciones.
    """
    name: str = "asesor_ventas"
    description: str = "Asesor comercial que adapta su tono al cliente, respeta permisos y elabora respuestas vendedoras."
    version: str = "1.5.0"

    def __init__(self, storage_dir: Optional[Path] = None):
        self.storage_dir = storage_dir or Path(__file__).parent / "sample_storage"
        self.sql_skill = CatalogoSQLSkill()
        self.router_skill = RouterJerarquicoSkill(self.storage_dir)

    def match(self, prompt: str, context: Dict[str, Any]) -> bool:
        # El asesor maneja consultas generales de venta y consultas de clientes
        return True

    def extract_user_style(self, prompt: str, history: List[dict]) -> dict:
        """Calcula métricas de vocabulario y tono del usuario para espejarlo."""
        all_text = prompt + " " + " ".join([m.get("content", "") for m in history if m.get("role") == "user"])
        words = re.findall(r"\b\w+\b", all_text.lower())
        
        is_informal = any(w in words for w in ["che", "hola", "dale", "joya", "barato", "tenes", "pasa", "de una", "genial"])
        is_formal = any(w in words for w in ["estimado", "usted", "solicito", "presupuesto", "cotizacion", "agradeceria"])

        tone = "informal_cercano" if is_informal and not is_formal else ("formal_ejecutivo" if is_formal else "cordial_neutro")
        return {
            "total_palabras": len(words),
            "tono_detectado": tone,
            "palabras_frecuentes": list(set([w for w in words if len(w) > 4]))[:10]
        }

    def check_permissions(self, user_id: str = "default") -> dict:
        """Carga permisos otorgados previamente en MEMORY.md o archivo de permisos."""
        memory_file = self.storage_dir / "MEMORY.md"
        permissions = {
            "auto_confirm_quote": False,
            "preferred_currency": "ARS",
            "show_stock": True
        }
        if memory_file.exists():
            content = memory_file.read_text(encoding="utf-8")
            if "permiso: cotizacion_directa" in content.lower() or "sin repreguntar" in content.lower():
                permissions["auto_confirm_quote"] = True
        return permissions

    def execute(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        history = context.get("history", [])
        style = self.extract_user_style(prompt, history)
        permissions = self.check_permissions()

        # 1. Ruteo jerárquico
        routing = self.router_skill.route_query(prompt)

        # 2. Búsqueda SQL
        db_res = self.sql_skill.execute(prompt, context)

        # 3. Formulación de respuesta vendedora y empática (Mirroring)
        if db_res.get("tipo_consulta") == "producto_mas_barato" and db_res.get("producto"):
            prod = db_res["producto"]
            if style["tono_detectado"] == "informal_cercano":
                saludo = "¡Qué tal! Acá tenés la mejor opción económica que tenemos:"
                cierre = "¿Querés que te prepare el pedido o te aparte algunas unidades?"
            elif style["tono_detectado"] == "formal_ejecutivo":
                saludo = "Estimado/a, le presento la cotización más conveniente disponible en nuestro catálogo:"
                cierre = "Quedamos a su entera disposición para emitir el comprobante correspondiente."
            else:
                saludo = "¡Mucho gusto! Te comparto la opción más accesible de nuestro catálogo:"
                cierre = "Si te sirve, podemos avanzar con la preparación del pedido."

            respuesta_bonita = (
                f"{saludo}\n\n"
                f"📌 **{prod['nombre']}**\n"
                f"- **Precio:** ${prod['precio']:.2f}\n"
                f"- **Stock Disponible:** {prod['stock']} unidades\n"
                f"- **Detalle:** {prod['descripcion']}\n\n"
                f"{cierre}"
            )
        else:
            respuesta_bonita = f"He consultado el módulo de **{routing['modulo_identificado']}** y nuestro catálogo. ¿Deseas consultar algún artículo en particular?"

        return {
            "skill": self.name,
            "success": True,
            "estilo_usuario": style,
            "permisos_activos": permissions,
            "ruteo": routing,
            "sql_utilizado": db_res.get("sql"),
            "respuesta_sugerida": respuesta_bonita
        }

class SkillManager:
    """Administrador central de Skills del agente."""
    def __init__(self, base_storage: Optional[Path] = None):
        self.storage = base_storage or Path(__file__).parent / "sample_storage"
        self.skills: List[BaseSkill] = [
            RouterJerarquicoSkill(self.storage),
            CatalogoSQLSkill(),
            AsesorVentasSkill(self.storage)
        ]

    def process_prompt(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        context = context or {}
        results = []
        for skill in self.skills:
            if skill.match(prompt, context):
                res = skill.execute(prompt, context)
                results.append(res)

        # La habilidad de asesor de ventas integra todo
        asesor = next((s for s in self.skills if isinstance(s, AsesorVentasSkill)), None)
        final_output = asesor.execute(prompt, context) if asesor else results[-1]

        return {
            "prompt": prompt,
            "skills_ejecutadas": [s.name for s in self.skills if s.match(prompt, context)],
            "resultado_asesor": final_output
        }

if __name__ == "__main__":
    manager = SkillManager()
    test_prompt = "Hola, quiero saber cuál es el cuaderno más barato que tenés en stock"
    output = manager.process_prompt(test_prompt)
    print("=== TEST PROMPT ===")
    print(test_prompt)
    print("\n=== RESPUESTA BONITA GENERADA ===")
    print(output["resultado_asesor"]["respuesta_sugerida"])
    print("\n=== DETALLES DE SKILLS ===")
    print(json.dumps(output, indent=2, ensure_ascii=False))
