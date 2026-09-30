def test_anomaly_engine_returns_list():
    from app.ingestion import initialize_database
    from app.anomaly_engine import AnomalyEngine
    initialize_database()
    result = AnomalyEngine().detect()
    assert isinstance(result, list)
