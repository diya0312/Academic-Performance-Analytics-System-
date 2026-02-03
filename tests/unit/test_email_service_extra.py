# tests/unit/test_email_service_extra.py
import pytest
from unittest.mock import patch, MagicMock
import email

from backend.email_service import send_alert_email


def test_send_alert_email_success():
    """Ensure SMTP is called correctly and no exception is raised."""
    
    mock_smtp = MagicMock()
    with patch("smtplib.SMTP", return_value=mock_smtp):
        send_alert_email(
            to_email="test@example.com",
            student_name="Alice",
            risk_score=0.85,
            course="CSE101",
            instructor="Dr. Smith"
        )

    # SMTP was initialized
    mock_smtp.starttls.assert_called_once()
    mock_smtp.login.assert_called_once()
    mock_smtp.sendmail.assert_called_once()
    mock_smtp.quit.assert_called_once()


def test_send_alert_email_failure():
    """Simulate an SMTP failure but ensure the function handles it gracefully."""
    
    with patch("smtplib.SMTP", side_effect=Exception("SMTP DOWN")):
        # Should NOT raise an exception
        send_alert_email(
            to_email="abc@xyz.com",
            student_name="Bob",
            risk_score=0.92,
            course="CSE102",
            instructor="Prof X"
        )
