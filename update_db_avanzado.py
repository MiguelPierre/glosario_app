import sqlite3


def agregar_columnas_avanzadas():
    conexion = sqlite3.connect("glosario.db")
    cursor = conexion.cursor()

    nuevas_columnas = {
        "origen_definicion": "TEXT",
        "destino_definicion": "TEXT",
        "origen_relaciones": "TEXT",
        "destino_relaciones": "TEXT",
    }

    print("🔧 Iniciando actualización de la base de datos...")

    for columna, tipo in nuevas_columnas.items():
        try:
            cursor.execute(f"ALTER TABLE terminos ADD COLUMN {columna} {tipo}")
            print(f"✅ Columna '{columna}' añadida.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print(f"ℹ️ La columna '{columna}' ya existía.")
            else:
                print(f"❌ Error al añadir {columna}: {e}")

    conexion.commit()
    conexion.close()
    print("🏁 Actualización de esquema finalizada.")


if __name__ == "__main__":
    agregar_columnas_avanzadas()
