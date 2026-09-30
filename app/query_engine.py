import duckdb
from app.config import DATABASE_PATH
from app.llm.groq_client import GroqClient
from app.sql_validator import validate_sql

class QueryEngine:
    def __init__(self):
        self.llm = GroqClient()

    def execute(self, question: str):
        sql = self.llm.generate_sql(question)
        validate_sql(sql)

        con = duckdb.connect(DATABASE_PATH, read_only=True)
        try:
            result = con.execute(sql)
            columns = [d[0] for d in result.description]
            rows = result.fetchall()
            data = [dict(zip(columns, row)) for row in rows]
        finally:
            con.close()

        return {
            "question": question,
            "sql": sql,
            "answer": self._format_answer(data),
            "data": data,
        }

    @staticmethod
    def _format_answer(data):
        if not data:
            return "No matching records were found."
        if len(data) == 1 and len(data[0]) == 1:
            key, value = next(iter(data[0].items()))
            return f"The result is {value}."
        if len(data) == 1:
            return ", ".join(f"{k}: {v}" for k, v in data[0].items()) + "."
        return f"I found {len(data)} matching records."
