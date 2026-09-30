import duckdb
from app.config import DATABASE_PATH, DATA_PATH

REQUIRED_COLUMNS = [
    "ticket_id", "created_at", "category", "priority", "status",
    "response_time_hrs", "resolution_time_hrs", "agent_id",
    "customer_rating", "issue_summary",
]

def initialize_database():
    con = duckdb.connect(DATABASE_PATH)
    try:
        con.execute("""
            CREATE OR REPLACE TABLE tickets AS
            SELECT * FROM read_csv_auto(?)
        """, [DATA_PATH])
        con.execute("""
            ALTER TABLE tickets
            ALTER COLUMN created_at SET DATA TYPE TIMESTAMP
            USING CAST(created_at AS TIMESTAMP)
        """)
    finally:
        con.close()

def validate_database():
    con = duckdb.connect(DATABASE_PATH, read_only=True)
    try:
        rows = con.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'tickets'
            ORDER BY ordinal_position
        """).fetchall()
        actual = [r[0] for r in rows]
    finally:
        con.close()

    missing = [c for c in REQUIRED_COLUMNS if c not in actual]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return True
