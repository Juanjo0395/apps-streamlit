import streamlit as st
from PIL import Image
import json
import os
import uuid
import base64
import mimetypes
import html
import textwrap


# ============================================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ============================================================

st.set_page_config(
    page_title="AI Portfolio",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CARPETAS Y ARCHIVOS
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

    /* ======================================================
       VARIABLES
       ====================================================== */

    :root {
        --bg: #f4f7fb;
        --surface: #ffffff;
        --surface-soft: #f8fafc;

        --text: #0f172a;
        --text-secondary: #64748b;

        --primary: #2563eb;
        --primary-dark: #1d4ed8;
        --cyan: #06b6d4;

        --border: #e2e8f0;

        --shadow:
            0 10px 35px rgba(15, 23, 42, 0.08);

        --shadow-hover:
            0 18px 45px rgba(15, 23, 42, 0.14);
    }


    /* ======================================================
       APLICACIÓN
       ====================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 15% 0%,
                rgba(37, 99, 235, 0.07),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(6, 182, 212, 0.06),
                transparent 25%
            ),
            var(--bg);
    }


    /* ======================================================
       OCULTAR ELEMENTOS DE STREAMLIT
       ====================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* ======================================================
       SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"] {
        background: #0b1220;
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    section[data-testid="stSidebar"] * {
        color: #dbeafe;
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.10);
    }


    /* ======================================================
       MARCA DEL SIDEBAR
       ====================================================== */

    .sidebar-brand {
        padding: 10px 4px 22px 4px;
    }

    .sidebar-brand-title {
        color: white;
        font-size: 22px;
        font-weight: 750;
        letter-spacing: -0.5px;
    }

    .sidebar-brand-title span {
        color: #22d3ee;
    }

    .sidebar-brand-subtitle {
        color: #94a3b8;
        font-size: 13px;
        line-height: 1.5;
        margin-top: 6px;
    }


    /* ======================================================
       HERO PRINCIPAL
       ====================================================== */

    .hero {
        position: relative;
        overflow: hidden;

        padding: 46px 48px;

        margin-bottom: 34px;

        border-radius: 24px;

        background:
            linear-gradient(
                135deg,
                #0b1220 0%,
                #111c33 55%,
                #12304a 100%
            );

        box-shadow:
            0 20px 50px rgba(15, 23, 42, 0.16);
    }

    .hero::before {
        content: "";

        position: absolute;

        width: 260px;
        height: 260px;

        right: -80px;
        top: -120px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(34, 211, 238, 0.30),
                transparent 65%
            );
    }

    .hero::after {
        content: "";

        position: absolute;

        width: 180px;
        height: 180px;

        left: 45%;
        bottom: -130px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(37, 99, 235, 0.25),
                transparent 70%
            );
    }

    .hero-label {
        position: relative;
        z-index: 2;

        display: inline-block;

        color: #67e8f9;

        font-size: 12px;
        font-weight: 700;

        letter-spacing: 2px;
        text-transform: uppercase;

        margin-bottom: 12px;
    }

    .hero-title {
        position: relative;
        z-index: 2;

        color: white;

        font-size: clamp(32px, 4vw, 52px);

        line-height: 1.05;

        font-weight: 800;

        letter-spacing: -1.8px;

        margin: 0;
    }

    .hero-title span {
        color: #22d3ee;
    }

    .hero-description {
        position: relative;
        z-index: 2;

        max-width: 720px;

        color: #cbd5e1;

        font-size: 16px;
        line-height: 1.7;

        margin-top: 17px;
        margin-bottom: 0;
    }


    /* ======================================================
       ENCABEZADOS DE SECCIÓN
       ====================================================== */

    .section-header {
        display: flex;

        align-items: flex-end;

        justify-content: space-between;

        margin-bottom: 18px;
    }

    .section-title {
        color: var(--text);

        font-size: 25px;

        font-weight: 750;

        letter-spacing: -0.6px;

        margin: 0;
    }

    .section-description {
        color: var(--text-secondary);

        font-size: 14px;

        margin-top: 5px;
    }


    /* ======================================================
       ESTADÍSTICAS
       ====================================================== */

    .stats-grid {
        display: grid;

        grid-template-columns:
            repeat(3, 1fr);

        gap: 14px;

        margin-bottom: 34px;
    }

    .stat-card {
        background: rgba(255,255,255,0.85);

        border: 1px solid var(--border);

        border-radius: 16px;

        padding: 18px 20px;

        box-shadow:
            0 5px 20px rgba(15,23,42,0.04);
    }

    .stat-label {
        color: #64748b;

        font-size: 12px;

        text-transform: uppercase;

        letter-spacing: 1px;

        font-weight: 700;
    }

    .stat-value {
        color: var(--text);

        font-size: 27px;

        font-weight: 800;

        margin-top: 4px;
    }


    /* ======================================================
       GRID DEL PORTAFOLIO
       ====================================================== */

    .portfolio-grid {
        display: grid;

        grid-template-columns:
            repeat(3, minmax(0, 1fr));

        gap: 24px;

        align-items: stretch;

        margin-bottom: 24px;
    }


    /* ======================================================
       TARJETA DE APLICACIÓN
       ====================================================== */

    .portfolio-card {
        display: flex;

        flex-direction: column;

        overflow: hidden;

        min-width: 0;

        background: var(--surface);

        border:
            1px solid rgba(226, 232, 240, 0.95);

        border-radius: 20px;

        box-shadow: var(--shadow);

        transition:
            transform 0.25s ease,
            box-shadow 0.25s ease,
            border-color 0.25s ease;
    }

    .portfolio-card:hover {
        transform: translateY(-5px);

        box-shadow: var(--shadow-hover);

        border-color:
            rgba(37,99,235,0.20);
    }


    /* ======================================================
       IMAGEN DE LA TARJETA
       ====================================================== */

    .portfolio-image-wrapper {
        position: relative;

        width: 100%;

        height: 205px;

        overflow: hidden;

        background:
            linear-gradient(
                135deg,
                #e2e8f0,
                #f8fafc
            );
    }

    .portfolio-image {
        width: 100%;
        height: 100%;

        object-fit: cover;

        display: block;

        transition:
            transform 0.35s ease;
    }

    .portfolio-card:hover
    .portfolio-image {
        transform: scale(1.035);
    }


    /* ======================================================
       BADGE
       ====================================================== */

    .portfolio-badge {
        position: absolute;

        top: 14px;
        left: 14px;

        padding: 6px 10px;

        border-radius: 999px;

        background:
            rgba(11, 18, 32, 0.82);

        backdrop-filter: blur(8px);

        color: #e0f2fe;

        font-size: 10px;

        font-weight: 700;

        letter-spacing: 1px;

        text-transform: uppercase;
    }


    /* ======================================================
       CONTENIDO DE TARJETA
       ====================================================== */

    .portfolio-content {
        display: flex;

        flex-direction: column;

        flex: 1;

        padding:
            21px
            21px
            20px
            21px;
    }

    .portfolio-title {
        color: var(--text);

        font-size: 19px;

        line-height: 1.3;

        font-weight: 750;

        margin-bottom: 9px;
    }

    .portfolio-description {
        color: #64748b;

        font-size: 14px;

        line-height: 1.6;

        display: -webkit-box;

        -webkit-line-clamp: 4;

        -webkit-box-orient: vertical;

        overflow: hidden;

        min-height: 90px;

        margin-bottom: 20px;
    }


    /* ======================================================
       FOOTER DE TARJETA
       ====================================================== */

    .portfolio-footer {
        margin-top: auto;
    }


    /* ======================================================
       BOTÓN DE APLICACIÓN
       ====================================================== */

    .portfolio-button {
        display: flex;

        align-items: center;

        justify-content: center;

        width: 100%;

        box-sizing: border-box;

        padding: 11px 16px;

        border-radius: 11px;

        background:
            linear-gradient(
                135deg,
                #2563eb,
                #0891b2
            );

        color: white !important;

        text-decoration: none !important;

        font-size: 13px;

        font-weight: 700;

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .portfolio-button:hover {
        color: white !important;

        transform: translateY(-1px);

        box-shadow:
            0 8px 20px
            rgba(37,99,235,0.25);
    }


    /* ======================================================
       ESTADO VACÍO
       ====================================================== */

    .empty-state {
        padding: 65px 30px;

        text-align: center;

        background: white;

        border:
            1px dashed #cbd5e1;

        border-radius: 20px;
    }

    .empty-icon {
        font-size: 32px;

        color: #94a3b8;

        margin-bottom: 10px;
    }

    .empty-title {
        color: var(--text);

        font-size: 20px;

        font-weight: 750;
    }

    .empty-description {
        color: #64748b;

        font-size: 14px;

        margin-top: 5px;
    }


    /* ======================================================
       ADMINISTRACIÓN
       ====================================================== */

    .admin-hero {
        background:
            linear-gradient(
                135deg,
                #0b1220,
                #172554
            );

        border-radius: 22px;

        padding: 32px;

        color: white;

        margin-bottom: 26px;

        box-shadow:
            0 16px 40px
            rgba(15,23,42,0.14);
    }

    .admin-hero-title {
        font-size: 29px;

        font-weight: 800;

        letter-spacing: -0.8px;
    }

    .admin-hero-description {
        color: #cbd5e1;

        font-size: 14px;

        line-height: 1.6;

        max-width: 700px;

        margin-top: 7px;
    }


    /* ======================================================
       PANEL ADMINISTRATIVO
       ====================================================== */

    .admin-panel {
        background: white;

        border:
            1px solid var(--border);

        border-radius: 20px;

        padding: 26px;

        box-shadow:
            0 8px 30px
            rgba(15,23,42,0.05);

        margin-bottom: 22px;
    }

    .admin-panel-title {
        color: var(--text);

        font-size: 18px;

        font-weight: 750;

        margin-bottom: 4px;
    }

    .admin-panel-description {
        color: #64748b;

        font-size: 13px;

        margin-bottom: 20px;
    }


    /* ======================================================
       PIE DE PÁGINA
       ====================================================== */

    .footer {
        margin-top: 55px;

        padding: 25px 0;

        border-top:
            1px solid #e2e8f0;

        text-align: center;

        color: #94a3b8;

        font-size: 12px;

        letter-spacing: 0.3px;
    }


    /* ======================================================
       RESPONSIVE
       ====================================================== */

    @media (max-width: 1000px) {

        .portfolio-grid {
            grid-template-columns:
                repeat(2, minmax(0, 1fr));
        }

    }


    @media (max-width: 700px) {

        .hero {
            padding: 32px 25px;
        }

        .portfolio-grid {
            grid-template-columns: 1fr;
        }

        .stats-grid {
            grid-template-columns: 1fr;
        }

    }

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# FUNCIÓN PARA RENDERIZAR HTML
# ============================================================

def render_html(contenido):
    """
    Renderiza HTML eliminando automáticamente
    la indentación del código multilínea.

    Esto evita que Streamlit interprete los
    bloques HTML como código Markdown.
    """

    contenido_limpio = textwrap.dedent(
        contenido
    ).strip()

    st.markdown(
        contenido_limpio,
        unsafe_allow_html=True
    )


# ============================================================
# FUNCIONES DE DATOS
# ============================================================

def cargar_apps():

    if not os.path.exists(
        ARCHIVO_APPS
    ):
        return []

    try:

        with open(
            ARCHIVO_APPS,
            "r",
            encoding="utf-8"
        ) as archivo:

            datos = json.load(
                archivo
            )

            if isinstance(
                datos,
                list
            ):
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

    extensiones_permitidas = [
        ".png",
        ".jpg",
        ".jpeg",
        ".webp"
    ]

    if extension not in extensiones_permitidas:

        raise ValueError(
            "Formato de imagen no permitido."
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
    ) as f:

        f.write(
            archivo.getbuffer()
        )

    return ruta


def eliminar_imagen(ruta):

    if not ruta:
        return

    if os.path.exists(ruta):

        try:

            os.remove(ruta)

        except Exception:

            pass


def imagen_a_base64(ruta):

    if not ruta:
        return None

    if not os.path.exists(ruta):
        return None

    try:

        with open(
            ruta,
            "rb"
        ) as archivo:

            contenido = base64.b64encode(
                archivo.read()
            ).decode("utf-8")

        mime = (
            mimetypes.guess_type(
                ruta
            )[0]
            or "image/jpeg"
        )

        return (
            f"data:{mime};base64,"
            f"{contenido}"
        )

    except Exception:

        return None


# ============================================================
# SEGURIDAD PARA HTML
# ============================================================

def limpiar(texto):

    return html.escape(
        str(texto),
        quote=True
    )


# ============================================================
# CARGAR APLICACIONES
# ============================================================

apps = cargar_apps()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    render_html(
        """
        <div class="sidebar-brand">

            <div class="sidebar-brand-title">
                AI<span>·</span>PORTFOLIO
            </div>

            <div class="sidebar-brand-subtitle">
                Colección de aplicaciones,
                experimentos y proyectos
                desarrollados con inteligencia
                artificial.
            </div>

        </div>
        """
    )

    st.divider()

    st.markdown(
        "### Navegación"
    )

    seccion = st.radio(
        "Sección",
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

    render_html(
        """
        <div style="
            color:#94a3b8;
            font-size:12px;
            line-height:1.6;
            margin-top:12px;
        ">
            Un espacio centralizado para
            presentar proyectos de IA de
            forma clara, profesional y visual.
        </div>
        """
    )

    st.divider()

    url_recursos = (
        "https://sites.google.com/view/"
        "aplicacionesdeia/inicio"
    )

    render_html(
        f"""
        <a
            href="{url_recursos}"
            target="_blank"
            rel="noopener noreferrer"
            style="
                color:#67e8f9;
                text-decoration:none;
                font-size:13px;
                font-weight:600;
            "
        >
            Recursos y ejercicios ↗
        </a>
        """
    )


# ============================================================
# SECCIÓN: PORTAFOLIO
# ============================================================

if seccion == "Portafolio":

    # ========================================================
    # HERO
    # ========================================================

    render_html(
        """
        <div class="hero">

            <div class="hero-label">
                AI · DIGITAL PORTFOLIO
            </div>

            <h1 class="hero-title">
                Aplicaciones de
                <span>Inteligencia Artificial</span>
            </h1>

            <p class="hero-description">
                Explora una colección de aplicaciones
                y proyectos desarrollados para
                experimentar, aprender y resolver
                problemas mediante tecnologías de
                inteligencia artificial.
            </p>

        </div>
        """
    )


    # ========================================================
    # ESTADÍSTICAS
    # ========================================================

    render_html(
        f"""
        <div class="stats-grid">

            <div class="stat-card">

                <div class="stat-label">
                    Proyectos
                </div>

                <div class="stat-value">
                    {len(apps)}
                </div>

            </div>


            <div class="stat-card">

                <div class="stat-label">
                    Formato
                </div>

                <div class="stat-value">
                    Web Apps
                </div>

            </div>


            <div class="stat-card">

                <div class="stat-label">
                    Categoría
                </div>

                <div class="stat-value">
                    AI / ML
                </div>

            </div>

        </div>
        """
    )


    # ========================================================
    # ENCABEZADO DE PROYECTOS
    # ========================================================

    render_html(
        """
        <div class="section-header">

            <div>

                <div class="section-title">
                    Proyectos
                </div>

                <div class="section-description">
                    Aplicaciones disponibles para explorar.
                </div>

            </div>

        </div>
        """
    )


    # ========================================================
    # PORTAFOLIO VACÍO
    # ========================================================

    if len(apps) == 0:

        render_html(
            """
            <div class="empty-state">

                <div class="empty-icon">
                    ◇
                </div>

                <div class="empty-title">
                    Todavía no hay proyectos
                </div>

                <div class="empty-description">
                    Ve a la sección Administración
                    para agregar tu primera aplicación.
                </div>

            </div>
            """
        )


    # ========================================================
    # MOSTRAR APLICACIONES
    # ========================================================

    else:

        tarjetas = []


        for app in apps:

            titulo = limpiar(
                app.get(
                    "titulo",
                    "Aplicación"
                )
            )

            descripcion = limpiar(
                app.get(
                    "descripcion",
                    ""
                )
            )

            url = limpiar(
                app.get(
                    "url",
                    "#"
                )
            )

            ruta_imagen = app.get(
                "imagen",
                ""
            )


            # ------------------------------------------------
            # IMAGEN
            # ------------------------------------------------

            imagen_base64 = imagen_a_base64(
                ruta_imagen
            )


            if imagen_base64:

                imagen_html = f"""
                    <img
                        class="portfolio-image"
                        src="{imagen_base64}"
                        alt="{titulo}"
                    >
                """

            else:

                imagen_html = """
                    <div style="
                        width:100%;
                        height:100%;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        color:#94a3b8;
                        font-size:13px;
                    ">
                        Imagen no disponible
                    </div>
                """


            # ------------------------------------------------
            # TARJETA COMPLETA
            # ------------------------------------------------

            tarjeta = f"""
            <div class="portfolio-card">

                <div class="portfolio-image-wrapper">

                    {imagen_html}

                    <div class="portfolio-badge">
                        AI PROJECT
                    </div>

                </div>


                <div class="portfolio-content">

                    <div class="portfolio-title">
                        {titulo}
                    </div>


                    <div class="portfolio-description">
                        {descripcion}
                    </div>


                    <div class="portfolio-footer">

                        <a
                            href="{url}"
                            target="_blank"
                            rel="noopener noreferrer"
                            class="portfolio-button"
                        >
                            Abrir aplicación

                            <span style="
                                margin-left:8px;
                            ">
                                ↗
                            </span>

                        </a>

                    </div>

                </div>

            </div>
            """

            tarjetas.append(
                tarjeta
            )


        # ====================================================
        # CREAR GRID DE 3 TARJETAS
        # ====================================================

        for i in range(
            0,
            len(tarjetas),
            3
        ):

            fila = tarjetas[
                i:i + 3
            ]


            contenido_grid = (
                """
                <div class="portfolio-grid">
                """
                +
                "".join(fila)
                +
                """
                </div>
                """
            )


            render_html(
                contenido_grid
            )


    # ========================================================
    # FOOTER
    # ========================================================

    render_html(
        """
        <div class="footer">
            AI Portfolio · Aplicaciones y
            proyectos de Inteligencia Artificial
        </div>
        """
    )


# ============================================================
# SECCIÓN: ADMINISTRACIÓN
# ============================================================

else:

    # ========================================================
    # HERO ADMINISTRACIÓN
    # ========================================================

    render_html(
        """
        <div class="admin-hero">

            <div class="admin-hero-title">
                Administración del portafolio
            </div>

            <div class="admin-hero-description">
                Gestiona las aplicaciones que aparecen
                en tu catálogo. Desde aquí puedes añadir
                nuevos proyectos o eliminar los que ya
                no quieras mostrar.
            </div>

        </div>
        """
    )


    # ========================================================
    # PANEL NUEVA APLICACIÓN
    # ========================================================

    render_html(
        """
        <div class="admin-panel">

            <div class="admin-panel-title">
                Nueva aplicación
            </div>

            <div class="admin-panel-description">
                Introduce la información que aparecerá
                públicamente en la tarjeta del proyecto.
            </div>

        </div>
        """
    )


    # ========================================================
    # FORMULARIO
    # ========================================================

    with st.form(
        "formulario_nueva_app",
        clear_on_submit=True
    ):

        col1, col2 = st.columns(
            [1.4, 1]
        )


        # ----------------------------------------------------
        # INFORMACIÓN
        # ----------------------------------------------------

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
                height=140
            )

            url = st.text_input(
                "URL de la aplicación",
                placeholder=(
                    "https://mi-aplicacion.streamlit.app/"
                )
            )


        # ----------------------------------------------------
        # IMAGEN
        # ----------------------------------------------------

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
                    "Preferiblemente utiliza una "
                    "imagen horizontal de buena calidad."
                )
            )


            render_html(
                """
                <div style="
                    background:#f8fafc;
                    border:1px solid #e2e8f0;
                    border-radius:12px;
                    padding:14px;
                    margin-top:12px;
                    color:#64748b;
                    font-size:12px;
                    line-height:1.6;
                ">

                    <strong style="
                        color:#334155;
                    ">
                        Recomendación
                    </strong>

                    <br>

                    Utiliza capturas limpias de tu
                    aplicación o una portada diseñada
                    específicamente para representar
                    el proyecto.

                </div>
                """
            )


        st.write("")


        # ----------------------------------------------------
        # BOTÓN PUBLICAR
        # ----------------------------------------------------

        agregar = st.form_submit_button(
            "Publicar aplicación",
            type="primary",
            use_container_width=True
        )


    # ========================================================
    # PROCESAR FORMULARIO
    # ========================================================

    if agregar:

        errores = []


        # ----------------------------------------------------
        # LIMPIAR DATOS
        # ----------------------------------------------------

        titulo = titulo.strip()

        descripcion = descripcion.strip()

        url = url.strip()


        # ----------------------------------------------------
        # VALIDAR TÍTULO
        # ----------------------------------------------------

        if not titulo:

            errores.append(
                "Debes escribir el nombre de la aplicación."
            )


        # ----------------------------------------------------
        # VALIDAR DESCRIPCIÓN
        # ----------------------------------------------------

        if not descripcion:

            errores.append(
                "Debes escribir una descripción."
            )


        # ----------------------------------------------------
        # VALIDAR URL
        # ----------------------------------------------------

        if not url:

            errores.append(
                "Debes escribir la URL."
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


        # ----------------------------------------------------
        # VALIDAR IMAGEN
        # ----------------------------------------------------

        if not imagen:

            errores.append(
                "Debes seleccionar una imagen."
            )


        # ====================================================
        # MOSTRAR ERRORES
        # ====================================================

        if errores:

            for error in errores:

                st.error(
                    error
                )


        # ====================================================
        # GUARDAR APLICACIÓN
        # ====================================================

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


            except Exception as e:

                st.error(
                    "No fue posible guardar "
                    f"la aplicación: {e}"
                )


    # ========================================================
    # APLICACIONES PUBLICADAS
    # ========================================================

    render_html(
        """
        <div style="
            height:20px;
        "></div>
        """
    )


    render_html(
        """
        <div class="admin-panel">

            <div class="admin-panel-title">
                Aplicaciones publicadas
            </div>

            <div class="admin-panel-description">
                Desde aquí puedes revisar y eliminar
                proyectos del catálogo.
            </div>

        </div>
        """
    )


    # ========================================================
    # SIN APLICACIONES
    # ========================================================

    if len(apps) == 0:

        st.info(
            "No hay aplicaciones publicadas todavía."
        )


    # ========================================================
    # LISTA DE APLICACIONES
    # ========================================================

    else:

        for app in apps:

            col1, col2, col3 = st.columns(
                [1, 5, 1]
            )


            # ------------------------------------------------
            # PREVISUALIZACIÓN
            # ------------------------------------------------

            with col1:

                ruta_imagen = app.get(
                    "imagen",
                    ""
                )


                if os.path.exists(
                    ruta_imagen
                ):

                    try:

                        imagen_preview = Image.open(
                            ruta_imagen
                        )

                        st.image(
                            imagen_preview,
                            width=100
                        )

                    except Exception:

                        st.write("—")

                else:

                    st.write("—")


            # ------------------------------------------------
            # INFORMACIÓN
            # ------------------------------------------------

            with col2:

                titulo_admin = limpiar(
                    app.get(
                        "titulo",
                        ""
                    )
                )

                url_admin = limpiar(
                    app.get(
                        "url",
                        ""
                    )
                )


                render_html(
                    f"""
                    <div style="
                        padding-top:5px;
                    ">

                        <div style="
                            font-weight:700;
                            color:#0f172a;
                            font-size:15px;
                        ">
                            {titulo_admin}
                        </div>

                        <div style="
                            color:#64748b;
                            font-size:12px;
                            margin-top:4px;
                            word-break:break-all;
                        ">
                            {url_admin}
                        </div>

                    </div>
                    """
                )


            # ------------------------------------------------
            # ELIMINAR
            # ------------------------------------------------

            with col3:

                eliminar = st.button(
                    "Eliminar",
                    key=f"eliminar_{app['id']}",
                    type="secondary"
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

                        if item["id"]
                        != app["id"]
                    ]


                    guardar_apps(
                        apps
                    )


                    st.success(
                        "Aplicación eliminada."
                    )


                    st.rerun()


    # ========================================================
    # FOOTER ADMINISTRACIÓN
    # ========================================================

    render_html(
        """
        <div class="footer">
            Panel de administración · AI Portfolio
        </div>
        """
    )
