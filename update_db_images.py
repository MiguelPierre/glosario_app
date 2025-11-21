import sqlite3

def agregar_columna_imagen():
    conexion = sqlite3.connect("glosario.db")
    cursor = conexion.cursor()
    
    try:
        # BLOB es el tipo de dato para guardar archivos binarios (fotos, pdfs, etc.)
        cursor.execute("ALTER TABLE terminos ADD COLUMN imagen BLOB")
        print("✅ Columna 'imagen' añadida con éxito.")
    except sqlite3.OperationalError:
        print("ℹ️ La columna 'imagen' ya existía.")
        
    conexion.commit()
    conexion.close()

if __name__ == "__main__":
    agregar_columna_imagen()