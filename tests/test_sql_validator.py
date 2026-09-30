from app.sql_validator import validate_sql

def test_select_allowed():
    assert validate_sql("SELECT COUNT(*) FROM tickets") is True

def test_delete_blocked():
    try:
        validate_sql("DELETE FROM tickets")
        assert False
    except ValueError:
        assert True

def test_drop_blocked():
    try:
        validate_sql("DROP TABLE tickets")
        assert False
    except ValueError:
        assert True
