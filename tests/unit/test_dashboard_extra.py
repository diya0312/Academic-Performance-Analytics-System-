import sys
import types
import pytest


# ---------------------------------------------------------------------
# FIXED Streamlit SessionState mock
# ---------------------------------------------------------------------
class SessionState(dict):
    """
    Behaves like Streamlit session_state:
    - dict-like:  "key" in session_state
    - attribute-like: session_state.key
    """
    def __getattr__(self, name):
        return self.get(name)
    def __setattr__(self, name, value):
        self[name] = value


@pytest.fixture
def dashboard_module(monkeypatch):
    """
    Import dashboard module safely by mocking Streamlit and all UI dependencies,
    so ONLY helper functions execute.
    """

    # -----------------------
    # Mock Streamlit Module
    # -----------------------
    fake_st = types.SimpleNamespace(
        session_state=SessionState(),      # <<< FIXED SESSION STATE
        error=lambda *a, **k: None,
        success=lambda *a, **k: None,
        warning=lambda *a, **k: None,
        info=lambda *a, **k: None,
        markdown=lambda *a, **k: None,
        button=lambda *a, **k: False,
        text_input=lambda *a, **k: "",
        number_input=lambda *a, **k: 0,
        file_uploader=lambda *a, **k: None,
        dataframe=lambda *a, **k: None,
        plotly_chart=lambda *a, **k: None,
        columns=lambda *a, **k: (None, None),
        title=lambda *a, **k: None,
        subheader=lambda *a, **k: None,
        sidebar=types.SimpleNamespace(
            title=lambda *a, **k: None,
            write=lambda *a, **k: None,
        ),
        stop=lambda: None,
        rerun=lambda: None,
        set_page_config=lambda *a, **k: None,
    )

    monkeypatch.setitem(sys.modules, "streamlit", fake_st)

    # ------------------------------
    # Mock plotly + autorefresh
    # ------------------------------
    fake_px = types.SimpleNamespace(
        bar=lambda *a, **k: None,
        scatter=lambda *a, **k: None,
        histogram=lambda *a, **k: None,
    )
    monkeypatch.setitem(sys.modules, "plotly.express", fake_px)

    fake_refresh = types.SimpleNamespace(
        st_autorefresh=lambda *a, **k: None
    )
    monkeypatch.setitem(sys.modules, "streamlit_autorefresh", fake_refresh)

    # ------------------------------
    # Import dashboard AFTER mocks
    # ------------------------------
    import importlib
    mod = importlib.import_module("src.frontend.dashboard")
    return mod


# ---------------------------------------------------------------------
# TESTS
# ---------------------------------------------------------------------

def test_safe_json_valid(dashboard_module):
    class FakeRes:
        def json(self):
            return {"ok": True}
        text = ""
        status_code = 200

    out = dashboard_module.safe_json(FakeRes())
    assert out == {"ok": True}


def test_safe_json_invalid_fallback(dashboard_module):
    class FakeRes:
        def json(self):
            raise ValueError("no json")

        text = "error-text"
        status_code = 500

    out = dashboard_module.safe_json(FakeRes())
    assert out["success"] is False
    assert out["message"] == "error-text"
    assert out["status_code"] == 500


def test_get_requests_session_singleton(dashboard_module):
    s1 = dashboard_module.get_requests_session()
    s2 = dashboard_module.get_requests_session()
    assert s1 is s2


def test_fetch_settings_success(monkeypatch, dashboard_module):
    class FakeRes:
        status_code = 200
        def json(self):
            return {"risk_threshold": 0.75, "model_version": "10"}

    class FakeSess:
        def get(self, *a, **k):
            return FakeRes()

    monkeypatch.setattr(dashboard_module, "get_requests_session", lambda: FakeSess())
    settings = dashboard_module.fetch_settings()

    assert settings["risk_threshold"] == 0.75
    assert settings["model_version"] == "10"


def test_fetch_settings_failure(monkeypatch, dashboard_module):
    class FakeBadRes:
        status_code = 500
        def json(self):
            return {"x": "y"}

    class FakeSess:
        def get(self, *a, **k):
            return FakeBadRes()

    monkeypatch.setattr(dashboard_module, "get_requests_session", lambda: FakeSess())
    settings = dashboard_module.fetch_settings()

    assert settings["risk_threshold"] == 0.6
    assert settings["model_version"] == "1"
