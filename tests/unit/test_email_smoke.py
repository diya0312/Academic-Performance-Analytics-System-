def test_email_send_function_exists():
    from src.backend.email_service import send_alert_email
    assert callable(send_alert_email)
