import sqlite3

def reparar_base_datos():
    print("🔧 Iniciando reparación de la base de datos...")
    conexion = sqlite3.connect("glosario.db")
    cursor = conexion.cursor()
    
    # 1. Intentar añadir la columna CATEGORIA
    try:
        cursor.execute("ALTER TABLE terminos ADD COLUMN categoria TEXT")
        print("✅ Columna 'categoria' añadida con éxito.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("ℹ️ La columna 'categoria' ya existía (Correcto).")
        else:
            print(f"⚠️ Error inesperado en categoria: {e}")

    # 2. Intentar añadir la columna IMAGEN (Esta es la que te falta)
    try:
        cursor.execute("ALTER TABLE terminos ADD COLUMN imagen BLOB")
        print("✅ Columna 'imagen' añadida con éxito.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("ℹ️ La columna 'imagen' ya existía (Correcto).")
        else:
            print(f"⚠️ Error inesperado en imagen: {e}")
            
    conexion.commit()
    conexion.close()
    print("🏁 Reparación finalizada.")

if __name__ == "__main__":
    reparar_base_datos()