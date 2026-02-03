def test_app_import_does_not_crash():
    import src.backend.app as app
    assert hasattr(app, "app")
