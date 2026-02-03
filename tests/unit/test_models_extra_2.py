# tests/unit/test_models_extra_2.py
from backend.models import FakeDB, get_db


def test_fake_db_user_lookup_admin():
    db = FakeDB()
    cur = db.cursor()
    cur.execute("SELECT role FROM users WHERE username = %s", ("admin",))
    row = cur.fetchone()
    assert row[0] == "admin"


def test_fake_db_user_insert():
    db = FakeDB()
    cur = db.cursor()
    cur.execute("INSERT INTO users (username, password, role) VALUES (%s,%s,%s)",
                ("new_user", "pass123", "student"))
    cur.close()

    cur2 = db.cursor()
    cur2.execute("SELECT role FROM users WHERE username = %s", ("new_user",))
    row = cur2.fetchone()
    assert row[2] == "student"


def test_fake_db_records_select():
    db = FakeDB()
    cur = db.cursor()
    cur.execute("SELECT * FROM records")
    rows = cur.fetchall()

    assert len(rows) == 1
    assert len(rows[0]) == 9  # correct schema length


def test_get_db_returns_fake_on_failure(monkeypatch):
    import backend.models as models

    def fake_connect_fail(*args, **kwargs):
        raise Exception("No SQL server")

    monkeypatch.setattr("mysql.connector.connect", fake_connect_fail)

    db = models.get_db()
    assert isinstance(db, FakeDB)
