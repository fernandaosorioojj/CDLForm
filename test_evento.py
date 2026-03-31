from integrations.event_processor import EventProcessor


processor = EventProcessor()

evento = processor.procesar_evento_externo({
    "IdApontamento": 1001,
    "NumOrdem": "OP-0001",
    "estado_anterior": "En proceso",
    "estado_nuevo": "Terminado",
    "fecha_evento": "2026-03-31 08:30:00",
    "CodRecurso": "MAQ-01",
    "Operador": "Juan Perez",
    "CodAtiv": "ATIV-01",
    "CodSetor": "AREA-LAM",
    "Turno": 1,
    "DtProducao": "2026-03-31",
    "HoraInicio": "2026-03-31 07:00:00",
    "HoraFim": "2026-03-31 08:15:00",
    "DescricaoOP": "Fabricación lote 1",
    "DescricaoProcesso": "Laminado",
    "Obs": "Proceso normal",
    "QtdProduzida": 120,
    "QtdPlanejado": 150,
    "QtdPerdas": 3,
    "JustificativaPerda": "Ajuste inicial"
})

print("=== RESULTADO EVENTO ===")
print(evento)

print("\n=== CAMPOS CLAVE ===")
print("debe_disparar:", evento.get("debe_disparar"))
print("mensaje:", evento.get("mensaje"))
print("contexto_resuelto:", evento.get("contexto_resuelto"))
print("formulario:", evento.get("formulario"))