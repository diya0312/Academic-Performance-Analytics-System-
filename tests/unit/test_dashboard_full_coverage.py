import importlib
import sys
import types
import pytest
import inspect


def make_fake_streamlit(role="student"):
    """Return a fake Streamlit module with a proper attribute-based session_state."""

    # must be attribute-based, NOT a dict
    session_state = types.SimpleNamespace(
        logged_in=True,
        role=role,
        username="testuser",
        last_active=0,
        login_username="u",
        login_password="p",
        requests_session=None
    )

    fake_st = types.SimpleNamespace(
        session_state=session_state,
        error=lambda *a, **k: None,
        success=lambda *a, **k: None,
        warning=lambda *a, **k: None,
        info=lambda *a, **k: None,
        markdown=lambda *a, **k: None,
        button=lambda *a, **k: False,
        text_input=lambda *a, **k: "",
        number_input=lambda *a, **k: 50,
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

    return fake_st


def fake_requests_session():
    """Fake requests.Session() that returns valid JSON always."""
    class FakeRes:
        status_code = 200
        text = ""
        def json(self):
            return {
                "success": True,
                "risk_threshold": 0.5,
                "model_version": "2",
                "processed": 1
            }

    class FakeSess:
        def get(self, *a, **k): return FakeRes()
        def post(self, *a, **k): return FakeRes()

    return FakeSess()


def run_dashboard_import(role):
    """Re-import dashboard under specific role to hit that code block."""

    # ensure fresh import each time
    sys.modules.pop("src.frontend.dashboard", None)

    # mock modules BEFORE importing dashboard
    sys.modules["streamlit"] = make_fake_streamlit(role)
    sys.modules["plotly.express"] = types.SimpleNamespace(
        bar=lambda *a, **k: None,
        scatter=lambda *a, **k: None,
        histogram=lambda *a, **k: None,
    )
    sys.modules["streamlit_autorefresh"] = types.SimpleNamespace(
        st_autorefresh=lambda *a, **k: None
    )

    # patch requests.Session globally before import
    import requests
    requests.Session = lambda: fake_requests_session()

    # import dashboard
    importlib.invalidate_caches()
    importlib.import_module("src.frontend.dashboard")


def test_cover_dashboard_student():
    run_dashboard_import("student")


def test_cover_dashboard_instructor():
    run_dashboard_import("instructor")


def test_cover_dashboard_admin():
    run_dashboard_import("admin")
