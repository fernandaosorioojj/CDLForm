from __future__ import annotations

DB_SERVER = "172.16.2.251"
DB_DATABASE = "MetricsBetaProductivo"
DB_USERNAME = "fosorio"
DB_PASSWORD = "Bop123456+"
DB_DRIVER = "ODBC Driver 18 for SQL Server"
DB_TRUST_SERVER_CERTIFICATE = "yes"


def build_connection_string() -> str:
    return (
        f"DRIVER={{{DB_DRIVER}}};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_DATABASE};"
        f"UID={DB_USERNAME};"
        f"PWD={DB_PASSWORD};"
        f"TrustServerCertificate={DB_TRUST_SERVER_CERTIFICATE};"
    )