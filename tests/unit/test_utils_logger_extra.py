from unittest.mock import patch
from src.backend.utils.logger import log_event

def test_log_event():
    with patch("logging.info") as mock_log:
        log_event("hello")
        mock_log.assert_called_once_with("hello")
