# THOR – 3D-Konzeptmodell

| Datei | Wofür |
|---|---|
| `thor.step` | Fusion 360 / FreeCAD: *Datei → Öffnen* (Baugruppe mit 40 benannten Bauteilen und Farben) |
| `thor.glb` | Blender: *Datei → Importieren → glTF 2.0*. Maße sind mm, in Blender ggf. auf 0,001 skalieren. |
| `thor_modell.py` | Parametrisches Quellmodell (CadQuery). Maße oben im Skript ändern und neu erzeugen. |
| `viewer.html` | Web-Viewer für das GLB |

Neu erzeugen:

```bash
pip install cadquery
python3 thor_modell.py
```

Keg, Nachbrennkammer und Schalldämpfer sind im Viertelschnitt modelliert, damit man hineinsieht.
Rohre sind Vollkörper (Layoutmodell, keine Fertigungszeichnung).
