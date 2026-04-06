import pyodbc

server = "172.16.2.251"
database = "MetricsBetaProductivo"
username = "fosorio"
password = "Bop123456+"
driver = "ODBC Driver 18 for SQL Server"

cod_recurso = "CodRecurso"

connection_string = (
    f"DRIVER={{{driver}}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    "TrustServerCertificate=yes;"
)

sql = """
SELECT TOP 20
    [IdApontamento],
    [NumOrdem],
    [CodRecurso],
    [CodSetor],
    [CodAtiv],
    [Turno],
    [HoraFim],
    [Operador],
    [DescricaoOP],
    [DescricaoProcesso],
    [QtdProduzida],
    [QtdPlanejado],
    [QtdPerdas],
    [JustificativaPerda],
    [Obs]
FROM [MetricsBetaProductivo].[dbo].[Apontamentos]
WHERE [HoraFim] IS NOT NULL
  AND [HoraFim] <> '1899-12-30 00:00:00.000'
ORDER BY [HoraFim] DESC
"""

with pyodbc.connect(connection_string) as conn:
    cursor = conn.cursor()
    cursor.execute(sql, (cod_recurso,))
    rows = cursor.fetchall()

    print(f"Total filas obtenidas: {len(rows)}")
    print()

    for row in rows:
        print(row)