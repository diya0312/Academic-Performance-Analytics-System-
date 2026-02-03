def test_dashboard_import_safe():
    import importlib
    mod = importlib.import_module("src.frontend.dashboard")
    assert mod is not None
