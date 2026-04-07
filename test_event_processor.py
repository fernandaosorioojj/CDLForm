from __future__ import annotations

from integrations.event_processor import EventProcessor


event_processor = EventProcessor()

resultado = event_processor.procesar_ciclo_estacion_actual(
    limit_consulta=50,
    limit_creacion=50,
    solo_finalizados=True,
    solo_con_num_ordem=True,
)

contexto = resultado["contexto"]
disparo = resultado["resultado_disparo"]

print(f"Estación local: {contexto['estacion']}")
print(f"CodRecursos homologados: {contexto['cod_recursos']}")
print(f"Total consultados: {resultado['total_consultados']}")
print(f"Total pendientes nuevos: {resultado['total_pendientes_nuevos']}")
print(f"Total registrados en cola: {resultado['total_registrados_en_cola']}")
print(f"Total formularios creados: {resultado['total_formularios_creados']}")
print(f"Total formularios ya existentes: {resultado['total_formularios_existentes']}")
print(f"Total errores de formulario: {resultado['total_errores_formulario']}")
print(f"Se abrió formulario: {disparo['se_abrio']}")
print(f"Motivo disparo: {disparo['motivo']}")

if disparo["formulario"]:
    print(disparo["formulario"])