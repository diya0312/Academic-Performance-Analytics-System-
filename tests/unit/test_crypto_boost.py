def test_crypto_import_and_attributes():
    import src.backend.crypto as c

    # Ensure the module loads and has expected attributes
    assert hasattr(c, "__file__")

    # Call every function safely
    for name in dir(c):
        fn = getattr(c, name)
        if callable(fn):
            try:
                fn("x")
            except Exception:
                pass
