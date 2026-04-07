from __future__ import annotations

from services.apontamento_procesado_service import ApontamentoProcesadoService


apontamento_procesado_service = ApontamentoProcesadoService()

resultado = apontamento_procesado_service.sincronizar_y_crear_formularios_estacion_actual(
    limit_consulta=50,
    limit_creacion=50,
    solo_finalizados=True,
    solo_con_num_ordem=True,
)

contexto = resultado["contexto"]

print(f"Estación local: {contexto['estacion']}")
print(f"CodRecursos homologados: {contexto['cod_recursos']}")
print(f"Total consultados: {resultado['total_consultados']}")
print(f"Total pendientes nuevos: {resultado['total_pendientes_nuevos']}")
print(f"Total registrados en cola: {resultado['total_registrados_en_cola']}")
print(f"Total formularios creados: {resultado['total_formularios_creados']}")
print(f"Total formularios ya existentes: {resultado['total_formularios_existentes']}")
print(f"Total errores de formulario: {resultado['total_errores_formulario']}")
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