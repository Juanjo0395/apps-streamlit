"""
Persistencia de datos del portafolio.

Streamlit Community Cloud borra el disco de la app cada vez que se
reinicia, se duerme o se vuelve a desplegar. Por eso los datos
(apps.json e imágenes) se guardan en una rama del repositorio de
GitHub usando su API.

Si no hay credenciales en st.secrets se usa el disco local, lo cual
sirve para desarrollo pero NO persiste en Streamlit Cloud.
"""

import base64
import os

import requests
import streamlit as st


API_GITHUB = "https://api.github.com"

TIEMPO_ESPERA = 30

CARPETA_LOCAL = "datos_apps"


class ErrorAlmacenamiento(Exception):
    pass


# ============================================================
# DISCO LOCAL
# ============================================================

class AlmacenamientoLocal:

    es_persistente = False

    def __init__(self, carpeta: str = CARPETA_LOCAL):
        self.carpeta = carpeta

    def _ruta(self, ruta: str) -> str:
        return os.path.join(self.carpeta, *ruta.split("/"))

    def leer(self, ruta: str) -> bytes | None:

        ruta_local = self._ruta(ruta)

        if not os.path.exists(ruta_local):
            return None

        with open(ruta_local, "rb") as archivo:
            return archivo.read()

    def escribir(self, ruta: str, contenido: bytes, mensaje: str) -> None:

        ruta_local = self._ruta(ruta)

        os.makedirs(os.path.dirname(ruta_local), exist_ok=True)

        with open(ruta_local, "wb") as archivo:
            archivo.write(contenido)

    def eliminar(self, ruta: str, mensaje: str) -> None:

        ruta_local = self._ruta(ruta)

        if os.path.exists(ruta_local):
            os.remove(ruta_local)


# ============================================================
# GITHUB
# ============================================================

def _cabeceras(token: str, accept: str = "application/vnd.github+json") -> dict:

    return {
        "Authorization": f"Bearer {token}",
        "Accept": accept,
        "X-GitHub-Api-Version": "2022-11-28",
    }


def _verificar(respuesta: requests.Response, accion: str) -> None:

    if respuesta.ok:
        return

    try:
        detalle = respuesta.json().get("message", "")
    except ValueError:
        detalle = respuesta.text[:200]

    raise ErrorAlmacenamiento(
        f"GitHub respondió {respuesta.status_code} al {accion}: {detalle}"
    )


@st.cache_data(show_spinner=False, max_entries=200)
def _leer_github(repo: str, rama: str, ruta: str, _token: str) -> bytes | None:
    """
    Lee un archivo de la rama. Se cachea para no llamar a la API
    en cada rerun; se limpia cada vez que se escribe o elimina.
    """

    respuesta = requests.get(
        f"{API_GITHUB}/repos/{repo}/contents/{ruta}",
        headers=_cabeceras(_token, "application/vnd.github.raw+json"),
        params={"ref": rama},
        timeout=TIEMPO_ESPERA,
    )

    if respuesta.status_code == 404:
        return None

    _verificar(respuesta, f"leer {ruta}")

    return respuesta.content


class AlmacenamientoGitHub:

    es_persistente = True

    def __init__(self, token: str, repo: str, rama: str, carpeta: str):

        self.token = token
        self.repo = repo
        self.rama = rama
        self.carpeta = carpeta.strip("/")

    def _ruta(self, ruta: str) -> str:

        if not self.carpeta:
            return ruta

        return f"{self.carpeta}/{ruta}"

    def _url_contenido(self, ruta: str) -> str:
        return f"{API_GITHUB}/repos/{self.repo}/contents/{self._ruta(ruta)}"

    def _sha(self, ruta: str) -> str | None:

        respuesta = requests.get(
            self._url_contenido(ruta),
            headers=_cabeceras(self.token),
            params={"ref": self.rama},
            timeout=TIEMPO_ESPERA,
        )

        if respuesta.status_code == 404:
            return None

        _verificar(respuesta, f"consultar {ruta}")

        return respuesta.json().get("sha")

    def asegurar_rama(self) -> None:
        """
        Crea la rama de datos a partir de la rama principal si no
        existe. Se usa una rama aparte para que guardar datos no
        dispare un nuevo despliegue de la app.
        """

        url_repo = f"{API_GITHUB}/repos/{self.repo}"

        respuesta = requests.get(
            f"{url_repo}/branches/{self.rama}",
            headers=_cabeceras(self.token),
            timeout=TIEMPO_ESPERA,
        )

        if respuesta.ok:
            return

        if respuesta.status_code != 404:
            _verificar(respuesta, f"consultar la rama {self.rama}")

        respuesta = requests.get(
            url_repo,
            headers=_cabeceras(self.token),
            timeout=TIEMPO_ESPERA,
        )
        _verificar(respuesta, "consultar el repositorio")

        rama_principal = respuesta.json()["default_branch"]

        respuesta = requests.get(
            f"{url_repo}/git/ref/heads/{rama_principal}",
            headers=_cabeceras(self.token),
            timeout=TIEMPO_ESPERA,
        )
        _verificar(respuesta, f"consultar la rama {rama_principal}")

        respuesta = requests.post(
            f"{url_repo}/git/refs",
            headers=_cabeceras(self.token),
            json={
                "ref": f"refs/heads/{self.rama}",
                "sha": respuesta.json()["object"]["sha"],
            },
            timeout=TIEMPO_ESPERA,
        )
        _verificar(respuesta, f"crear la rama {self.rama}")

    def leer(self, ruta: str) -> bytes | None:

        return _leer_github(
            self.repo,
            self.rama,
            self._ruta(ruta),
            self.token,
        )

    def escribir(self, ruta: str, contenido: bytes, mensaje: str) -> None:

        cuerpo = {
            "message": mensaje,
            "content": base64.b64encode(contenido).decode("ascii"),
            "branch": self.rama,
        }

        sha = self._sha(ruta)

        if sha:
            cuerpo["sha"] = sha

        respuesta = requests.put(
            self._url_contenido(ruta),
            headers=_cabeceras(self.token),
            json=cuerpo,
            timeout=TIEMPO_ESPERA,
        )

        _leer_github.clear()

        _verificar(respuesta, f"guardar {ruta}")

    def eliminar(self, ruta: str, mensaje: str) -> None:

        sha = self._sha(ruta)

        if not sha:
            return

        respuesta = requests.delete(
            self._url_contenido(ruta),
            headers=_cabeceras(self.token),
            json={
                "message": mensaje,
                "sha": sha,
                "branch": self.rama,
            },
            timeout=TIEMPO_ESPERA,
        )

        _leer_github.clear()

        _verificar(respuesta, f"eliminar {ruta}")


# ============================================================
# SELECCIÓN DEL ALMACENAMIENTO
# ============================================================

def _config_github() -> dict | None:

    try:
        config = st.secrets.get("github")
    except Exception:
        # No existe secrets.toml (por ejemplo, en local).
        return None

    if not config or not config.get("token") or not config.get("repo"):
        return None

    return config


@st.cache_resource(show_spinner=False)
def obtener_almacenamiento():

    config = _config_github()

    if config is None:
        return AlmacenamientoLocal()

    almacenamiento = AlmacenamientoGitHub(
        token=config["token"],
        repo=config["repo"],
        rama=config.get("rama", "datos"),
        carpeta=config.get("carpeta", "datos_apps"),
    )

    almacenamiento.asegurar_rama()

    return almacenamiento
