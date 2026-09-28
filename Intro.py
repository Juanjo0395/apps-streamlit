import streamlit as st
from PIL import Image
import json
import os
import uuid
import base64


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Aplicaciones de Inteligencia Artificial",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# CARPETAS Y ARCHIVOS
# ============================================================

CARPETA_DATOS = "datos_apps"
CARPETA_IMAGENES = os.path.join(CARPETA_DATOS, "imagenes")
ARCHIVO_APPS = os.path.join(CARPETA_DATOS, "apps.json")

os.makedirs(CARPETA_IMAGENES, exist_ok=True)


# ============================================================
# ESTILOS
# ============================================================

st.markdown("""
<style>

    /* -------------------------------------------------------
       FONDO GENERAL
    ------------------------------------------------------- */

    .stApp {
        background-color: #f7f8fa;
    }


    /* -------------------------------------------------------
       TÍTULO PRINCIPAL
    ------------------------------------------------------- */

    .titulo-principal {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        color: #1f2937;
        margin-top: 10px;
        margin-bottom: 5px;
    }


    .subtitulo-principal {
        text-align: center;
        font-size: 18px;
        color: #6b7280;
        margin-bottom: 35px;
    }


    /* -------------------------------------------------------
       TARJETAS
    ------------------------------------------------------- */

    .app-card {
        background-color: white;
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 25px;

        box-shadow:
            0px 4px 15px rgba(0,0,0,0.08);

        border: 1px solid #eeeeee;

        min-height: 450px;

        transition: all 0.2s ease;
    }


    .app-card:hover {
        box-shadow:
            0px 8px 25px rgba(0,0,0,0.13);

        transform: translateY(-2px);
    }


    /* -------------------------------------------------------
       TÍTULO DE CADA APP
    ------------------------------------------------------- */

    .app-title {
        font-size: 21px;
        font-weight: 700;
        color: #1f2937;
        margin-top: 12px;
        margin-bottom: 8px;
    }


    /* -------------------------------------------------------
       DESCRIPCIÓN
    ------------------------------------------------------- */

    .app-description {
        font-size: 15px;
        color: #4b5563;
        line-height: 1.55;

        min-height: 72px;

        margin-bottom: 12px;
    }


    /* -------------------------------------------------------
       BOTÓN DE LA APP
    ------------------------------------------------------- */

    .app-button {
        display: inline-block;

        background-color: #ff4b4b;

        color: white !important;

        padding: 9px 18px;

        border-radius: 8px;

        text-decoration: none !important;

        font-weight: 600;

        margin-top: 5px;
    }


    .app-button:hover {
        background-color: #e63939;
        color: white !important;
    }


    /* -------------------------------------------------------
       CAJA DE ADMINISTRACIÓN
    ------------------------------------------------------- */

    .admin-box {
        background-color: white;

        border-radius: 15px;

        padding: 20px;

        border: 1px solid #e5e7eb;

        margin-bottom: 25px;
    }


    /* -------------------------------------------------------
       INFORMACIÓN
    ------------------------------------------------------- */

    .info-box {
        background-color: #eef6ff;

        border-left: 5px solid #3b82f6;

        padding: 15px;

        border-radius: 8px;

        margin-bottom: 20px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# FUNCIONES
# ============================================================

def cargar_apps():

    if not os.path.exists(ARCHIVO_APPS):
        return []

    try:

        with open(
            ARCHIVO_APPS,
            "r",
            encoding="utf-8"
        ) as archivo:

            return json.load(archivo)

    except Exception:
        return []


def guardar_apps(apps):

    os.makedirs(CARPETA_DATOS, exist_ok=True)

    with open(
        ARCHIVO_APPS,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            apps,
            archivo,
            ensure_ascii=False,
            indent=4
        )


def guardar_imagen(archivo):

    extension = os.path.splitext(
        archivo.name
    )[1].lower()

    nombre = f"{uuid.uuid4().hex}{extension}"

    ruta = os.path.join(
        CARPETA_IMAGENES,
        nombre
    )

    with open(ruta, "wb") as f:
        f.write(archivo.getbuffer())

    return ruta


def eliminar_imagen(ruta):

    if os.path.exists(ruta):

        try:
            os.remove(ruta)
        except:
            pass


# ============================================================
# CARGAR APLICACIONES
# ============================================================

apps = cargar_apps()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🤖 Catálogo de IA")

    st.write(
        """
        Desde este espacio puedes administrar
        tus aplicaciones de Inteligencia Artificial.
        """
    )

    st.divider()

    st.subheader("📊 Información")

    st.write(
        f"Aplicaciones registradas: **{len(apps)}**"
    )

    st.divider()

    st.subheader("📚 Recursos")

    url_recursos = (
        "https://sites.google.com/view/"
        "aplicacionesdeia/inicio"
    )

    st.markdown(
        f"[🔗 Páginas y ejercicios]({url_recursos})"
    )


# ============================================================
# TÍTULO
# ============================================================

st.markdown(
    """
    <div class="titulo-principal">
        Aplicaciones de Inteligencia Artificial 🤖
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitulo-principal">
        Explora mis aplicaciones y proyectos desarrollados
        con Inteligencia Artificial.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ADMINISTRACIÓN
# ============================================================

with st.expander(
    "⚙️ Administrar aplicaciones",
    expanded=False
):

    st.markdown(
        """
        <div class="info-box">

        <b>Agregar una nueva aplicación</b>

        <br><br>

        Completa los campos siguientes y la aplicación
        aparecerá automáticamente en el catálogo.

        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # FORMULARIO
    # --------------------------------------------------------

    with st.form(
        "formulario_nueva_app",
        clear_on_submit=True
    ):

        st.subheader("➕ Nueva aplicación")

        titulo = st.text_input(
            "Título de la aplicación",
            placeholder="Ejemplo: Análisis de imágenes"
        )

        descripcion = st.text_area(
            "Descripción",
            placeholder=(
                "Escribe una breve descripción "
                "de lo que hace tu aplicación..."
            ),
            height=100
        )

        url = st.text_input(
            "Enlace de la aplicación",
            placeholder=(
                "https://mi-aplicacion.streamlit.app/"
            )
        )

        imagen = st.file_uploader(
            "Imagen de la aplicación",
            type=[
                "png",
                "jpg",
                "jpeg",
                "webp"
            ],
            help=(
                "Sube una imagen que represente "
                "tu aplicación."
            )
        )

        st.write("")

        agregar = st.form_submit_button(
            "🚀 Agregar aplicación",
            use_container_width=True
        )


    # --------------------------------------------------------
    # PROCESAR FORMULARIO
    # --------------------------------------------------------

    if agregar:

        errores = []

        if not titulo.strip():
            errores.append(
                "Debes escribir un título."
            )

        if not descripcion.strip():
            errores.append(
                "Debes escribir una descripción."
            )

        if not url.strip():
            errores.append(
                "Debes escribir el enlace."
            )

        if not imagen:
            errores.append(
                "Debes subir una imagen."
            )


        # ----------------------------------------------------
        # VALIDAR URL
        # ----------------------------------------------------

        if url.strip():

            if not (
                url.startswith("http://")
                or
                url.startswith("https://")
            ):

                errores.append(
                    "El enlace debe comenzar con "
                    "http:// o https://"
                )


        # ----------------------------------------------------
        # MOSTRAR ERRORES
        # ----------------------------------------------------

        if errores:

            for error in errores:
                st.error(error)


        # ----------------------------------------------------
        # GUARDAR
        # ----------------------------------------------------

        else:

            try:

                ruta_imagen = guardar_imagen(imagen)

                nueva_app = {

                    "id": uuid.uuid4().hex,

                    "titulo": titulo.strip(),

                    "descripcion":
                        descripcion.strip(),

                    "url":
                        url.strip(),

                    "imagen":
                        ruta_imagen

                }

                apps.append(nueva_app)

                guardar_apps(apps)

                st.success(
                    "✅ Aplicación agregada correctamente."
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"No fue posible guardar la aplicación: {e}"
                )


# ============================================================
# ADMINISTRAR APLICACIONES EXISTENTES
# ============================================================

if len(apps) > 0:

    with st.expander(
        "🗑️ Eliminar aplicaciones",
        expanded=False
    ):

        st.warning(
            "Atención: al eliminar una aplicación "
            "también se eliminará su imagen."
        )

        for app in apps:

            col1, col2 = st.columns(
                [5, 1]
            )

            with col1:

                st.write(
                    f"**{app['titulo']}**"
                )

            with col2:

                eliminar = st.button(
                    "🗑️",
                    key=f"eliminar_{app['id']}"
                )

                if eliminar:

                    eliminar_imagen(
                        app["imagen"]
                    )

                    apps = [
                        a for a in apps
                        if a["id"] != app["id"]
                    ]

                    guardar_apps(apps)

                    st.success(
                        "Aplicación eliminada."
                    )

                    st.rerun()


# ============================================================
# CATÁLOGO
# ============================================================

if len(apps) == 0:

    st.info(
        """
        📭 Todavía no tienes aplicaciones.

        Abre **⚙️ Administrar aplicaciones** para
        agregar tu primera aplicación.
        """
    )


else:

    # --------------------------------------------------------
    # CREAR FILAS DE 3 APLICACIONES
    # --------------------------------------------------------

    for i in range(
        0,
        len(apps),
        3
    ):

        fila = apps[
            i:i + 3
        ]

        columnas = st.columns(
            3
        )


        for columna, app in zip(
            columnas,
            fila
        ):

            with columna:

                # --------------------------------------------
                # TARJETA
                # --------------------------------------------

                st.markdown(
                    '<div class="app-card">',
                    unsafe_allow_html=True
                )


                # --------------------------------------------
                # IMAGEN
                # --------------------------------------------

                try:

                    if os.path.exists(
                        app["imagen"]
                    ):

                        imagen = Image.open(
                            app["imagen"]
                        )

                        st.image(
                            imagen,
                            use_container_width=True
                        )

                    else:

                        st.info(
                            "Imagen no disponible"
                        )

                except Exception:

                    st.warning(
                        "No se pudo cargar la imagen."
                    )


                # --------------------------------------------
                # TÍTULO
                # --------------------------------------------

                st.markdown(
                    f"""
                    <div class="app-title">
                        {app["titulo"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # --------------------------------------------
                # DESCRIPCIÓN
                # --------------------------------------------

                st.markdown(
                    f"""
                    <div class="app-description">
                        {app["descripcion"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # --------------------------------------------
                # ENLACE
                # --------------------------------------------

                st.markdown(
                    f"""
                    <a
                        href="{app["url"]}"
                        target="_blank"
                        class="app-button"
                    >
                        🚀 Abrir aplicación
                    </a>
                    """,
                    unsafe_allow_html=True
                )


                # --------------------------------------------
                # CERRAR TARJETA
                # --------------------------------------------

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )


# ============================================================
# PIE DE PÁGINA
# ============================================================

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        color:#777;
        padding:15px;
    ">

        🤖 Catálogo de aplicaciones de Inteligencia Artificial

    </div>
    """,
    unsafe_allow_html=True
)
