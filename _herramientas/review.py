"""
renderiza el resultado (mscz) y el pdf original a png para compararlos.
  python review.py "<Carpeta>" "<Canción>" "<pdf original>" [dpi]
salida: WORK/review/<tag>/orig-N.png y final-N.png (~1500 px de ancho)
"""
import sys, re, subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from rutas import REPO, WORK, MS
import pymupdf
from PIL import Image


def reducir(p, ancho=1500):
    im = Image.open(p)
    if im.width > ancho:
        im = im.resize((ancho, round(im.height * ancho / im.width)), Image.LANCZOS)
    # fondo blanco: musescore exporta png con transparencia
    if im.mode in ("RGBA", "LA"):
        fondo = Image.new("RGB", im.size, "white")
        fondo.paste(im, mask=im.split()[-1])
        im = fondo
    im.save(p)


def review(carpeta, cancion, pdf, dpi=150):
    tag = re.sub(r"[^0-9A-Za-z]", "_", f"{carpeta}_{cancion}")
    out = WORK / "review" / tag
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("*.png"):
        f.unlink()
    doc = pymupdf.open(pdf)
    for i, pg in enumerate(doc, 1):
        pg.get_pixmap(dpi=dpi).save(out / f"orig-{i}.png")
        reducir(out / f"orig-{i}.png")
    mscz = REPO / carpeta / cancion / "Edicion" / "partitura.mscz"
    subprocess.run([MS, str(mscz), "-o", str(out / "final.png")], capture_output=True)
    for f in sorted(out.glob("final-*.png")):
        reducir(f)
    print(out)
    for f in sorted(out.glob("*.png")):
        print(" ", f.name)


if __name__ == "__main__":
    review(sys.argv[1], sys.argv[2], sys.argv[3], *(int(x) for x in sys.argv[4:5]))
