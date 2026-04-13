from __future__ import annotations

from services.workflows.apontamento_procesado_service import ApontamentoProcesadoService


apontamento_procesado_service = ApontamentoProcesadoService()

resultado = apontamento_procesado_service.crear_formularios_desde_registros_pendientes(
    limit=100
)

print(
    "Total pendientes en cola para crear formulario: "
    f"{resultado['total_pendientes_formulario']}"
)
print(f"Total formularios creados: {resultado['total_formularios_creados']}")
print(f"Total formularios ya existentes: {resultado['total_formularios_existentes']}")
print(f"Total errores: {resultado['total_errores']}")
print()

if resultado["formularios_creados"]:
    print("FORMULARIOS CREADOS")
    for formulario in resultado["formularios_creados"]:
        print(formulario)
    print()

if resultado["formularios_existentes"]:
    print("FORMULARIOS YA EXISTENTES")
    for formulario in resultado["formularios_existentes"]:
        print(formulario)
    print()

if resultado["errores"]:
    print("ERRORES")
    for error in resultado["errores"]:
        print(error)
