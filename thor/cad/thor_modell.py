#!/usr/bin/env python3
"""
THOR – parametrisches 3D-Konzeptmodell (CadQuery)

Erzeugt:
  thor.step  – für Fusion 360 / FreeCAD (Baugruppe mit Farben)
  thor.glb   – für Blender und den Web-Viewer

Alle Maße in mm. Koordinaten: Z nach oben, Keg steht auf z = 0.
Das Modell ist ein Konzept-/Layoutmodell: Rohre sind Vollkörper,
Wandstärken nur dort modelliert, wo man hineinschauen soll.

Aufruf:  python3 thor_modell.py
"""
from pathlib import Path
import cadquery as cq

OUT = Path(__file__).parent

# ---------------------------------------------------------------- Parameter
KEG_D, KEG_H = 408, 600          # 50-l-Euro-Keg
JACKET_GAP = 30                  # Wassermantel-Spalt
LINING = 50                      # Feuerfest-Auskleidung
OUTLET_D = 133                   # Heißgasabgang DN 125

NBK_D, NBK_H = 700, 1200         # Nachbrennkammer außen (ausgemauert, ~250 l innen)
NBK_LINING = 80
NBK_X = 900

TURBO_Z = 1450                   # Höhe Turbolader-Achse (Achse in Y-Richtung)
AIR_D = 89                       # Ladeluft DN 80
FEED_D = 70                      # Förderleitung DN 65
EXH_D, EXH_JACKET_D = 168, 219   # Abgas DN 150 mit Kühlmantel

MUF_D, MUF_L = 500, 1400         # Schalldämpfer-WT innen
MUF_JACKET = 30
MUF_Y, MUF_Z, MUF_X0 = 900, 400, 700

SWIRL_Y = 150                    # Versatz für tangentiale Einläufe

# ---------------------------------------------------------------- Farben
C = {
    "steel":   cq.Color(0.74, 0.76, 0.79),
    "water":   cq.Color(0.10, 0.62, 0.58, 0.30),
    "lining":  cq.Color(0.72, 0.62, 0.50),
    "air":     cq.Color(0.20, 0.42, 0.66),
    "insul":   cq.Color(0.86, 0.86, 0.82),
    "exh":     cq.Color(0.10, 0.62, 0.58, 0.55),
    "gas":     cq.Color(0.80, 0.33, 0.10),
    "comp":    cq.Color(0.70, 0.72, 0.76),
    "turb":    cq.Color(0.28, 0.24, 0.22),
    "chra":    cq.Color(0.35, 0.36, 0.40),
    "fuel":    cq.Color(0.58, 0.40, 0.22),
    "dark":    cq.Color(0.22, 0.24, 0.27),
    "burner":  cq.Color(0.85, 0.65, 0.15),
}


# ---------------------------------------------------------------- Helfer
def V(*p):
    return cq.Vector(*p)


def cyl(d, h, base=(0, 0, 0), axis=(0, 0, 1)):
    return cq.Solid.makeCylinder(d / 2, h, V(*base), V(*axis))


def tube(d_out, d_in, h, base=(0, 0, 0), axis=(0, 0, 1)):
    return cyl(d_out, h, base, axis).cut(cyl(d_in, h, base, axis))


def pipe(points, d):
    """Rohrzug als Polylinie: Zylinder je Segment + Kugeln in den Bögen."""
    shape = None
    for a, b in zip(points, points[1:]):
        a, b = V(*a), V(*b)
        seg = cq.Solid.makeCylinder(d / 2, (b - a).Length, a, (b - a).normalized())
        shape = seg if shape is None else shape.fuse(seg)
    for p in points[1:-1]:
        shape = shape.fuse(cq.Solid.makeSphere(d / 2, V(*p), angleDegrees1=-90, angleDegrees2=90))
    return shape.clean()


def box(dx, dy, dz, center):
    return cq.Solid.makeBox(dx, dy, dz, V(center[0] - dx / 2, center[1] - dy / 2, center[2] - dz / 2))


# Viertelschnitt, damit man in Keg, Nachbrennkammer und Schalldämpfer hineinsieht
def cutaway(shape, center, size=4000):
    cx, cy, _ = center
    return shape.cut(cq.Solid.makeBox(size, size, size, V(cx, cy - size, -size / 2)))


assy = cq.Assembly(name="THOR")

# ---------------------------------------------------------------- Brennkammer (Keg)
jd = KEG_D + 2 * JACKET_GAP
keg = tube(KEG_D, KEG_D - 3, KEG_H).fuse(cyl(KEG_D, 3))
lining = tube(KEG_D - 3, KEG_D - 3 - 2 * LINING, KEG_H - 3, (0, 0, 3)).fuse(
    cyl(KEG_D - 3, LINING, (0, 0, 3)))
jacket = tube(jd + 6, jd, KEG_H + JACKET_GAP, (0, 0, -JACKET_GAP)).fuse(
    cyl(jd + 6, 3, (0, 0, -JACKET_GAP - 3)))
