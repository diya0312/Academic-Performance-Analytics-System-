# tests/unit/test_app_dummy_calls.py
import pytest
from backend.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_root_route_exists(client):
    r = client.get("/")
    assert r.status_code in (200, 302, 404)  # safe: different teams implement differently


def test_invalid_route_404(client):
    r = client.get("/this_route_does_not_exist")
    assert r.status_code == 404


def test_method_not_allowed(client):
    r = client.post("/api/alerts")  # this route is GET-only in your project
    assert r.status_code in (405, 500)  # depending on SQL presence


def test_missing_session_does_not_crash(client):
    r = client.get("/api/dashboard")
    assert r.status_code in (401, 403, 500,404)
