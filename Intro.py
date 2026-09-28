import streamlit as st
from PIL import Image
import json
import os
import uuid
import base64
import mimetypes
import html


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
# CONFIGURACIÓN DE ARCHIVOS
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

    /* ========================================================
       VARIABLES
       ======================================================== */

    :root {

        --bg: #f5f7fb;

        --surface: #ffffff;

        --surface-soft: #f8fafc;

        --text: #0f172a;

        --muted: #64748b;

        --muted-light: #94a3b8;

        --border: #e2e8f0;

        --primary: #2563eb;

        --primary-dark: #1d4ed8;

        --cyan: #06b6d4;

        --dark: #0b1220;

        --dark-2: #111c33;

        --shadow:
            0 12px 35px rgba(15, 23, 42, 0.07);

        --shadow-hover:
            0 20px 45px rgba(15, 23, 42, 0.13);
    }


    /* ========================================================
       APP
       ======================================================== */

    .stApp {

        background:

            radial-gradient(
                circle at 15% 0%,
                rgba(37, 99, 235, 0.08),
                transparent 28%
            ),

            radial-gradient(
                circle at 90% 10%,
                rgba(6, 182, 212, 0.07),
                transparent 25%
            ),

            var(--bg);
    }


    /* ========================================================
       CONTENEDOR PRINCIPAL
       ======================================================== */

    .block-container {

        max-width: 1280px !important;

        padding-top: 2rem !important;

        padding-bottom: 4rem !important;
    }


    /* ========================================================
       OCULTAR ELEMENTOS
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

        background:
            linear-gradient(
                180deg,
                #08101e 0%,
                #0b1220 100%
            );

        border-right:
            1px solid
            rgba(255,255,255,0.06);
    }


    section[data-testid="stSidebar"] * {
        color: #dbeafe;
    }


    section[data-testid="stSidebar"] hr {

        border-color:
            rgba(255,255,255,0.09);
    }


    /* ========================================================
       HERO
       ======================================================== */

    .hero {

        position: relative;

        overflow: hidden;

        padding: 48px;

        border-radius: 26px;

        margin-bottom: 28px;

        background:

            linear-gradient(
                135deg,
                #08101e 0%,
                #111c33 55%,
                #123650 100%
            );

        box-shadow:
            0 24px 60px
            rgba(15,23,42,0.18);
    }


    .hero::before {

        content: "";

        position: absolute;

        width: 320px;

        height: 320px;

        right: -120px;

        top: -150px;

        border-radius: 50%;

        background:

            radial-gradient(
                circle,
                rgba(34,211,238,0.28),
                transparent 67%
            );
    }


    .hero::after {

        content: "";

        position: absolute;

        width: 240px;

        height: 240px;

        left: 48%;

        bottom: -190px;

        border-radius: 50%;

        background:

            radial-gradient(
                circle,
                rgba(37,99,235,0.25),
                transparent 70%
            );
    }


    .hero-content {

        position: relative;

        z-index: 2;

        max-width: 820px;
    }


    .hero-kicker {

        color: #67e8f9;

        font-size: 11px;

        font-weight: 800;

        letter-spacing: 2.5px;

        text-transform: uppercase;

        margin-bottom: 15px;
    }


    .hero-title {

        color: white;

        font-size: clamp(
            34px,
            4vw,
            55px
        );

        line-height: 1.04;

        font-weight: 800;

        letter-spacing: -2px;

        margin: 0;
    }


    .hero-title span {

        color: #22d3ee;
    }


    .hero-description {

        color: #cbd5e1;

        font-size: 16px;

        line-height: 1.7;

        max-width: 720px;

        margin-top: 18px;

        margin-bottom: 0;
    }


    /* ========================================================
       STATS
       ======================================================== */

    .stats {

        display: grid;

        grid-template-columns:
            repeat(3, minmax(0, 1fr));

        gap: 14px;

        margin-bottom: 34px;
    }


    .stat {

        background:
            rgba(255,255,255,0.82);

        border:
            1px solid var(--border);

        border-radius: 16px;

        padding: 19px 21px;

        box-shadow:
            0 6px 22px
            rgba(15,23,42,0.04);
    }


    .stat-label {

        color: var(--muted);

        font-size: 10px;

        font-weight: 800;

        letter-spacing: 1.5px;

        text-transform: uppercase;
    }


    .stat-value {

        color: var(--text);

        font-size: 25px;

        font-weight: 800;

        margin-top: 5px;
    }


    /* ========================================================
       SECCIÓN
       ======================================================== */

    .section-heading {

        margin-bottom: 20px;
    }


    .section-title {

        color: var(--text);

        font-size: 27px;

        font-weight: 800;

        letter-spacing: -0.8px;

        margin: 0;
    }


    .section-description {

        color: var(--muted);

        font-size: 14px;

        margin-top: 5px;
    }


    /* ========================================================
       GRID
       ======================================================== */

    .portfolio-grid {

        display: grid;

        grid-template-columns:
            repeat(3, minmax(0, 1fr));

        gap: 24px;

        width: 100%;

        margin-bottom: 24px;
    }


    /* ========================================================
       CARD
       ======================================================== */

    .app-card {

        display: flex;

        flex-direction: column;

        min-width: 0;

        overflow: hidden;

        background:
            var(--surface);

        border:
            1px solid var(--border);

        border-radius: 20px;

        box-shadow:
            var(--shadow);

        transition:
            transform .25s ease,
            box-shadow .25s ease,
            border-color .25s ease;
    }


    .app-card:hover {

        transform:
            translateY(-5px);

        box-shadow:
            var(--shadow-hover);

        border-color:
            rgba(37,99,235,0.25);
    }


    /* ========================================================
       CARD IMAGE
       ======================================================== */

    .app-image {

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


    .app-image img {

        width: 100%;

        height: 100%;

        display: block;

        object-fit: cover;

        transition:
            transform .35s ease;
    }


    .app-card:hover
    .app-image img {

        transform:
            scale(1.035);
    }


    /* ========================================================
       CARD CONTENT
       ======================================================== */

    .app-body {

        display: flex;

        flex-direction: column;

        min-height: 235px;

        padding: 21px;
    }


    .app-tag {

        align-self: flex-start;

        color: #1d4ed8;

        background:
            #eff6ff;

        border:
            1px solid #dbeafe;

        border-radius: 999px;

        padding:
            5px 9px;

        font-size: 9px;

        font-weight: 800;

        letter-spacing: 1px;

        text-transform: uppercase;

        margin-bottom: 12px;
    }


    .app-title {

        color: var(--text);

        font-size: 19px;

        font-weight: 800;

        line-height: 1.3;

        margin-bottom: 9px;
    }


    .app-description {

        color: var(--muted);

        font-size: 13px;

        line-height: 1.65;

        display: -webkit-box;

        -webkit-line-clamp: 4;

        -webkit-box-orient: vertical;

        overflow: hidden;

        margin-bottom: 20px;
    }


    .app-button {

        display: block;

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

        text-align: center;

        text-decoration: none !important;

        font-size: 13px;

        font-weight: 750;

        margin-top: auto;

        transition:
            transform .2s ease,
            box-shadow .2s ease;
    }


    .app-button:hover {

        color: white !important;

        transform:
            translateY(-1px);

        box-shadow:
            0 8px 20px
            rgba(37,99,235,0.25);
    }


    /* ========================================================
       EMPTY STATE
       ======================================================== */

    .empty {

        text-align: center;

        padding: 70px 30px;

        background: white;

        border:
            1px dashed #cbd5e1;

        border-radius: 20px;
    }


    .empty-icon {

        color: #94a3b8;

        font-size: 32px;

        margin-bottom: 10px;
    }


    .empty-title {

        color: var(--text);

        font-size: 20px;

        font-weight: 800;
    }


    .empty-text {

        color: var(--muted);

        font-size: 14px;

        margin-top: 6px;
    }


    /* ========================================================
       ADMIN HERO
       ======================================================== */

    .admin-header {

        background:

            linear-gradient(
                135deg,
                #08101e,
                #172554
            );

        border-radius: 24px;

        padding: 34px;

        color: white;

        margin-bottom: 25px;

        box-shadow:
            0 18px 45px
            rgba(15,23,42,0.14);
    }


    .admin-title {

        font-size: 29px;

        font-weight: 800;

        letter-spacing: -1px;
    }


    .admin-description {

        color: #cbd5e1;

        font-size: 14px;

        line-height: 1.6;

        max-width: 700px;

        margin-top: 7px;
    }


    /* ========================================================
       ADMIN PANEL
       ======================================================== */

    .panel {

        background: white;

        border:
            1px solid var(--border);

        border-radius: 20px;

        padding: 25px;

        box-shadow:
            0 8px 30px
            rgba(15,23,42,0.05);

        margin-bottom: 22px;
    }


    .panel-title {

        color: var(--text);

        font-size: 18px;

        font-weight: 800;

        margin-bottom: 4px;
    }


    .panel-description {

        color: var(--muted);

        font-size: 13px;

        margin-bottom: 18px;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {

        margin-top: 55px;

        padding-top: 25px;

        border-top:
            1px solid var(--border);

        text-align: center;

        color: var(--muted-light);

        font-size: 12px;

        letter-spacing: .3px;
    }


    /* ========================================================
       RESPONSIVE
       ======================================================== */

    @media (max-width: 1000px) {

        .portfolio-grid {

            grid-template-columns:
                repeat(2, minmax(0, 1fr));
        }
    }


    @media (max-width: 700px) {

        .block-container {

            padding-left: 1rem !important;

            padding-right: 1rem !important;
        }


        .hero {

            padding: 32px 25px;

            border-radius: 20px;
        }


        .stats {

            grid-template-columns: 1fr;
        }


        .portfolio-grid {

            grid-template-columns: 1fr;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FUNCIONES HTML
# ============================================================

def mostrar_html(contenido):
    """
    Renderiza HTML directamente con st.html().

    IMPORTANTE:
    No usar st.markdown() para estos bloques.
    """

    st.html(contenido)


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
# FUNCIONES DE IMAGEN
# ============================================================

def guardar_imagen(archivo):

    extension = os.path.splitext(
        archivo.name
    )[1].lower()

    permitidas = [
        ".png",
        ".jpg",
        ".jpeg",
        ".webp"
    ]

    if extension not in permitidas:

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


def imagen_base64(ruta):

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
            mimetypes.guess_type(ruta)[0]
            or "image/jpeg"
        )

        return (
            f"data:{mime};base64,"
            f"{contenido}"
        )

    except Exception:

        return None


# ============================================================
# SEGURIDAD
# ============================================================

def escapar(valor):

    return html.escape(
        str(valor),
        quote=True
    )


# ============================================================
# CARGAR DATOS
# ============================================================

apps = cargar_apps()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    mostrar_html(
        """
        <div style="
            padding: 8px 0 22px 0;
        ">

            <div style="
                color:white;
                font-size:21px;
                font-weight:800;
                letter-spacing:-0.5px;
            ">
                AI<span style="color:#22d3ee;">·</span>PORTFOLIO
            </div>

            <div style="
                color:#94a3b8;
                font-size:12px;
                line-height:1.55;
                margin-top:7px;
            ">
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

    mostrar_html(
        """
        <div style="
            color:#94a3b8;
            font-size:11px;
            line-height:1.6;
            margin-top:10px;
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

    st.link_button(
        "Recursos y ejercicios ↗",
        url_recursos,
        use_container_width=True
    )


# ============================================================
# PORTAFOLIO
# ============================================================

if seccion == "Portafolio":

    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    mostrar_html(
        """
        <section class="hero">

            <div class="hero-content">

                <div class="hero-kicker">
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

        </section>
        """
    )


    # --------------------------------------------------------
    # ESTADÍSTICAS
    # --------------------------------------------------------

    mostrar_html(
        f"""
        <div class="stats">

            <div class="stat">

                <div class="stat-label">
                    Proyectos
                </div>

                <div class="stat-value">
                    {len(apps)}
                </div>

            </div>


            <div class="stat">

                <div class="stat-label">
                    Formato
                </div>

                <div class="stat-value">
                    Web Apps
                </div>

            </div>


            <div class="stat">

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


    # --------------------------------------------------------
    # TÍTULO PROYECTOS
    # --------------------------------------------------------

    mostrar_html(
        """
        <div class="section-heading">

            <div class="section-title">
                Proyectos
            </div>

            <div class="section-description">
                Aplicaciones disponibles para explorar.
            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # SIN APLICACIONES
    # --------------------------------------------------------

    if not apps:

        mostrar_html(
            """
            <div class="empty">

                <div class="empty-icon">
                    ◇
                </div>

                <div class="empty-title">
                    Todavía no hay proyectos
                </div>

                <div class="empty-text">
                    Ve a Administración para publicar
                    tu primera aplicación.
                </div>

            </div>
            """
        )


    # --------------------------------------------------------
    # APLICACIONES
    # --------------------------------------------------------

    else:

        tarjetas = []

        for app in apps:

            titulo = escapar(
                app.get(
                    "titulo",
                    "Aplicación"
                )
            )

            descripcion = escapar(
                app.get(
                    "descripcion",
                    ""
                )
            )

            url = escapar(
                app.get(
                    "url",
                    "#"
                )
            )

            ruta = app.get(
                "imagen",
                ""
            )

            img = imagen_base64(ruta)


            if img:

                imagen_html = f"""
                    <img
                        src="{img}"
                        alt="{titulo}"
                    >
                """

            else:

                imagen_html = """
                    <div style="
                        height:205px;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        color:#94a3b8;
                        font-size:13px;
                    ">
                        Imagen no disponible
                    </div>
                """


            tarjeta = f"""
            <article class="app-card">

                <div class="app-image">

                    {imagen_html}

                </div>


                <div class="app-body">

                    <div class="app-tag">
                        AI PROJECT
                    </div>


                    <div class="app-title">
                        {titulo}
                    </div>


                    <div class="app-description">
                        {descripcion}
                    </div>


                    <a
                        class="app-button"
                        href="{url}"
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        Abrir aplicación
                        <span style="margin-left:7px;">
                            ↗
                        </span>
                    </a>

                </div>

            </article>
            """

            tarjetas.append(tarjeta)


        # ----------------------------------------------------
        # GRID COMPLETO
        # ----------------------------------------------------

        for i in range(
            0,
            len(tarjetas),
            3
        ):

            fila = tarjetas[
                i:i + 3
            ]

            mostrar_html(
                f"""
                <div class="portfolio-grid">
                    {''.join(fila)}
                </div>
                """
            )


    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    mostrar_html(
        """
        <div class="footer">
            AI Portfolio · Aplicaciones y proyectos
            de Inteligencia Artificial
        </div>
        """
    )


# ============================================================
# ADMINISTRACIÓN
# ============================================================

else:

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    mostrar_html(
        """
        <section class="admin-header">

            <div class="admin-title">
                Administración del portafolio
            </div>

            <div class="admin-description">
                Gestiona las aplicaciones que aparecen
                públicamente en tu catálogo.
                Publica nuevos proyectos o elimina
                los que ya no quieras mostrar.
            </div>

        </section>
        """
    )


    # --------------------------------------------------------
    # PANEL NUEVA APP
    # --------------------------------------------------------

    mostrar_html(
        """
        <div class="panel">

            <div class="panel-title">
                Nueva aplicación
            </div>

            <div class="panel-description">
                Completa la información que aparecerá
                en la tarjeta pública del proyecto.
            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # FORMULARIO
    # --------------------------------------------------------

    with st.form(
        "formulario_nueva_app",
        clear_on_submit=True
    ):

        col1, col2 = st.columns(
            [1.5, 1],
            gap="large"
        )


        with col1:

            titulo = st.text_input(
                "Nombre de la aplicación",
                placeholder="Ej. Simulador de datos IoT"
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
                    "Se recomienda una imagen "
                    "horizontal de buena calidad."
                )
            )

            st.info(
                "Usa una captura limpia de tu aplicación "
                "o una portada diseñada para representar "
                "el proyecto."
            )


        st.write("")


        publicar = st.form_submit_button(
            "Publicar aplicación",
            type="primary",
            use_container_width=True
        )


    # --------------------------------------------------------
    # PROCESAR FORMULARIO
    # --------------------------------------------------------

    if publicar:

        titulo = titulo.strip()

        descripcion = descripcion.strip()

        url = url.strip()

        errores = []


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


        if not imagen:

            errores.append(
                "Debes seleccionar una imagen."
            )


        if errores:

            for error in errores:

                st.error(error)


        else:

            try:

                ruta = guardar_imagen(
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
                        ruta
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
                    f"No fue posible guardar "
                    f"la aplicación: {e}"
                )


    # --------------------------------------------------------
    # APLICACIONES PUBLICADAS
    # --------------------------------------------------------

    st.write("")

    mostrar_html(
        """
        <div class="panel">

            <div class="panel-title">
                Aplicaciones publicadas
            </div>

            <div class="panel-description">
                Revisa los proyectos que forman parte
                del catálogo y elimina los que ya no
                quieras mostrar.
            </div>

        </div>
        """
    )


    if not apps:

        st.info(
            "No hay aplicaciones publicadas todavía."
        )


    else:

        for app in apps:

            col1, col2, col3 = st.columns(
                [1, 5, 1],
                vertical_alignment="center"
            )


            # ------------------------------------------------
            # IMAGEN
            # ------------------------------------------------

            with col1:

                ruta = app.get(
                    "imagen",
                    ""
                )

                if os.path.exists(ruta):

                    try:

                        preview = Image.open(
                            ruta
                        )

                        st.image(
                            preview,
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

                st.markdown(
                    f"**{app.get('titulo', 'Aplicación')}**"
                )

                st.caption(
                    app.get(
                        "url",
                        ""
                    )
                )


            # ------------------------------------------------
            # ELIMINAR
            # ------------------------------------------------

            with col3:

                eliminar = st.button(
                    "Eliminar",
                    key=f"eliminar_{app['id']}"
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


    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    mostrar_html(
        """
        <div class="footer">
            Panel de administración · AI Portfolio
        </div>
        """
    )
