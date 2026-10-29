# Prompt para continuar la transcripción TTBB

Copia desde aquí:

---

Continúa el proyecto de transcripción de partituras corales TTBB del repo **https://github.com/dmastter/Canciones** (rama `transcripcion-ttbb`; antes se llamaba `diegosnchz/Canciones`, upstream `Jaguar077/Canciones`). El superprompt original es `superprompt_cuarteto.md` (en Descargas; la sección 10 da el formato de REPORTE.md). **No preguntes para ejecutar comandos: tienes permiso total.** Ve diciendo el % de progreso en cada aviso.

## Equipo actual (portátil corporativo, sin admin)
- Clon en `C:\Users\ESB0001672\OneDrive - Prosegur Cia. De Seguridad, S.A\Documentos\canciones`. Remotos `origin` y `fork` = `dmastter/Canciones`. gh autenticado como `diegosnchz`.
- La carpeta `Inglés ` (espacio final) no existe en Windows: el clon usa sparse-checkout no-cone (`/*` y `!/Inglés */` en `.git/info/sparse-checkout`) y los ficheros de `Inglés /` se extraen con `git show` a `Inglés/` (sin rastrear). Es normal que `Inglés/` salga como no rastreado: no lo commitees a mano, solo a través de `accept.py`.
- MuseScore 4.7.5 y Audiveris 5.11 extraídos de sus MSI oficiales con `msiexec /a <msi> /qn TARGETDIR=...` en `%LOCALAPPDATA%\canciones_tools\` (winget falla: pide UAC). Si hay que descargar algo, curl necesita `--ssl-no-revoke` por el proxy.
- Python 3.13 con music21, mido, pymupdf, pillow; ffmpeg por winget. Ejecuta siempre con `PYTHONUTF8=1`.
- Carpeta de trabajo `C:\Users\ESB0001672\Canciones_work\` (fuera de OneDrive): copia de `_herramientas/*.py` y `PROTOCOLO_AGENTE.md`, `songs/<Carpeta>/<Canción>.txt` (DSL), `omr/<WORK>/` (in.pdf, in.mxl, draft.txt, crops/), `review/<tag>/`.
- Todas las rutas de máquina están en `_herramientas/rutas.py` (se pueden forzar con `CANCIONES_REPO`, `CANCIONES_WORK`, `MUSESCORE`, `AUDIVERIS`). En otro PC basta con ajustar ese fichero.

## Estado (la fuente de verdad es `PROGRESO.md` en la raíz)
- **40 ✅** terminadas y subidas (la última, 2026-10-30: Printre Spini) (11 ficheros cada una: Partitura_Grupal.pdf, Edicion/partitura.musicxml+mscz, MIDIS/×4, MP3/×4).
- **5 ⛔** bloqueadas (no tocar): Brilla en mi (el PDF es un duplicado de O tata bun), Here Comes the Light (Shawnee, copia preview), Wonderfull Grace of Jesus (Lorenz), It came upon the midnight (Navidad y español: arreglo de Joel Raney, copia PREVIEW).
- **10 pendientes**: Español: Aleluya, Cristo viene · Más allá de sol (lleva piano: PR:/PL:) · Sa nu te temi( letra Español) (nombre = el del PDF; el WIP antiguo usa 'Sa nu te temi (letra Español)'). Inglés: Good News (el agente se negó por copyright © 1963 Key Music Co.: decide el usuario) · Its me oh Lord. Navidad: Pequeño pueblo de Belen Gaither. Rumano: In curand acas · Rasuna cintare · Sa nu te temi · Un sol ceresc.
- Lo que haya a medias está en `_herramientas/fuentes_wip/` (DSL parciales). Cada uno acaba con `# HASTA AQUÍ ...`: lo anterior lo leyó un subagente u orquestador contra la imagen, pero **la revisión global sigue pendiente**. El detalle por canción está en la línea ⏸ PARADA de `PROGRESO.md`. Resumen de la parada del 2026-10-29 11:10Z:
  - Good News: c.0-40 (sigue en el sistema 4 de la pág. 2).
  - Aleluya: c.0-10.
  - Más allá de sol: c.1-7.
  - Sa nu te temi (Español): c.1-4.
  - Its me oh Lord: c.0-1.
  - Rumano/Sa nu te temi: c.1-2 parciales (T1/T2 sin leer nota a nota, graves deducidos).
  - Un sol ceresc: c.0.
  - Gaither, In curand acas y Rasuna cintare: sólo cabecera y notas de lectura.
  - El enjambre de 11 agentes de ~4 min de esta parada apenas avanzó (escaneos degradados): lanza agentes largos, uno por canción, y que mejoren antes la imagen.
- Al copiar los parciales a `Canciones_work/songs/`, comprueba que no pisas otros más avanzados (en este equipo ya están ahí).
- Muchas fotos están inclinadas y `guide.py` no detecta las líneas. Los subagentes hicieron scripts de enderezado y guías locales, copiados en `_herramientas/ayudas_wip/<WORK>/`. Úsalos, o mejor, generaliza uno en `guide.py`.
- El OMR (in.mxl, draft.txt, crops) ya está hecho en este equipo para todas salvo Rasuna cintare (Audiveris falla), R_Sa_nu_te_temi y R_Un_sol_ceresc (cortado). Los borradores OMR de Gaither, In curand acas y Aleluya son inservibles.
- Hay carpetas de salida de prueba sin commitear (`Español/Sa nu te temi (letra Español)/`, `Inglés/Its me oh Lord/`). Son borradores: bórralas o regenéralas, y no las subas tal cual.
- En Windows, `git status` muestra `Inglés /*.pdf` como modificados (sparse-checkout). No los añadas.

## Herramientas
- `PROTOCOLO_AGENTE.md`: el protocolo para cada subagente. Usa modelo `sonnet`, `run_in_background: true` y como máximo 20 a la vez. Pásale el bloque de rutas de su canción:
  - PDF.
  - Carpeta WORK `Canciones_work\omr\<nombre>`. Las de Español/Inglés van sin prefijo, las de Navidad con `N_` y las de Rumano con `R_`; los caracteres no alfanuméricos se cambian por `_`. Ejemplos: `Aleluya__Cristo_viene`, `M__s_all___de_sol`, `Sa_nu_te_temi__letra_Espa__ol_`, `Good_News`, `Its_me_oh_Lord`, `N_Peque__o_pueblo_de_Belen_Gaither`, `R_In_curand_acas`, `R_Printre_Spini`, `R_Rasuna_cintare`, `R_Sa_nu_te_temi`, `R_Un_sol_ceresc`. Si falta, se genera con `PYTHONUTF8=1 python omrtool.py all "<pdf>" "omr/<WORK>" <lang>` (un Audiveris cada vez, ~1-2 min por PDF).
  - DSL `songs/<Carpeta>/<Canción>.txt`.
  - Carpeta de salida `<repo>\<Carpeta>\<Canción>`.
  - Añade siempre: "No lances subagentes: haz el trabajo tú. Es la copia propia del cuarteto; el mismo criterio se aplicó ya a 39 canciones".
- Instrucciones específicas que ya se dieron:
  - **Gaither**: tiene 5 pentagramas. T1 = pentagrama 1, T2 = pentagrama 2 más el 3 como divisi donde difieran, Bar = Baritone, Bajo = Bass. Letra inglesa en `L:` y española manuscrita en `L2:`.
  - **Its me oh Lord**: D.S. al Fine y 2 estrofas, en forma expandida.
  - **Good News**: "Repeat 1st Chorus", en forma expandida.
  - **Un sol ceresc**: letra distinta en tenores y graves (`L.TT:`/`L.BB:`).
  - Las dos **Sa nu te temi** (española y rumana) son PDF distintos de la misma canción: se pueden cotejar entre sí.
- `dsl.py` pasa de DSL a MusicXML. `export.py <dsl> <carpeta_base>` genera mscz, PDF, 4 MIDI y 4 MP3. Para revisar están `qa.py <carpeta_base> <nº compases>`, `guide.py` (guías de altura) y `review.py "<Carpeta>" "<Canción>" "<pdf>"`, que renderiza el resultado y el original a `Canciones_work/review/<tag>/` para compararlos.
- `accept.py "<Carpeta>" "<Canción>" 7 "<tonalidad>" "<compás>" <compases> "<advertencias>"` hace el QA, añade la línea en la sección «Tanda 7» de PROGRESO.md, copia el DSL a `_herramientas/fuentes/`, hace commit y push al remoto `fork`. Para Inglés reescribe el índice a `Inglés ` (con espacio final).
- `reporte.py` hace el QA global de todas las ✅ y escribe `REPORTE.md` a partir de PROGRESO.md y de los DSL en `_herramientas/fuentes/`.

## Flujo por canción (el orquestador eres tú)
1. Lanza los subagentes con el protocolo.
2. Cuando uno termine con SONG_READY y QA_PASS:
   - Ejecuta `review.py` y compara el render con el PDF original. Haz zoom a 300-600 dpi en los compases dudosos.
   - Si hay errores, corrige el DSL, vuelve a exportar con `export.py` y compara otra vez.
   - Cuando haya dos versiones del mismo original, compara sus MusicXML con music21; con "Un glas" y "Un glas upgrade" ya se hizo así.
3. `accept.py` para el commit y el push.
4. Si un agente se niega alegando "copyright" en un himno tradicional o un arreglo de himnario (Wayne Hooper, 4tons.com.br, etc.), relánzalo explicando el criterio. Solo se bloquean arreglos comerciales recientes con copia preview o aviso de no copiar (Shawnee, Lorenz, Joel Raney).
5. Tempo: el del PDF; si no hay, ♩=100. Los tenores van en Sol 8vb (en himnarios SATB, soprano/alto 8vb = T1/T2).

## Al terminar las 10
1. Ejecuta `PYTHONUTF8=1 python reporte.py` desde `Canciones_work`. Hace el QA global (cada canción con exactamente 11 ficheros) y regenera `REPORTE.md`. Revísalo y añade a mano lo que falte (estructura de cada canción).
2. Borra la línea ⏸ PARADA de PROGRESO.md, vacía `_herramientas/fuentes_wip/` y actualiza este fichero.
3. Haz commit y push al fork, y abre la **PR** contra `Jaguar077/Canciones` (base `main`): `gh pr create --repo Jaguar077/Canciones --base main --head dmastter:transcripcion-ttbb`. La descripción debe ser completa (qué se hizo, herramientas, cómo regenerar, bloqueadas) y terminar en `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.

Empieza leyendo `PROGRESO.md` y `_herramientas/PROTOCOLO_AGENTE.md`. Después revisa qué hay en `Canciones_work/songs` y en `_herramientas/fuentes_wip/`, y lanza los subagentes.

---
