# tests/unit/test_ml_engine_extra.py
from backend.ml_engine import predict_risk, get_model_version, rebuild_model


def test_predict_risk_bounds_and_types():
    # valid range
    assert 0.0 <= predict_risk(50, 50) <= 1.0

    # out-of-range values (should clamp)
    assert predict_risk(200, -10) == predict_risk(100, 0)

    # invalid type handling
    assert predict_risk("abc", "xyz") == 1.0  # worst case: marks=0, attendance=0


def test_predict_risk_extremes():
    assert predict_risk(100, 100) == 0.0       # best case
    assert predict_risk(0, 0) == 1.0           # worst case
    assert predict_risk(100, 0) > 0
    assert predict_risk(0, 100) > 0


def test_model_version_increment():
    v1 = get_model_version()
    v2 = rebuild_model()
    assert int(v2) == int(v1) + 1

    v3 = rebuild_model()
    assert int(v3) == int(v2) + 1
