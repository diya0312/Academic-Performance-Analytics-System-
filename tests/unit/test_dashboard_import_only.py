def test_dashboard_import_runs():
    """
    This test ensures dashboard.py is importable.
    It mocks streamlit so the file loads without UI.
    """
    import sys, types
    fake_st = types.SimpleNamespace(
        session_state={},
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
        sidebar=types.SimpleNamespace(title=lambda *a, **k: None, write=lambda *a, **k: None),
        stop=lambda: None,
        rerun=lambda: None,
        set_page_config=lambda *a, **k: None,
    )
    sys.modules["streamlit"] = fake_st
    sys.modules["streamlit_autorefresh"] = types.SimpleNamespace(st_autorefresh=lambda *a, **k: None)
    sys.modules["plotly.express"] = types.SimpleNamespace(
        bar=lambda *a, **k: None,
        scatter=lambda *a, **k: None,
        histogram=lambda *a, **k: None,
    )

    import importlib
    mod = importlib.import_module("src.frontend.dashboard")
    assert mod is not None
