from __future__ import annotations

from services.apontamento_procesado_service import ApontamentoProcesadoService


apontamento_procesado_service = ApontamentoProcesadoService()

resultado = apontamento_procesado_service.listar_apontamientos_pendientes_estacion_actual(
    limit=20,
    solo_finalizados=True,
    solo_con_num_ordem=True,
)

contexto = resultado["contexto"]
pendientes = resultado["apontamientos_pendientes"]

print(f"Estación local: {contexto['estacion']}")
print(f"CodRecursos homologados: {contexto['cod_recursos']}")
print(f"Total consultados: {resultado['total_consultados']}")
print(f"Total pendientes: {resultado['total_pendientes']}")
print(
    "Total omitidos por ya procesados: "
    f"{resultado['total_omitidos_ya_procesados']}"
)
print(
    "Total omitidos por NumOrdem vacío: "
    f"{resultado['total_omitidos_sin_num_ordem']}"
)
print()

for row in pendientes:
    print(row)