lid = cyl(jd + 20, 12, (0, 0, KEG_H)).cut(cyl(OUTLET_D, 12, (0, 0, KEG_H)))
grate = cyl(KEG_D - 2 * LINING - 10, 8, (0, 0, 150))

assy.add(cutaway(keg, (0, 0, 0)), name="Keg_50l", color=C["steel"])
assy.add(cutaway(lining, (0, 0, 0)), name="Auskleidung", color=C["lining"])
assy.add(cutaway(jacket, (0, 0, 0)), name="Wassermantel_Brennkammer", color=C["water"])
assy.add(lid, name="Deckel", color=C["steel"])
assy.add(grate, name="Rost", color=C["dark"])
assy.add(cyl(KEG_D - 2 * LINING - 40, 40, (0, 0, 158)), name="Glutbett", color=C["gas"])

# ---------------------------------------------------------------- Nachbrennkammer
nbk = tube(NBK_D, NBK_D - 8, NBK_H, (NBK_X, 0, 0)).fuse(cyl(NBK_D, 8, (NBK_X, 0, 0))).fuse(
    cyl(NBK_D, 8, (NBK_X, 0, NBK_H - 8)))
nbk_lin = tube(NBK_D - 8, NBK_D - 8 - 2 * NBK_LINING, NBK_H - 16, (NBK_X, 0, 8))
assy.add(cutaway(nbk, (NBK_X, 0, 0)), name="Nachbrennkammer", color=C["insul"])
assy.add(cutaway(nbk_lin, (NBK_X, 0, 0)), name="NBK_Ausmauerung", color=C["lining"])

# Heißgas: Keg -> NBK (isoliert)
hot1 = pipe([(0, 0, KEG_H), (0, 0, 760), (NBK_X - NBK_D / 2 + 10, 0, 760)], OUTLET_D + 60)
assy.add(hot1, name="Heissgas_Keg_NBK_isoliert", color=C["insul"])
# NBK -> Turbine (isoliert)
hot2 = pipe([(NBK_X, 0, NBK_H), (NBK_X, 0, TURBO_Z - 70)], OUTLET_D + 60)
assy.add(hot2, name="Heissgas_NBK_Turbine_isoliert", color=C["insul"])

# ---------------------------------------------------------------- Turbolader (Achse Y)
ty = 0  # Turbinengehäuse über NBK
assy.add(cyl(150, 80, (NBK_X, ty - 40, TURBO_Z), (0, 1, 0)), name="Turbinengehaeuse", color=C["turb"])
assy.add(cyl(90, 70, (NBK_X, ty - 110, TURBO_Z), (0, 1, 0)), name="Lagergehaeuse_Oel", color=C["chra"])
assy.add(cyl(175, 80, (NBK_X, ty - 190, TURBO_Z), (0, 1, 0)), name="Verdichtergehaeuse", color=C["comp"])
# Frischluft-Einlauf mit Schutzgitter
assy.add(cyl(76, 160, (NBK_X, ty - 350, TURBO_Z), (0, 1, 0)), name="Frischluft_Einlauf", color=C["air"])
assy.add(cyl(90, 6, (NBK_X, ty - 356, TURBO_Z), (0, 1, 0)), name="Schutzgitter", color=C["dark"])
# Anfahrgebläse mit Rückschlagklappe
assy.add(pipe([(NBK_X, ty - 290, TURBO_Z), (NBK_X, ty - 290, TURBO_Z - 200)], 60),
         name="Anfahr_Leitung", color=C["air"])
assy.add(cyl(80, 30, (NBK_X, ty - 290, TURBO_Z - 140)), name="Rueckschlagklappe", color=C["dark"])
assy.add(box(260, 220, 200, (NBK_X, ty - 290, TURBO_Z - 300)), name="Anfahrgeblaese", color=C["dark"])

# ---------------------------------------------------------------- Ladeluft
# Verdichteraustritt tangential -> über Keg -> Sekundärluft tangential in den Keg
A = (NBK_X - 85, -150, TURBO_Z)
B = (300, -150, TURBO_Z)
Cc = (300, -SWIRL_Y, 450)
D = (60, -SWIRL_Y, 450)
assy.add(pipe([A, B, Cc, D], AIR_D), name="Ladeluft_Sekundaerluft", color=C["air"])
# Zapfluft / Förderluft: Abzweig bei z=700, um den Bunker herum, tangential ein (gleicher Drehsinn)
T = (300, -150, 700)
bleed = [T, (-1000, -150, 700), (-1000, -150, 250), (-1000, SWIRL_Y, 250), (-60, SWIRL_Y, 250)]
assy.add(pipe(bleed, FEED_D), name="Zapfluft_Foerderleitung", color=C["air"])
assy.add(cq.Solid.makeSphere(AIR_D / 2 + 8, V(*T)), name="T_Stueck", color=C["dark"])
assy.add(cyl(FEED_D + 30, 40, (-850, SWIRL_Y, 250), (1, 0, 0)), name="Injektor", color=C["dark"])

