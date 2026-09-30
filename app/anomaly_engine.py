import duckdb
from app.config import DATABASE_PATH

class AnomalyEngine:
    def detect(self):
        con = duckdb.connect(DATABASE_PATH, read_only=True)
        try:
            df = con.execute("SELECT * FROM tickets").fetchdf()
        finally:
            con.close()

        anomalies = []

        resolution = df["resolution_time_hrs"].dropna()
        if not resolution.empty:
            q1 = resolution.quantile(0.25)
            q3 = resolution.quantile(0.75)
            upper = q3 + 1.5 * (q3 - q1)

            for _, row in df[df["resolution_time_hrs"] > upper].iterrows():
                anomalies.append({
                    "ticket_id": row["ticket_id"],
                    "type": "long_resolution_time",
                    "severity": "high",
                    "value": float(row["resolution_time_hrs"]),
                    "threshold": float(upper),
                    "description": "Resolution time is unusually high.",
                })

        max_created = df["created_at"].max()
        age_hours = (max_created - df["created_at"]).dt.total_seconds() / 3600

        old_high = df[
            (df["status"] != "Resolved") &
            (df["priority"].isin(["High", "Critical"])) &
            (age_hours > 24)
        ]

        for idx, row in old_high.iterrows():
            anomalies.append({
                "ticket_id": row["ticket_id"],
                "type": "old_high_priority_unresolved",
                "severity": "critical" if row["priority"] == "Critical" else "high",
                "value": float(age_hours[idx]),
                "threshold": 24,
                "description": "High-priority ticket has remained unresolved for more than 24 hours.",
            })

        response = df["response_time_hrs"].dropna()
        if not response.empty:
            q1 = response.quantile(0.25)
            q3 = response.quantile(0.75)
            upper = q3 + 1.5 * (q3 - q1)

            for _, row in df[df["response_time_hrs"] > upper].iterrows():
                anomalies.append({
                    "ticket_id": row["ticket_id"],
                    "type": "slow_response_time",
                    "severity": "medium",
                    "value": float(row["response_time_hrs"]),
                    "threshold": float(upper),
                    "description": "Response time is unusually high.",
                })

        return anomalies
