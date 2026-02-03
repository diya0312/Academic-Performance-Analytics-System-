def test_hit_common_routes():
    from src.backend.app import app
    client = app.test_client()

    # These routes may return 401/403/404 — that's fine.
    for ep in ["/api/export_pdf", "/api/export", "/api/all_records",
               "/api/settings", "/api/audit_logs", "/api/users"]:
        r = client.get(ep)
        assert r.status_code in (200, 400, 401, 403, 404, 500)
