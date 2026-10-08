"""
Módulo de Base de Datos y Catálogo para la Clase 8 (10-skill)
Permite gestionar la base de datos SQLite de insumos, obtener esquemas (DESCRIBE)
y ejecutar consultas SQL parametrizadas o filtradas.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "catalogo.sqlite3"

def init_database(db_path: Path = DB_PATH):
    """Crea las tablas e inserta los datos de ejemplo iniciales."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Tabla de categorías
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL,
        descripcion TEXT,
        palabras_clave TEXT
    )
    """)

    # Tabla de insumos / productos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS insumos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        precio REAL NOT NULL,
        stock INTEGER NOT NULL,
        categoria_id INTEGER,
        palabras_relacionadas TEXT,
        FOREIGN KEY (categoria_id) REFERENCES categorias (id)
    )
    """)

    # Insertar categorías si están vacías
    cursor.execute("SELECT COUNT(*) FROM categorias")
    if cursor.fetchone()[0] == 0:
        categorias = [
            (1, "libreria", "Insumos y artículos de librería, oficina y escolares", "libro, cuaderno, lapiz, borrador, regla, resma, hojas, marcador"),
            (2, "indumentaria", "Ropa, uniformes y calzado comercial", "remera, pantalon, buzo, camisa, campera, zapatillas"),
            (3, "carniceria", "Cortes de carne, aves y pescados", "carne, pollo, pescado, asado, lomo, milanesa, vacio")
        ]
        cursor.executemany("INSERT INTO categorias (id, nombre, descripcion, palabras_clave) VALUES (?, ?, ?, ?)", categorias)

    # Insertar insumos si están vacíos
    cursor.execute("SELECT COUNT(*) FROM insumos")
    if cursor.fetchone()[0] == 0:
        insumos = [
            # Librería
            ("Cuaderno de dibujo espiralado", "Cuaderno con hojas lisas especiales para dibujo 20x30", 150.0, 50, 1, "cuaderno, dibujo, espiral, arte"),
            ("Cuaderno A4 universitario", "Cuaderno A4 rayado tapa dura 100 hojas", 200.0, 100, 1, "cuaderno, a4, hojas, universidad, rayado"),
            ("Cuaderno económico tapa blanda", "Cuaderno tamaño escolar 48 hojas económico", 95.0, 250, 1, "cuaderno, economico, escolar, barato"),
            ("Lápices de colores x12", "Caja de lápices de madera de 12 colores vivos", 100.0, 100, 1, "lapiz, lapices, colores, pintar"),
            ("Lapicera trazo fino azul", "Bolígrafo tinta gel azul 0.5mm", 45.0, 300, 1, "lapicera, boligrafo, azul, escribir"),
            ("Resma A4 75g", "Resma 500 hojas multifunción blanco puro", 450.0, 40, 1, "resma, papel, a4, impresion"),
            
            # Indumentaria
            ("Remera de algodón básica", "Remera manga corta 100% algodón peinado", 1200.0, 80, 2, "remera, algodon, basica, remeras"),
            ("Pantalón de trabajo cargo", "Pantalón reforzado con 6 bolsillos", 2500.0, 45, 2, "pantalon, cargo, trabajo, pantalones"),
            ("Buzo cuello redondo", "Buzo clásico de frisa abrigado", 3100.0, 30, 2, "buzo, abrigo, frisa, invierno"),

            # Carnicería
            ("Pechuga de pollo fresca x kg", "Pechuga desosada de granja seleccionada", 850.0, 60, 3, "pollo, pechuga, granja, carne blanca"),
            ("Asado de tira novillito x kg", "Corte especial para parrilla", 1800.0, 40, 3, "asado, carne, tira, novillito, parrilla"),
            ("Milanesas preparadas x kg", "Milanesas de carne de nalga empanadas", 1400.0, 55, 3, "milanesa, carne, nalga, empanada")
        ]
        cursor.executemany(
            "INSERT INTO insumos (nombre, descripcion, precio, stock, categoria_id, palabras_relacionadas) VALUES (?, ?, ?, ?, ?, ?)",
            insumos
        )

    conn.commit()
    conn.close()

def describe_schema(db_path: Path = DB_PATH) -> dict:
    """Devuelve el esquema completo de las tablas (equivalente a DESCRIBE / PRAGMA)."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    schema = {}
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = [row[0] for row in cursor.fetchall()]
    
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        schema[table] = [
            {"cid": col[0], "name": col[1], "type": col[2], "notnull": bool(col[3]), "dflt_value": col[4], "pk": bool(col[5])}
            for col in columns
        ]
    conn.close()
    return schema

def query_catalogo(sql_query: str, params: tuple = (), db_path: Path = DB_PATH) -> list:
    """Ejecuta una consulta SQL de lectura y retorna los resultados como lista de diccionarios."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql_query, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def find_cheapest_product(keyword: str, categoria: str = None, db_path: Path = DB_PATH) -> dict:
    """
    Busca el producto más barato que coincida con una palabra clave o categoría.
    Implementa: SELECT * FROM insumos WHERE ... ORDER BY precio ASC LIMIT 1
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
    SELECT i.id, i.nombre, i.descripcion, i.precio, i.stock, c.nombre AS categoria, i.palabras_relacionadas
    FROM insumos i
    LEFT JOIN categorias c ON i.categoria_id = c.id
    WHERE (LOWER(i.nombre) LIKE ? OR LOWER(i.palabras_relacionadas) LIKE ? OR LOWER(i.descripcion) LIKE ?)
    """
    params = [f"%{keyword.lower()}%", f"%{keyword.lower()}%", f"%{keyword.lower()}%"]

    if categoria:
        query += " AND LOWER(c.nombre) = ?"
        params.append(categoria.lower())

    query += " ORDER BY i.precio ASC LIMIT 1"

    cursor.execute(query, tuple(params))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

if __name__ == "__main__":
    init_database()
    print("Base de datos de catálogo inicializada con éxito.")
    print("Esquema:")
    print(describe_schema())
    print("\nProducto más barato para 'cuaderno':")
    print(find_cheapest_product("cuaderno"))
