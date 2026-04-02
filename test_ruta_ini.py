from pathlib import Path

ruta = Path(r"C:\JOBTRACK\jobtrack.ini")

print("Existe:", ruta.exists())
print("Ruta:", ruta)

if ruta.exists():
    print(ruta.read_text(encoding="utf-8"))