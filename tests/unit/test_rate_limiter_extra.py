from src.backend.middleware.rate_limiter import rate_limit_check

def test_rate_limit_check_always_true():
    assert rate_limit_check() is True
