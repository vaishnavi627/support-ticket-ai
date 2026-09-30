import re

FORBIDDEN_KEYWORDS = [
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE",
    "TRUNCATE", "GRANT", "REVOKE", "COPY", "ATTACH", "DETACH",
    "INSTALL", "LOAD",
]

def validate_sql(sql: str):
    sql = sql.strip()
    if not sql:
        raise ValueError("Empty SQL query.")

    if ";" in sql.rstrip(";"):
        raise ValueError("Multiple SQL statements are not allowed.")

    normalized = sql.upper().strip()
    if not (normalized.startswith("SELECT") or normalized.startswith("WITH")):
        raise ValueError("Only SELECT queries are allowed.")

    for keyword in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{keyword}\b", normalized):
            raise ValueError(f"Forbidden SQL operation: {keyword}")

    table_matches = re.findall(
        r"\b(?:FROM|JOIN)\s+([a-zA-Z_][a-zA-Z0-9_]*)",
        sql,
        flags=re.IGNORECASE,
    )
    for table in table_matches:
        if table.lower() != "tickets":
            raise ValueError(f"Unauthorized table: {table}")

    for term in ["information_schema", "pg_catalog", "sqlite_master", "pragma"]:
        if term.lower() in sql.lower():
            raise ValueError(f"Unauthorized SQL reference: {term}")

    return True
