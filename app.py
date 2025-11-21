import streamlit as st
import sqlite3
import pandas as pd
import io

# --- 0. CONFIGURACIÓN INICIAL Y ESTADO ---
st.set_page_config(page_title="Glosario Vial Pro", layout="wide", page_icon="🚧")

# Inicializa el estado para saber qué término mostrar
if "termino_seleccionado_id" not in st.session_state:
    st.session_state["termino_seleccionado_id"] = None


# --- FUNCIONES DE BASE DE DATOS ---
def obtener_conexion():
    return sqlite3.connect("glosario.db")


def ejecutar_consulta(query, params=()):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()


# ----------------------------------------------------------------------
# VISTA DE DETALLE: IMPLEMENTACIÓN AVANZADA
# ----------------------------------------------------------------------
def mostrar_detalle_termino(termino_id):
    conn = obtener_conexion()
    # Recuperar TODOS los datos
    dato = pd.read_sql(
        "SELECT * FROM terminos WHERE id = ?", conn, params=(termino_id,)
    ).iloc[0]
    conn.close()

    # Botón para volver a la búsqueda
    if st.button("⬅️ Volver a los resultados de búsqueda"):
        st.session_state["termino_seleccionado_id"] = None
        st.rerun()

    st.title(f"Detalle Terminológico: {dato['origen_term']} ➝ {dato['destino_term']}")
    st.caption(
        f"ID de registro: {dato['id']} | Categoría: {dato['categoria']} | Fuente: {dato['fuente']}"
    )
    st.divider()

    col_en, col_es = st.columns(2)

    # COLUMNA DE ORIGEN (EN/Inglés)
    with col_en:
        st.subheader(f"🌐 Término Origen ({dato['origen_lang']})")
        st.markdown(f"## **{dato['origen_term']}**")

        # 1. Definición Formal de Origen
        st.markdown("### 📝 Definición")
        if dato["origen_definicion"]:
            st.code(dato["origen_definicion"], language="markdown")
        else:
            st.info("Sin definición formal.")

        # 2. Relaciones Conceptuales de Origen
        st.markdown("### 🗂️ Relaciones Conceptuales")
        if dato["origen_relaciones"]:
            st.markdown(f"> *{dato['origen_relaciones']}*")
        else:
            st.info("Sin relaciones jerárquicas o conceptuales.")

        # 3. Contexto Asociativo de Origen (Campo existente)
        st.markdown("### Contexto de Uso")
        if dato["contexto"]:
            st.markdown(f"> *{dato['contexto']}*")
        else:
            st.info("Sin contexto de uso.")

    # COLUMNA DE DESTINO (ES/Español)
    with col_es:
        st.subheader(f"🇪🇸 Término Destino ({dato['destino_lang']})")
        st.markdown(f"## **{dato['destino_term']}**")

        # 1. Definición Formal de Destino
        st.markdown("### 📝 Definición")
        if dato["destino_definicion"]:
            st.code(dato["destino_definicion"], language="markdown")
        else:
            st.info("Sin definición formal.")

        # 2. Relaciones Conceptuales de Destino
        st.markdown("### 🗂️ Relaciones Conceptuales")
        if dato["destino_relaciones"]:
            st.markdown(f"> *{dato['destino_relaciones']}*")
        else:
            st.info("Sin relaciones conceptuales.")

        # 3. Referencia Visual (Imagen)
        st.markdown("### 📸 Referencia Visual")
        if dato["imagen"]:
            st.image(dato["imagen"], use_container_width=True)
        else:
            st.info("Sin imagen de referencia.")


