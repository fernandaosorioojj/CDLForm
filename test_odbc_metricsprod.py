from __future__ import annotations

import pyodbc

from config.sql_server_config import build_connection_string


connection_string = build_connection_string()

sql = """
SELECT DISTINCT
    LTRIM(RTRIM([CodRecurso])) AS CodRecurso
FROM [dbo].[Apontamentos]
WHERE [CodRecurso] LIKE ?
   OR [CodRecurso] LIKE ?
   OR [CodRecurso] LIKE ?
   OR [CodRecurso] LIKE ?
ORDER BY CodRecurso
"""

with pyodbc.connect(connection_string) as conn:
    cursor = conn.cursor()
    cursor.execute(sql, ("%77%", "%UTECO%", "%MONTAJE%", "%LAMIN%"))
    rows = cursor.fetchall()

    print("CodRecursos encontrados:")
    for row in rows:
        print(row[0])