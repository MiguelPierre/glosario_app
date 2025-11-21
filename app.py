import streamlit as st
import sqlite3
import pandas as pd
import io

# 1. Configuración
st.set_page_config(page_title="Glosario Vial Pro", layout="wide", page_icon="🚧")
st.title("🚧 Glosario de Seguridad Vial")

# --- FUNCIONES DE BASE DE DATOS ---
def obtener_conexion():
    return sqlite3.connect("glosario.db")

def ejecutar_consulta(query, params=()):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

# --- PESTAÑAS ---
tab1, tab2, tab3 = st.tabs(["🔍 Consultar", "➕ Añadir", "⚙️ Gestionar"])

# ==========================================
# PESTAÑA 1: CONSULTAR (MODO FICHAS)
# ==========================================
with tab1:
    col_search, col_cat = st.columns([3, 1])
    query = col_search.text_input("Buscar término:", placeholder="Ej: baliza, barrier...")
    filtro_cat = col_cat.selectbox("Filtrar por Categoría", ["Todas", "General", "Señalización", "Ingeniería Civil", "Sistemas ITS", "Legal/Normativa"])

    conn = obtener_conexion()
    # Seleccionamos también la imagen
    sql = "SELECT id, origen_term, destino_term, categoria, origen_lang, destino_lang, contexto, fuente, imagen FROM terminos WHERE (origen_term LIKE ? OR destino_term LIKE ?)"
    params = [f'%{query}%', f'%{query}%']

    if filtro_cat != "Todas":
        sql += " AND categoria = ?"
        params.append(filtro_cat)

    # Leemos los datos. ¡Ojo! Pandas no maneja bien BLOBs directamente para visualizar,
    # así que iteraremos manualmente si hay pocos resultados.
    df = pd.read_sql(sql, conn, params=params)
    conn.close()

    if not df.empty:
        st.success(f"Encontrados {len(df)} términos.")
        st.divider()
        
        # Iteramos sobre cada resultado para mostrarlo como una "Ficha" bonita
        for index, row in df.iterrows():
            with st.container():
                c_texto, c_img = st.columns([3, 1])
                
                with c_texto:
                    # Título grande con los términos
                    st.subheader(f"{row['origen_term']} ➝ {row['destino_term']}")
                    # Etiquetas pequeñas
                    st.caption(f"📂 {row['categoria']} | 🌍 {row['origen_lang']} -> {row['destino_lang']}")
                    
                    if row['contexto']:
                        st.info(f"📝 **Contexto:** {row['contexto']}")
                    
                    # Detalles extra en letra pequeña
                    detalles = []
                    if row['fuente']: detalles.append(f"Fuente: {row['fuente']}")
                    st.text(" | ".join(detalles))
                
                with c_img:
                    # Si hay imagen (bytes), la mostramos
                    if row['imagen']:
                        st.image(row['imagen'], caption="Referencia Visual", use_container_width=True)
                    else:
                        # Espacio vacío si no hay foto
                        st.write("") 
                
                st.divider() # Línea separadora entre fichas
    else:
        if query:
            st.warning("No se encontraron resultados.")
        else:
            st.info("Escribe algo para buscar.")

# ==========================================
# PESTAÑA 2: AÑADIR (CON FOTO)
# ==========================================
with tab2:
    st.header("Añadir nuevo término")
    with st.form("form_alta"):
        c1, c2, c3 = st.columns(3)
        nuevo_origen = c1.text_input("Término Origen *")
        nuevo_destino = c2.text_input("Término Destino *")
        nueva_categoria = c3.selectbox("Categoría", ["General", "Señalización", "Ingeniería Civil", "Sistemas ITS", "Legal/Normativa"])
        
        c4, c5 = st.columns(2)
        lang_origen = c4.selectbox("Idioma Origen", ["Inglés", "Español", "Francés"], key="l_orig")
        lang_destino = c5.selectbox("Idioma Destino", ["Español", "Inglés", "Francés"], key="l_dest")
        
        nuevo_contexto = st.text_area("Contexto")
        nueva_fuente = st.text_input("Fuente")
        
        # CAMPO NUEVO: SUBIDA DE IMAGEN
        archivo_imagen = st.file_uploader("📸 Subir imagen (Opcional)", type=["png", "jpg", "jpeg"])
        
        if st.form_submit_button("Guardar"):
            if nuevo_origen and nuevo_destino:
                # Procesar imagen a binario
                blob_imagen = None
                if archivo_imagen:
                    blob_imagen = archivo_imagen.getvalue()

                sql = """INSERT INTO terminos (origen_term, destino_term, categoria, origen_lang, destino_lang, contexto, fuente, imagen) 
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
                ejecutar_consulta(sql, (nuevo_origen, nuevo_destino, nueva_categoria, lang_origen, lang_destino, nuevo_contexto, nueva_fuente, blob_imagen))
                st.success(f"✅ '{nuevo_origen}' guardado correctamente.")
                st.rerun()
            else:
                st.error("Faltan campos obligatorios.")

# ==========================================
# PESTAÑA 3: GESTIÓN
# ==========================================
with tab3:
    st.header("Modificar o Eliminar")
    
    conn = obtener_conexion()
    todos_terminos = pd.read_sql("SELECT id, origen_term, destino_term FROM terminos", conn)
    conn.close()
    
    if not todos_terminos.empty:
        opciones = {f"{row['id']} : {row['origen_term']} -> {row['destino_term']}": row['id'] for index, row in todos_terminos.iterrows()}
        seleccion = st.selectbox("Selecciona el término a gestionar:", list(opciones.keys()))
        id_seleccionado = opciones[seleccion]

        conn = obtener_conexion()
        # Leemos todo para rellenar el formulario
        dato = pd.read_sql("SELECT * FROM terminos WHERE id = ?", conn, params=(id_seleccionado,)).iloc[0]
        conn.close()

        with st.form("form_edicion"):
            st.subheader(f"Editando ID: {id_seleccionado}")
            e_origen = st.text_input("Origen", value=dato['origen_term'])
            e_destino = st.text_input("Destino", value=dato['destino_term'])
            # Nota: La edición de imagen es compleja, de momento permitimos editar texto
            st.info("ℹ️ Para cambiar la imagen, es mejor borrar y crear de nuevo el término.")
            
            col_del, col_upd = st.columns([1, 4])
            with col_upd:
                if st.form_submit_button("💾 Actualizar Textos"):
                    ejecutar_consulta("UPDATE terminos SET origen_term=?, destino_term=? WHERE id=?", (e_origen, e_destino, id_seleccionado))
                    st.success("Actualizado.")
                    st.rerun()
            with col_del:
                if st.form_submit_button("🗑️ BORRAR", type="primary"):
                    ejecutar_consulta("DELETE FROM terminos WHERE id=?", (id_seleccionado,))
                    st.error("Eliminado.")
                    st.rerun()