# ----------------------------------------------------------------------
# VISTA DE BÚSQUEDA (MAIN APP) - Solo la estructura
# ----------------------------------------------------------------------
def mostrar_busqueda():
    st.title("🚧 Glosario de Seguridad Vial")

    tab1, tab2, tab3 = st.tabs(["🔍 Consultar", "➕ Añadir", "⚙️ Gestionar"])

    # PESTAÑA 1: CONSULTAR (Sin cambios, solo muestra el botón de detalle)
    with tab1:
        # Lógica de búsqueda y filtrado (se mantiene igual)
        col_search, col_cat = st.columns([3, 1])
        query = col_search.text_input(
            "Buscar término:", placeholder="Ej: arcén, shoulder..."
        )
        filtro_cat = col_cat.selectbox(
            "Filtrar por Categoría",
            [
                "Todas",
                "General",
                "Señalización",
                "Ingeniería Civil",
                "Sistemas ITS",
                "Legal/Normativa",
            ],
        )

        conn = obtener_conexion()
        sql = "SELECT id, origen_term, destino_term, categoria, origen_lang, destino_lang, contexto, fuente, imagen FROM terminos WHERE (origen_term LIKE ? OR destino_term LIKE ?)"
        params = [f"%{query}%", f"%{query}%"]
        if filtro_cat != "Todas":
            sql += " AND categoria = ?"
            params.append(filtro_cat)
        df = pd.read_sql(sql, conn, params=params)
        conn.close()

        if not df.empty:
            st.success(
                f"Encontrados {len(df)} términos. Haz clic en 'Ver Detalle' para el contexto completo."
            )
            st.divider()

            # Mostramos los resultados como fichas con un botón de detalle
            for index, row in df.iterrows():
                with st.container(border=True):
                    c_texto, c_accion = st.columns([4, 1])

                    with c_texto:
                        st.subheader(f"{row['origen_term']} ➝ {row['destino_term']}")
                        st.caption(
                            f"📂 {row['categoria']} | 🌍 {row['origen_lang']} -> {row['destino_lang']}"
                        )

                    with c_accion:
                        # Botón que, al ser presionado, guarda el ID y recarga la página
                        if st.button("Ver Detalle", key=f"detalle_{row['id']}"):
                            st.session_state["termino_seleccionado_id"] = row["id"]
                            st.rerun()  # Dispara la recarga de la app para mostrar el detalle

        else:
            if query:
                st.warning("No se encontraron resultados.")
            else:
                st.info("Escribe algo para buscar.")

        # Código de exportación se mantiene aquí (opcional)
        st.markdown("### 📥 Descargar Resultados")
        # (El código de descarga de Excel se mantiene igual aquí si es necesario)

    # PESTAÑA 2: AÑADIR (NUEVOS CAMPOS)
    with tab2:
        st.header("Añadir nuevo término")
        with st.form("form_alta"):
            c1, c2, c3 = st.columns(3)
            nuevo_origen = c1.text_input("Término Origen *")
            nuevo_destino = c2.text_input("Término Destino *")
            nueva_categoria = c3.selectbox(
                "Categoría",
                [
                    "General",
                    "Señalización",
                    "Ingeniería Civil",
                    "Sistemas ITS",
                    "Legal/Normativa",
                ],
            )

            c4, c5 = st.columns(2)
            lang_origen = c4.selectbox(
                "Idioma Origen", ["Inglés", "Español", "Francés"], key="l_orig"
            )
            lang_destino = c5.selectbox(
                "Idioma Destino", ["Español", "Inglés", "Francés"], key="l_dest"
            )

            st.markdown("---")
            st.subheader("📝 Definiciones y Contexto")

            # NUEVOS CAMPOS PARA DEFINICIÓN
            def_col_orig, def_col_dest = st.columns(2)
            nueva_origen_definicion = def_col_orig.text_area(
                "Definición Formal (Origen)"
            )
            nueva_destino_definicion = def_col_dest.text_area(
                "Definición Formal (Destino)"
            )

            # CAMPO EXISTENTE (Contexto)
            nuevo_contexto = st.text_area("Contexto de Uso (ej. Frase de ejemplo)")
            nueva_fuente = st.text_input(
                "Fuente de Origen (ej. Manual de Carreteras, DGT)"
            )

            st.markdown("---")
            st.subheader("🗂️ Relaciones Conceptuales (Jerarquías)")

            # NUEVOS CAMPOS PARA RELACIONES
            rel_col_orig, rel_col_dest = st.columns(2)
            nueva_origen_relaciones = rel_col_orig.text_area(
                "Relaciones (Origen, ej. Parte de: X)"
            )
            nueva_destino_relaciones = rel_col_dest.text_area(
                "Relaciones (Destino, ej. Tipo de: Y)"
            )

            st.markdown("---")

            # IMAGEN Y BOTÓN DE GUARDAR
            archivo_imagen = st.file_uploader(
                "📸 Subir imagen (Opcional)", type=["png", "jpg", "jpeg"]
            )

            if st.form_submit_button("Guardar Término Completo"):
                if nuevo_origen and nuevo_destino:
                    blob_imagen = None
                    if archivo_imagen:
                        blob_imagen = archivo_imagen.getvalue()

                    sql = """INSERT INTO terminos (origen_term, destino_term, categoria, origen_lang, destino_lang, contexto, fuente, imagen, origen_definicion, destino_definicion, origen_relaciones, destino_relaciones) 
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

                    ejecutar_consulta(
                        sql,
                        (
                            nuevo_origen,
                            nuevo_destino,
                            nueva_categoria,
                            lang_origen,
                            lang_destino,
                            nuevo_contexto,
                            nueva_fuente,
                            blob_imagen,
                            nueva_origen_definicion,
                            nueva_destino_definicion,
                            nueva_origen_relaciones,
                            nueva_destino_relaciones,
                        ),
                    )
                    st.success(
                        f"✅ '{nuevo_origen}' guardado correctamente con campos avanzados."
                    )
                    st.rerun()
                else:
                    st.error("Faltan campos obligatorios.")

    # PESTAÑA 3: GESTIÓN (MANTENER CÓDIGO ANTERIOR AQUÍ)
    with tab3:
        st.header("Modificar o Eliminar")

        conn = obtener_conexion()
        todos_terminos = pd.read_sql(
            "SELECT id, origen_term, destino_term FROM terminos", conn
        )
        conn.close()

        if not todos_terminos.empty:
            opciones = {
                f"{row['id']} : {row['origen_term']} -> {row['destino_term']}": row[
                    "id"
                ]
                for index, row in todos_terminos.iterrows()
            }
            seleccion = st.selectbox(
                "Selecciona el término a gestionar:", list(opciones.keys())
            )
            id_seleccionado = opciones[seleccion]

            conn = obtener_conexion()
            # Leemos todo para rellenar el formulario
            dato = pd.read_sql(
                "SELECT * FROM terminos WHERE id = ?", conn, params=(id_seleccionado,)
            ).iloc[0]
            conn.close()

            with st.form("form_edicion"):
                st.subheader(f"Editando ID: {id_seleccionado}")
                e_origen = st.text_input("Origen", value=dato["origen_term"])
                e_destino = st.text_input("Destino", value=dato["destino_term"])
                # Nota: La edición de imagen es compleja, de momento permitimos editar texto
                st.info(
                    "ℹ️ Para cambiar la imagen, es mejor borrar y crear de nuevo el término."
                )

                col_del, col_upd = st.columns([1, 4])
                with col_upd:
                    if st.form_submit_button("💾 Actualizar Textos"):
                        ejecutar_consulta(
                            "UPDATE terminos SET origen_term=?, destino_term=? WHERE id=?",
                            (e_origen, e_destino, id_seleccionado),
                        )
                        st.success("Actualizado.")
                        st.rerun()
                with col_del:
                    if st.form_submit_button("🗑️ BORRAR", type="primary"):
                        ejecutar_consulta(
                            "DELETE FROM terminos WHERE id=?", (id_seleccionado,)
                        )
                        st.error("Eliminado.")
                        st.rerun()


# ----------------------------------------------------------------------
# EJECUCIÓN PRINCIPAL DE LA APLICACIÓN (MANTENER SIN CAMBIOS)
# ----------------------------------------------------------------------
if st.session_state["termino_seleccionado_id"] is not None:
    mostrar_detalle_termino(st.session_state["termino_seleccionado_id"])
else:
    mostrar_busqueda()
