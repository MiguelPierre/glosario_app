import sqlite3

def iniciar_base_datos():
    # Conectamos con la base de datos (si no existe, la crea automáticamente)
    conexion = sqlite3.connect("glosario.db")
    cursor = conexion.cursor()

    # Creamos la tabla "terminos" con las columnas que definimos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS terminos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origen_term TEXT NOT NULL,
            destino_term TEXT NOT NULL,
            origen_lang TEXT,
            destino_lang TEXT,
            contexto TEXT,
            fuente TEXT,
            notas TEXT
        )
    """)

    # Guardamos los cambios y cerramos
    conexion.commit()
    conexion.close()
    print("¡Base de datos 'glosario.db' creada con éxito!")

if __name__ == "__main__":
    iniciar_base_datos()