import inspect

def test_crypto_module_has_functions():
    import src.backend.crypto as c

    funcs = {
        name: getattr(c, name)
        for name in dir(c)
        if callable(getattr(c, name))
    }

    assert len(funcs) > 0

    # -------------------------------
    # SAFE handling of encrypt_value
    # -------------------------------
    if "encrypt_value" in funcs:
        f = funcs["encrypt_value"]
        args = len(inspect.signature(f).parameters)

        try:
            if args == 1:
                f("hello")
            elif args == 2:
                f("hello", "key123")
            else:
                f(*(["hello"] * args))
        except Exception:
            assert False, "encrypt_value crashed"

    # -------------------------------
    # SAFE handling of decrypt_value
    # -------------------------------
    if "decrypt_value" in funcs:
        f = funcs["decrypt_value"]
        args = len(inspect.signature(f).parameters)

        try:
            dummy = "encrypted-text"
            if args == 1:
                f(dummy)
            elif args == 2:
                f(dummy, "key123")
            else:
                f(*([dummy] * args))
        except Exception:
            assert False, "decrypt_value crashed"

    # password hashing helpers
    if "encrypt_password" in funcs and "verify_password" in funcs:
        h = c.encrypt_password("pass123")
        assert c.verify_password("pass123", h) is True
        assert c.verify_password("wrong", h) is False
