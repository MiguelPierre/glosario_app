import sqlite3
import pandas as pd
import os

# --- 1. CONFIGURACIÓN ---
NOMBRE_ARCHIVO_CSV = 'glosario_completo.csv'
NOMBRE_BD = 'glosario.db'
NOMBRE_TABLA = 'terminos'

# Definimos las columnas que el CSV DEBE tener, en el orden correcto para la BD
COLUMNAS_ESPERADAS = [
    'origen_term', 'destino_term', 'origen_lang', 'destino_lang', 
    'categoria', 'contexto', 'fuente'
]

# --- 2. FUNCIÓN DE IMPORTACIÓN ---
def importar_glosario():
    if not os.path.exists(NOMBRE_ARCHIVO_CSV):
        print(f"❌ Error: El archivo {NOMBRE_ARCHIVO_CSV} no se encuentra en la carpeta.")
        return

    try:
        # 2a. Leer el archivo CSV usando Pandas
        df = pd.read_csv(NOMBRE_ARCHIVO_CSV, sep=';')
        
        # 2b. Verificar que el CSV contenga las columnas necesarias
        if not all(col in df.columns for col in COLUMNAS_ESPERADAS):
            print("❌ Error: El archivo CSV no contiene todas las columnas esperadas.")
            print(f"Columnas requeridas: {COLUMNAS_ESPERADAS}")
            return

        # Seleccionar solo las columnas que vamos a importar y rellenar nulos con string vacío (para SQLite)
        df = df[COLUMNAS_ESPERADAS].fillna('') 
        
        # 2c. Conectar a la base de datos
        conn = sqlite3.connect(NOMBRE_BD)
        cursor = conn.cursor()
        
        contador = 0
        
        # 2d. Iterar sobre el DataFrame e insertar en la base de datos
        for index, row in df.iterrows():
            # CORRECCIÓN APLICADA AQUÍ: Se usan 8 placeholders (?) en total.
            sql_insert = f"""
                INSERT INTO {NOMBRE_TABLA} ({', '.join(COLUMNAS_ESPERADAS)}, imagen)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            # Los valores de la fila (7) se unen con un None para la columna 'imagen' (total 8 valores)
            valores = tuple(row)
            cursor.execute(sql_insert, valores + (None,))

            contador += 1
            
        conn.commit()
        conn.close()
        
        print(f"✅ ¡Importación finalizada! Se añadieron {contador} términos.")
        
    except Exception as e:
        print(f"❌ Ocurrió un error durante la importación: {e}")

if __name__ == "__main__":
    importar_glosario()