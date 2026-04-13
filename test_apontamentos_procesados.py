from __future__ import annotations

from services.workflows.apontamento_procesado_service import ApontamentoProcesadoService


apontamento_procesado_service = ApontamentoProcesadoService()

resultado = apontamento_procesado_service.listar_apontamentos_pendientes_estacion_actual(
    limit=20,
    solo_finalizados=True,
    solo_con_num_ordem=True,
)

contexto = resultado["contexto"]
pendientes = resultado["apontamientos_pendientes"]

print(f"EstaciÃ³n local: {contexto['estacion']}")
print(f"Total pendientes antes de registrar: {len(pendientes)}")
print()

if not pendientes:
    print("No hay apuntamientos pendientes para registrar.")
else:
    registrados = apontamento_procesado_service.registrar_apontamientos_procesados(
        apontamientos=pendientes,
        contexto=contexto,
        estado="pendiente_formulario",
    )

    print(f"Total registrados en storage/apontamentos_procesados.json: {len(registrados)}")
    print()

    for registro in registrados:
        print(registro)
