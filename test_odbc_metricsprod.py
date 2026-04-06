import pyodbc

server = "172.16.2.251"
database = "MetricsBetaProductivo"
username = "fosorio"
password = "Bop123456+"
driver = "ODBC Driver 18 for SQL Server"

connection_string = (
    f"DRIVER={{{driver}}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    "TrustServerCertificate=yes;"
)

with pyodbc.connect(connection_string) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 1 name FROM sys.tables ORDER BY name")
    row = cursor.fetchone()
    print("Conexión OK")
    print(row)