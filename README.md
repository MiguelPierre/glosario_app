# 🚧 Glosario Vial Profesional (EN/ES)

## Introducción
Este repositorio contiene el código fuente para el **Glosario Vial Profesional**, una herramienta web (Streamlit) desarrollada para estandarizar la terminología técnica bilingüe (Inglés/Español) utilizada en los proyectos de consultoría de seguridad vial y movilidad.

El objetivo principal es asegurar la **consistencia y calidad** terminológica en toda la documentación y traducciones.

---

## 🚀 Versión y Estado Actual
| Característica | Detalle |
| :--- | :--- |
| **Versión Actual** | **V1.2 - Producción** |
| **Despliegue** | Streamlit Community Cloud |
| **Base de Datos** | SQLite (Persistente) |
| **Funcionalidad Principal** | Búsqueda, Consulta Avanzada y Gestión Completa de la Base de Datos. |

---

## ✨ Características Clave

El glosario soporta la gestión de términos avanzados, incluyendo:

* **Búsqueda Rápida y Filtros:** Consulta por término (origen/destino) y filtrado por categoría (Ingeniería Civil, Señalización, Legal, etc.).
* **Vista de Detalle Profesional:** Al hacer clic en un término, se muestra una ficha completa con:
    * **Definiciones** (Origen y Destino).
    * **Contexto de Uso** (Origen y Destino).
    * **Relaciones Conceptuales** (Jerárquicas y No Jerárquicas).
    * **Referencia Visual** (Imágenes).
* **Gestión Completa de la DB:** Pestañas dedicadas para Añadir, Modificar y Eliminar términos, permitiendo el control total sobre la calidad del contenido.
* **Importación Masiva:** Script de soporte para cargar glosarios preexistentes en formato CSV/Excel.
* **Exportación de Datos:** Opción de exportar los resultados de la búsqueda a un archivo Excel.

---

## ⚙️ Estructura del Proyecto

* `app.py`: El script principal de la aplicación Streamlit. Contiene toda la lógica de la interfaz y las interacciones con la base de datos.
* `glosario.db`: El archivo de base de datos SQLite persistente que almacena todos los términos.
* `requirements.txt`: Lista de dependencias de Python necesarias para el despliegue (Streamlit, pandas, xlsxwriter).
* `importar_csv.py`: Script auxiliar para la carga inicial o masiva de datos desde archivos CSV.
* `update_db_*.py`: Scripts de migración utilizados para expandir el esquema de la base de datos (añadir campos de Definición y Relaciones).

---

## 🛠️ Instalación y Uso Local

Para ejecutar la aplicación localmente (modo `standalone`):

1.  **Clonar el Repositorio:**
    ```bash
    git clone [https://docs.github.com/es/repositories/creating-and-managing-repositories/quickstart-for-repositories](https://docs.github.com/es/repositories/creating-and-managing-repositories/quickstart-for-repositories)
    cd [nombre del repositorio]
    ```
2.  **Instalar Dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Ejecutar la Aplicación:**
    ```bash
    streamlit run app.py
    ```

La aplicación se abrirá automáticamente en tu navegador predeterminado.
