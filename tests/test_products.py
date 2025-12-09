def test_create_product_success(client):
    payload = {
        "name": "Iphone 15",
        "price": 999.99,
        "description": "Apple Phone"
    }
    response = client.post("/products/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Iphone 15"
    assert data["id"] is not None


def test_create_product_validation_error(client):
    payload = {"name": "Bad Product", "price": -10}
    response = client.post("/products/", json=payload)
    assert response.status_code == 422


def test_get_product_success(client):
    payload = {"name": "Samsung S24", "price": 800}
    create_resp = client.post("/products/", json=payload)
    product_id = create_resp.json()["id"]

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Samsung S24"


def test_get_product_not_found(client):
    response = client.get("/products/99999")
    assert response.status_code == 404
    assert response.json()["error"] == "Not Found"


def test_product_auth_failure(client):
    del client.headers["X-API-Key"]
    response = client.get("/products/1")
    assert response.status_code == 401