# ---------------------------------------------------------------- Bunker + Schleuse
bx, by = -600, SWIRL_Y
hopper = (cq.Workplane("XY", origin=(bx, by, 700)).rect(200, 200)
          .workplane(offset=600).rect(650, 650).loft().val())
assy.add(hopper, name="Bunker_Hackschnitzel", color=C["fuel"])
assy.add(cyl(100, 20, (bx, by, 680)), name="Bunker_Auslauf", color=C["fuel"])
assy.add(cyl(250, 250, (bx, by - 125, 560), (0, 1, 0)), name="Schleuse", color=C["dark"])
assy.add(box(120, 120, 120, (bx, by - 190, 560)), name="Schleuse_Antrieb", color=C["chra"])
assy.add(pipe([(bx, by, 435), (bx, by, 250)], FEED_D), name="Fallrohr", color=C["fuel"])

# ---------------------------------------------------------------- Asche + Startbrenner
assy.add(pipe([(0, 0, -JACKET_GAP - 3), (0, 0, -250)], 80), name="Ascheaustrag", color=C["steel"])
assy.add(cyl(200, 200, (0, -100, -340), (0, 1, 0)), name="Ascheschleuse", color=C["dark"])
assy.add(box(260, 260, 200, (0, 0, -560)), name="Aschebehaelter", color=C["chra"])
assy.add(pipe([(jd / 2, 0, 320), (480, 0, 320)], 60), name="Startbrenner_Rohr", color=C["burner"])
assy.add(box(160, 130, 130, (560, 0, 320)), name="Startbrenner_Propan", color=C["burner"])

# ---------------------------------------------------------------- Abgas mit Kühlmantel + Schalldämpfer-WT
exh_pts = [(NBK_X, ty + 40, TURBO_Z), (NBK_X, MUF_Y, TURBO_Z), (NBK_X, MUF_Y, MUF_Z + MUF_D / 2)]
assy.add(pipe(exh_pts, EXH_JACKET_D), name="Abgasrohr_Kuehlmantel", color=C["exh"])
assy.add(pipe(exh_pts, EXH_D - 20), name="Abgasrohr_innen", color=C["gas"])

mx0, mx1 = MUF_X0, MUF_X0 + MUF_L
muf_shell = tube(MUF_D, MUF_D - 6, MUF_L, (mx0, MUF_Y, MUF_Z), (1, 0, 0))
for x in (mx0, mx1 - 6):
    muf_shell = muf_shell.fuse(cyl(MUF_D, 6, (x, MUF_Y, MUF_Z), (1, 0, 0)))
# Trennwände mit versetzten Durchtrittsöffnungen (3 Kammern)
for i, x in enumerate((mx0 + MUF_L / 3, mx0 + 2 * MUF_L / 3)):
    wall = cyl(MUF_D - 6, 6, (x, MUF_Y, MUF_Z), (1, 0, 0))
    hz = MUF_Z + (-140 if i == 0 else 140)
    wall = wall.cut(cyl(140, 6, (x, MUF_Y, hz), (1, 0, 0)))
    muf_shell = muf_shell.fuse(wall)
mj = MUF_D + 2 * MUF_JACKET
muf_jacket = tube(mj + 6, mj, MUF_L + 60, (mx0 - 30, MUF_Y, MUF_Z), (1, 0, 0))
assy.add(cutaway(muf_shell, (0, MUF_Y, 0)), name="Schalldaempfer_WT_3_Kammern", color=C["steel"])
assy.add(cutaway(muf_jacket, (0, MUF_Y, 0)), name="Schalldaempfer_Kuehlmantel", color=C["water"])
# Kamin
assy.add(pipe([(mx1 - 150, MUF_Y, MUF_Z + MUF_D / 2), (mx1 - 150, MUF_Y, 2000)], EXH_D),
         name="Kamin", color=C["steel"])
# Kondensat
assy.add(pipe([(mx1 - 150, MUF_Y, MUF_Z - mj / 2), (mx1 - 150, MUF_Y, -100)], 34),
         name="Kondensatablauf", color=C["water"])

# ---------------------------------------------------------------- Kühlwasser-Stutzen
assy.add(pipe([(-jd / 2 + 40, -60, KEG_H - 20), (-jd / 2 + 40, -60, KEG_H + 160)], 60),
         name="VL_Vorlauf", color=C["water"])
assy.add(pipe([(mx0 + 100, MUF_Y, MUF_Z - mj / 2), (mx0 + 100, MUF_Y, -100)], 60),
         name="RL_Ruecklauf", color=C["water"])

# ---------------------------------------------------------------- Export
assy.export(str(OUT / "thor.step"))
assy.export(str(OUT / "thor.glb"))
print("geschrieben:", OUT / "thor.step", OUT / "thor.glb")
