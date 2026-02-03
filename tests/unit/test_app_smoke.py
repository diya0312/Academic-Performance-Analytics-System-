import importlib

def test_app_imports():
    mod = importlib.import_module("src.backend.app")
    assert hasattr(mod, "app")

def test_app_has_routes():
    from src.backend.app import app
    routes = [str(r) for r in app.url_map.iter_rules()]
    # Just check important ones exist
    assert any("login" in r for r in routes)
    assert any("settings" in r for r in routes)
    assert any("add_record" in r for r in routes)
