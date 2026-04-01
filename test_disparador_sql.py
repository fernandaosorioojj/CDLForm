from services.disparador_service import DisparadorService

def main() -> None:
    service = DisparadorService(
        server=" 172.16.2.251",
        database="MetricsProd",
        username="fosorio",
        password="Bo123456+",
    )

    pendientes = service.buscar_apontamentos_pendientes()
    print(f"Pendientes encontrados: {len(pendientes)}")

    for item in pendientes:
        print(item)

    resultados = service.procesar_pendientes()
    print(f"Procesados: {len(resultados)}")

    for resultado in resultados:
        print(resultado)


if __name__ == "__main__":
    main()