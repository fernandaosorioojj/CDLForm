from __future__ import annotations

from utils.json_manager import JsonManager


registros = JsonManager.read_json("storage/apontamentos_procesados.json") or []

print(f"Total registros: {len(registros)}")
print()

for registro in registros:
    print(
        {
            "id_apontamento": registro.get("id_apontamento"),
            "num_ordem": registro.get("num_ordem"),
            "estado": registro.get("estado"),
            "id_formulario": registro.get("id_formulario"),
            "observacion": registro.get("observacion"),
        }
    )