"""
rutas de la máquina: repo, carpeta de trabajo, musescore y audiveris.
se pueden forzar con las variables CANCIONES_REPO, CANCIONES_WORK, MUSESCORE y AUDIVERIS.
"""
import os
from pathlib import Path

HOME = Path.home()
LOCAL = Path(os.environ.get("LOCALAPPDATA", HOME / "AppData" / "Local"))


def _primera(env, candidatos):
    if os.environ.get(env):
        return Path(os.environ[env])
    for c in candidatos:
        if Path(c).exists():
            return Path(c)
    return Path(candidatos[0])


REPO = _primera("CANCIONES_REPO", [
    HOME / "OneDrive - Prosegur Cia. De Seguridad, S.A" / "Documentos" / "canciones",
    HOME / "Canciones",
])
WORK = _primera("CANCIONES_WORK", [HOME / "Canciones_work"])
MS = str(_primera("MUSESCORE", [
    LOCAL / "canciones_tools" / "MuseScore" / "MuseScore 4" / "bin" / "MuseScore4.exe",
    r"C:\Program Files\MuseScore 4\bin\MuseScore4.exe",
]))
AV = str(_primera("AUDIVERIS", [
    LOCAL / "canciones_tools" / "Audiveris" / "Audiveris" / "Audiveris.exe",
    WORK / "audiveris" / "Audiveris" / "Audiveris.exe",
]))
