import duckdb
from app.config import DATABASE_PATH

def get_connection(read_only=False):
    return duckdb.connect(DATABASE_PATH, read_only=read_only)
