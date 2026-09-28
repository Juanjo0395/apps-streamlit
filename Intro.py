import streamlit as st
from PIL import Image, ImageOps
import json
import os
import uuid


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="AI Portfolio",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CONSTANTES
# ============================================================

CARPETA_DATOS = "datos_apps"
CARPETA_IMAGENES = os.path.join(
    CARPETA_DATOS,
    "imagenes"
)

ARCHIVO_APPS = os.path.join(
    CARPETA_DATOS,
    "apps.json"
)

URL_RECURSOS = (
    "https://sites.google.com/view/"
    "aplicacionesdeia/inicio"
)

EXTENSIONES_PERMITIDAS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp"
}


# ============================================================
# CREAR CARPETAS
# ============================================================

os.makedirs(
    CARPETA_IMAGENES,
    exist_ok=True
)


# ============================================================
# ESTILOS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       PALETA
       ======================================================== */

    :root {
        --bg: #f5f7fb;
        --surface: #ffffff;
        --surface-soft: #f8fafc;

        --navy: #0b1220;
        --navy-2: #111c33;

        --text: #0f172a;
        --muted: #64748b;
        --muted-light: #94a3b8;

        --blue: #2563eb;
        --blue-dark: #1d4ed8;

        --cyan: #06b6d4;
        --cyan-light: #67e8f9;

        --border: #e2e8f0;

        --shadow:
            0 10px 30px rgba(15, 23, 42, 0.07);
    }


    /* ========================================================
       APLICACIÓN
       ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 0%,
                rgba(37, 99, 235, 0.07),
                transparent 25%
            ),
            radial-gradient(
                circle at 95% 5%,
                rgba(6, 182, 212, 0.06),
                transparent 25%
            ),
            var(--bg);
    }


    /* ========================================================
       CONTENEDOR PRINCIPAL
       ======================================================== */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
        max-width: 1450px;
    }


    /* ========================================================
       OCULTAR ELEMENTOS DE STREAMLIT
       ======================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background: var(--navy);
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    section[data-testid="stSidebar"] * {
        color: #dbeafe;
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.10);
    }


    /* ========================================================
       SIDEBAR - MARCA
       ======================================================== */

    .brand-title {
        font-size: 22px;
        font-weight: 800;
        letter-spacing: -0.7px;
        color: #ffffff;
    }

    .brand-title span {
        color: var(--cyan-light);
    }

    .brand-subtitle {
        margin-top: 8px;
        color: #94a3b8;
        font-size: 12px;
        line-height: 1.65;
    }


    /* ========================================================
       SIDEBAR - NAVEGACIÓN
       ======================================================== */

    section[data-testid="stSidebar"]
    div[data-testid="stRadio"] label {
        color: #cbd5e1 !important;
        font-size: 13px;
    }


    /* ========================================================
       HERO
       ======================================================== */

    .hero-box {
        position: relative;
        overflow: hidden;

        padding: 42px 44px;

        border-radius: 24px;

        background:
            linear-gradient(
                135deg,
                #0b1220 0%,
                #111c33 55%,
                #12344d 100%
            );

        box-shadow:
            0 22px 55px
            rgba(15, 23, 42, 0.16);

        margin-bottom: 30px;
    }

    .hero-box::after {
        content: "";

        position: absolute;

        width: 300px;
        height: 300px;

        right: -120px;
        top: -150px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(34,211,238,0.27),
                transparent 67%
            );
    }

    .hero-kicker {
        position: relative;
        z-index: 1;

        color: var(--cyan-light);

        font-size: 11px;
        font-weight: 800;

        letter-spacing: 2.5px;

        text-transform: uppercase;

        margin-bottom: 12px;
    }

    .hero-heading {
        position: relative;
        z-index: 1;

        color: #ffffff;

        font-size: clamp(
            32px,
            4vw,
            52px
        );

        line-height: 1.05;

        font-weight: 850;

        letter-spacing: -2px;

        margin: 0;
    }

    .hero-heading-accent {
        color: var(--cyan-light);
    }

    .hero-text {
        position: relative;
        z-index: 1;

        max-width: 720px;

        margin-top: 17px;

        color: #cbd5e1;

        font-size: 15px;

        line-height: 1.75;
    }


    /* ========================================================
       TÍTULOS
       ======================================================== */

    .section-title {
        color: var(--text);

        font-size: 25px;

        font-weight: 800;

        letter-spacing: -0.7px;

        margin-bottom: 4px;
    }

    .section-description {
        color: var(--muted);

        font-size: 13px;

        margin-bottom: 20px;
    }


    /* ========================================================
       ESTADÍSTICAS
       ======================================================== */

    .stat-label {
        color: var(--muted);

        font-size: 11px;

        font-weight: 800;

        letter-spacing: 1.2px;

        text-transform: uppercase;
    }

    .stat-number {
        color: var(--text);

        font-size: 26px;

        font-weight: 850;

        margin-top: 4px;
    }

    .stat-accent {
        color: var(--blue);
    }


    /* ========================================================
       TARJETAS
       ======================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 18px;
        border-color: rgba(226, 232, 240, 0.95);
        background: rgba(255,255,255,0.96);

        box-shadow:
            0 8px 25px
            rgba(15,23,42,0.055);
    }


    /* ========================================================
       TÍTULO DE APLICACIÓN
       ======================================================== */

    .app-title {
        color: var(--text);

        font-size: 19px;

        font-weight: 800;

        letter-spacing: -0.4px;

        margin-top: 13px;
    }


    /* ========================================================
       DESCRIPCIÓN DE APLICACIÓN
       ======================================================== */

    .app-description {
        color: var(--muted);

        font-size: 13px;

        line-height: 1.65;

        min-height: 65px;

        margin-top: 7px;
    }


    /* ========================================================
       BADGE
       ======================================================== */

    .badge {
        display: inline-block;

        padding: 5px 9px;

        border-radius: 999px;

        background: #eff6ff;

        color: var(--blue);

        font-size: 10px;

        font-weight: 800;

        letter-spacing: 0.8px;

        text-transform: uppercase;

        margin-bottom: 5px;
    }


    /* ========================================================
       BOTONES
       ======================================================== */

    .stLinkButton > button,
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 700 !important;
    }


    /* ========================================================
       ADMINISTRACIÓN
       ======================================================== */

    .admin-header {
        padding: 32px 36px;

        border-radius: 22px;

        background:
            linear-gradient(
                135deg,
                #0b1220,
                #172554
            );

        box-shadow:
            0 18px 45px
            rgba(15,23,42,0.14);

        margin-bottom: 28px;
    }

    .admin-title {
        color: #ffffff;

        font-size: 30px;

        font-weight: 850;

        letter-spacing: -1px;
    }

    .admin-description {
        color: #cbd5e1;

        font-size: 14px;

        line-height: 1.65;

        max-width: 760px;

        margin-top: 7px;
    }


    /* ========================================================
       ADMIN - TÍTULOS
       ======================================================== */

    .panel-title {
        color: var(--text);

        font-size: 19px;

        font-weight: 800;
    }

    .panel-description {
        color: var(--muted);

        font-size: 13px;

        line-height: 1.6;

        margin-top: 4px;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer-line {
        margin-top: 50px;

        padding-top: 20px;

        border-top:
            1px solid var(--border);

        color: var(--muted-light);

        text-align: center;

        font-size: 11px;

        letter-spacing: 0.4px;
    }


    /* ========================================================
       RESPONSIVE
       ======================================================== */

    @media (max-width: 900px) {

        .hero-box {
            padding: 32px 28px;
        }

        .admin-header {
            padding: 28px;
        }
    }


    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FUNCIONES DE DATOS
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

            datos = json.load(archivo)

        if isinstance(datos, list):
            return datos

        return []

    except Exception:

        return []


def guardar_apps(apps):

    os.makedirs(
        CARPETA_DATOS,
        exist_ok=True
    )

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


# ============================================================
# FUNCIONES DE IMÁGENES
# ============================================================

def guardar_imagen(archivo):

    extension = os.path.splitext(
        archivo.name
    )[1].lower()

    if extension not in EXTENSIONES_PERMITIDAS:

        raise ValueError(
            "El formato de imagen no está permitido."
        )

    nombre = (
        f"{uuid.uuid4().hex}"
        f"{extension}"
    )

    ruta = os.path.join(
        CARPETA_IMAGENES,
        nombre
    )

    with open(
        ruta,
        "wb"
    ) as destino:

        destino.write(
            archivo.getbuffer()
        )

    return ruta


def eliminar_imagen(ruta):

    if not ruta:
        return

    if not os.path.exists(ruta):
        return

    try:

        os.remove(ruta)

    except Exception:

        pass


def cargar_imagen(ruta):

    if not ruta:
        return None

    if not os.path.exists(ruta):
        return None

    try:

        return Image.open(ruta)

    except Exception:

        return None


# ============================================================
# CARGAR DATOS
# ============================================================

apps = cargar_apps()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand-title">
            AI<span>·</span>PORTFOLIO
        </div>

        <div class="brand-subtitle">
            Colección de aplicaciones,
            experimentos y proyectos
            desarrollados con inteligencia
            artificial.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        "### Navegación"
    )

    seccion = st.radio(
        "Selecciona una sección",
        [
            "Portafolio",
            "Administración"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown(
        "### Resumen"
    )

    st.metric(
        "Aplicaciones",
        len(apps)
    )

    st.markdown(
        """
        <div class="brand-subtitle">
            Un espacio centralizado para
            presentar proyectos de IA de
            forma clara, profesional y visual.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.link_button(
        "Recursos y ejercicios ↗",
        URL_RECURSOS,
        width="stretch"
    )


# ============================================================
# PORTAFOLIO
# ============================================================

if seccion == "Portafolio":

    # ========================================================
    # HERO
    # ========================================================

    st.markdown(
        """
        <div class="hero-box">

            <div class="hero-kicker">
                AI · DIGITAL PORTFOLIO
            </div>

            <div class="hero-heading">
                Aplicaciones de
                <span class="hero-heading-accent">
                    Inteligencia Artificial
                </span>
            </div>

            <div class="hero-text">
                Explora una colección de aplicaciones
                y proyectos desarrollados para
                experimentar, aprender y resolver
                problemas mediante tecnologías de
                inteligencia artificial.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # ESTADÍSTICAS
    # ========================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        with st.container(border=True):

            st.markdown(
                '<div class="stat-label">Proyectos</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="stat-number">
                    {len(apps)}
                </div>
                """,
                unsafe_allow_html=True
            )


    with col2:

        with st.container(border=True):

            st.markdown(
                '<div class="stat-label">Formato</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div class="stat-number">
                    Web Apps
                </div>
                """,
                unsafe_allow_html=True
            )


    with col3:

        with st.container(border=True):

            st.markdown(
                '<div class="stat-label">Categoría</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div class="stat-number">
                    AI / ML
                </div>
                """,
                unsafe_allow_html=True
            )


    st.write("")


    # ========================================================
    # CABECERA DE PROYECTOS
    # ========================================================

    st.markdown(
        '<div class="section-title">Proyectos</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-description">
            Aplicaciones disponibles para explorar.
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # SIN APLICACIONES
    # ========================================================

    if not apps:

        with st.container(border=True):

            st.markdown(
                "### ◇ Todavía no hay proyectos"
            )

            st.write(
                "Ve a **Administración** para agregar "
                "tu primera aplicación."
            )


    # ========================================================
    # CATÁLOGO
    # ========================================================

    else:

        for inicio in range(
            0,
            len(apps),
            3
        ):

            fila = apps[
                inicio:inicio + 3
            ]

            columnas = st.columns(
                3
            )

            for columna, app in zip(
                columnas,
                fila
            ):

                with columna:

                    # ----------------------------------------
                    # TARJETA
                    # ----------------------------------------

                    with st.container(
                        border=True
                    ):

                        imagen = cargar_imagen(
                            app.get(
                                "imagen",
                                ""
                            )
                        )


                        # ------------------------------------
                        # IMAGEN
                        # ------------------------------------

                        if imagen:

                            st.image(
                                imagen,
                                width="stretch"
                            )

                        else:

                            st.info(
                                "Imagen no disponible"
                            )


                        # ------------------------------------
                        # BADGE
                        # ------------------------------------

                        st.markdown(
                            """
                            <div class="badge">
                                AI PROJECT
                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                        # ------------------------------------
                        # TÍTULO
                        # ------------------------------------

                        st.markdown(
                            f"""
                            <div class="app-title">
                                {app.get(
                                    "titulo",
                                    "Aplicación"
                                )}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                        # ------------------------------------
                        # DESCRIPCIÓN
                        # ------------------------------------

                        st.markdown(
                            f"""
                            <div class="app-description">
                                {app.get(
                                    "descripcion",
                                    ""
                                )}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                        # ------------------------------------
                        # BOTÓN
                        # ------------------------------------

                        url_app = app.get(
                            "url",
                            ""
                        )

                        if url_app:

                            st.link_button(
                                "Abrir aplicación ↗",
                                url_app,
                                width="stretch",
                                type="primary"
                            )


    # ========================================================
    # FOOTER
    # ========================================================

    st.markdown(
        """
        <div class="footer-line">
            AI Portfolio · Aplicaciones y proyectos
            de Inteligencia Artificial
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# ADMINISTRACIÓN
# ============================================================

else:

    # ========================================================
    # CABECERA
    # ========================================================

    st.markdown(
        """
        <div class="admin-header">

            <div class="admin-title">
                Administración del portafolio
            </div>

            <div class="admin-description">
                Gestiona desde aquí las aplicaciones
                que aparecen públicamente en tu
                catálogo. Puedes publicar nuevos
                proyectos o retirar los existentes.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # NUEVA APLICACIÓN
    # ========================================================

    with st.container(border=True):

        st.markdown(
            '<div class="panel-title">Nueva aplicación</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="panel-description">
                Introduce la información que aparecerá
                públicamente en la tarjeta del proyecto.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")


        # ----------------------------------------------------
        # FORMULARIO
        # ----------------------------------------------------

        with st.form(
            "formulario_nueva_app",
            clear_on_submit=True
        ):

            col1, col2 = st.columns(
                [1.5, 1]
            )


            # ------------------------------------------------
            # INFORMACIÓN
            # ------------------------------------------------

            with col1:

                titulo = st.text_input(
                    "Nombre de la aplicación",
                    placeholder=(
                        "Ej. Simulador de datos IoT"
                    )
                )

                descripcion = st.text_area(
                    "Descripción",
                    placeholder=(
                        "Explica brevemente qué hace "
                        "la aplicación y cuál es su propósito."
                    ),
                    height=150
                )

                url = st.text_input(
                    "URL de la aplicación",
                    placeholder=(
                        "https://mi-aplicacion.streamlit.app/"
                    )
                )


            # ------------------------------------------------
            # IMAGEN
            # ------------------------------------------------

            with col2:

                imagen = st.file_uploader(
                    "Imagen / portada",
                    type=[
                        "png",
                        "jpg",
                        "jpeg",
                        "webp"
                    ],
                    help=(
                        "Usa preferiblemente una imagen "
                        "horizontal de buena calidad."
                    )
                )

                st.info(
                    """
                    **Recomendación**

                    Utiliza una captura limpia de la
                    aplicación o una portada diseñada
                    específicamente para representar
                    el proyecto.
                    """
                )


            st.write("")


            # ------------------------------------------------
            # PUBLICAR
            # ------------------------------------------------

            publicar = st.form_submit_button(
                "Publicar aplicación",
                type="primary",
                width="stretch"
            )


    # ========================================================
    # PROCESAR FORMULARIO
    # ========================================================

    if publicar:

        errores = []


        titulo = titulo.strip()

        descripcion = descripcion.strip()

        url = url.strip()


        # ----------------------------------------------------
        # VALIDACIONES
        # ----------------------------------------------------

        if not titulo:

            errores.append(
                "Debes escribir el nombre de la aplicación."
            )


        if not descripcion:

            errores.append(
                "Debes escribir una descripción."
            )


        if not url:

            errores.append(
                "Debes escribir la URL de la aplicación."
            )

        elif not (
            url.startswith("http://")
            or
            url.startswith("https://")
        ):

            errores.append(
                "La URL debe comenzar con "
                "http:// o https://."
            )


        if not imagen:

            errores.append(
                "Debes seleccionar una imagen."
            )


        # ----------------------------------------------------
        # ERRORES
        # ----------------------------------------------------

        if errores:

            for error in errores:

                st.error(
                    error
                )


        # ----------------------------------------------------
        # GUARDAR
        # ----------------------------------------------------

        else:

            try:

                ruta_imagen = guardar_imagen(
                    imagen
                )


                nueva_app = {

                    "id":
                        uuid.uuid4().hex,

                    "titulo":
                        titulo,

                    "descripcion":
                        descripcion,

                    "url":
                        url,

                    "imagen":
                        ruta_imagen

                }


                apps.append(
                    nueva_app
                )


                guardar_apps(
                    apps
                )


                st.success(
                    "Aplicación publicada correctamente."
                )


                st.rerun()


            except Exception as error:

                st.error(
                    "No fue posible publicar "
                    f"la aplicación: {error}"
                )


    st.write("")
    st.write("")


    # ========================================================
    # APLICACIONES PUBLICADAS
    # ========================================================

    with st.container(border=True):

        st.markdown(
            '<div class="panel-title">Aplicaciones publicadas</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="panel-description">
                Revisa las aplicaciones actualmente
                visibles en tu portafolio.
            </div>
            """,
            unsafe_allow_html=True
        )


        st.write("")


        # ----------------------------------------------------
        # VACÍO
        # ----------------------------------------------------

        if not apps:

            st.info(
                "No hay aplicaciones publicadas todavía."
            )


        # ----------------------------------------------------
        # LISTA
        # ----------------------------------------------------

        else:

            for indice, app in enumerate(apps):

                col1, col2, col3 = st.columns(
                    [1.2, 5, 1]
                )


                # --------------------------------------------
                # IMAGEN
                # --------------------------------------------

                with col1:

                    imagen_preview = cargar_imagen(
                        app.get(
                            "imagen",
                            ""
                        )
                    )

                    if imagen_preview:

                        st.image(
                            imagen_preview,
                            width=110
                        )

                    else:

                        st.caption(
                            "Sin imagen"
                        )


                # --------------------------------------------
                # INFORMACIÓN
                # --------------------------------------------

                with col2:

                    st.markdown(
                        f"**{app.get('titulo', 'Sin título')}**"
                    )

                    st.caption(
                        app.get(
                            "url",
                            "Sin URL"
                        )
                    )


                    st.caption(
                        app.get(
                            "descripcion",
                            ""
                        )
                    )


                # --------------------------------------------
                # ELIMINAR
                # --------------------------------------------

                with col3:

                    eliminar = st.button(
                        "Eliminar",
                        key=(
                            f"eliminar_"
                            f"{app.get('id', indice)}"
                        ),
                        type="secondary",
                        width="stretch"
                    )


                    if eliminar:

                        eliminar_imagen(
                            app.get(
                                "imagen",
                                ""
                            )
                        )


                        apps = [
                            item

                            for item in apps

                            if item.get("id")
                            != app.get("id")
                        ]


                        guardar_apps(
                            apps
                        )


                        st.success(
                            "Aplicación eliminada."
                        )


                        st.rerun()


    # ========================================================
    # FOOTER
    # ========================================================

    st.markdown(
        """
        <div class="footer-line">
            Panel de administración · AI Portfolio
        </div>
        """,
        unsafe_allow_html=True
    )
