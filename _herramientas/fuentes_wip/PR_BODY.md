## Qué incluye

Transcripción a **cuarteto masculino TTBB** (Tenor 1, Tenor 2, Barítono, Bajo) de los PDF corales del repositorio.

- **49 canciones transcritas** en `Español/`, `Inglés /`, `Navidad/` y `Rumano/`.
- **6 canciones bloqueadas**, sin transcribir (ver abajo).
- Cada canción transcrita tiene **11 ficheros** en `<Carpeta>/<Canción>/`:
  - `Partitura_Grupal.pdf`
  - `Edicion/partitura.musicxml` y `Edicion/partitura.mscz`, editables en MuseScore 4
  - `MIDIS/` con Tenor1, Tenor2, Baritono y Bajo (`.mid`)
  - `MP3/` con las mismas cuatro voces (`.mp3`), cada voz destacada sobre las demás para ensayar
- Las canciones con piano (por ejemplo, Más allá de sol y Rasuna cintare) llevan además el acompañamiento en la partitura.
- `PROGRESO.md` tiene una línea por canción con tonalidad, compás, número de compases y advertencias: notas deducidas, lecturas dudosas y correcciones del revisor.
- `REPORTE.md` es el informe global: QA, estadísticas por carpeta y ficha de cada canción.

## Cómo se hizo

1. Cada PDF se leyó compás a compás contra la imagen, con ayuda de OMR (Audiveris) cuando el escaneo lo permitía, y se escribió en un DSL de texto (`_herramientas/fuentes/<Carpeta>/<Canción>.txt`).
2. `dsl.py` convierte el DSL a MusicXML. `export.py` genera mscz, PDF, MIDI y MP3 con MuseScore 4 y ffmpeg.
3. `qa.py` comprueba cada canción: 4 partes TTBB (o TTBB + piano), compases, letra y los 11 ficheros.
4. Un corrector independiente comparó cada partitura renderizada (`review.py`) con el original y corrigió los errores que encontró. Esas correcciones constan en las advertencias de `PROGRESO.md`.
5. `accept.py` registra cada canción y hace commit; `reporte.py` regenera `REPORTE.md`.

## Cómo regenerar

```bash
PYTHONUTF8=1 python _herramientas/export.py "_herramientas/fuentes/<Carpeta>/<Canción>.txt" "<Carpeta>/<Canción>"
PYTHONUTF8=1 python _herramientas/qa.py "<Carpeta>/<Canción>" <compases>
PYTHONUTF8=1 python _herramientas/reporte.py
```

Para cambiar de equipo, solo hay que editar las rutas de máquina en `_herramientas/rutas.py` o fijarlas con `CANCIONES_REPO`, `CANCIONES_WORK`, `MUSESCORE` y `AUDIVERIS`.

## Bloqueadas (no transcritas)

| Canción | Motivo |
|---|---|
| Inglés/Good News | Arreglo de Wayne Hooper, © 1963 Key Music Co. Bloqueada por decisión del propietario del repo; el trabajo parcial (c.0-40) está en `_herramientas/fuentes_wip/`. |
| Español/Brilla en mi | El PDF es idéntico, byte a byte, a `Rumano/O tata bun.pdf`. |
| Navidad/Here Comes the Light TTBB | Arreglo comercial (Shawnee Press), copia preview. |
| Rumano/Wonderfull Grace of Jesus | Arreglo comercial (Lorenz Publishing). |
| Navidad/It came upon the midnight partitura | Arreglo de Joel Raney, copia PREVIEW. |
| Español/It came upon the midnight clear (español) | La misma copia PREVIEW de Joel Raney. |

## A revisar a mano

Muchos originales son fotos o manuscritos de baja calidad. Las notas deducidas o dudosas están marcadas como `NOTA DEDUCIDA` en el DSL y aparecen en las advertencias de `PROGRESO.md` y `REPORTE.md`. Conviene que alguien del cuarteto las escuche con los MP3 antes de usarlas.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
