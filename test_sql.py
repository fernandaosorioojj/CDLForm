import pyodbc

tests = [
    (
        "ODBC Driver 18",
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=172.16.2.251;"
        "DATABASE=MetricsBetaProductivo;"
        "UID=fosorio;"
        "PWD=Bop123456+;"
        "Encrypt=no;"
        "TrustServerCertificate=yes;"
    ),
    (
        "SQL Server",
        "DRIVER={SQL Server};"
        "SERVER=172.16.2.251;"
        "DATABASE=MetricsBetaProductivo;"
        "UID=fosorio;"
        "PWD=Bop123456+;"
    ),
]

print("Drivers disponibles:", pyodbc.drivers())
print()

for name, conn_str in tests:
    print(f"Probando: {name}")
    try:
        conn = pyodbc.connect(conn_str, timeout=5)
        cur = conn.cursor()
        cur.execute("SELECT DB_NAME(), GETDATE()")
        row = cur.fetchone()
        print("OK ->", row)
        conn.close()
    except Exception as e:
        print("ERROR ->", repr(e))
    print("-" * 60)
