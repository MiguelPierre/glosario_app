import sqlite3

def agregar_columna_contexto():
    conexion = sqlite3.connect("glosario.db")
    cursor = conexion.cursor()
    
    columna_nueva = "destino_contexto"
    
    print("🔧 Iniciando actualización para añadir contexto destino...")
    
    try:
        cursor.execute(f"ALTER TABLE terminos ADD COLUMN {columna_nueva} TEXT")
        print(f"✅ Columna '{columna_nueva}' añadida.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print(f"ℹ️ La columna '{columna_nueva}' ya existía.")
        else:
            print(f"❌ Error al añadir {columna_nueva}: {e}")
            
    conexion.commit()
    conexion.close()
    print("🏁 Actualización de esquema finalizada.")

if __name__ == "__main__":
    agregar_columna_contexto()
