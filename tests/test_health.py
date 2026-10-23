def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["app"] == "RevCount"
    assert "timestamp" in data


def test_metrics_endpoint(client):
    response = client.get("/api/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "total_indexed_documents" in data
    assert "cache_hit_rate_pct" in data


def test_companies_endpoint(client):
    response = client.get("/api/companies")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 5
