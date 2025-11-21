import sqlite3

def actualizar_base_datos():
    conexion = sqlite3.connect("glosario.db")
    cursor = conexion.cursor()
    
    try:
        # Intentamos añadir la columna 'categoria'
        cursor.execute("ALTER TABLE terminos ADD COLUMN categoria TEXT")
        print("✅ Columna 'categoria' añadida con éxito.")
    except sqlite3.OperationalError:
        print("ℹ️ La columna 'categoria' ya existía.")
        
    conexion.commit()
    conexion.close()

if __name__ == "__main__":
    actualizar_base_datos()