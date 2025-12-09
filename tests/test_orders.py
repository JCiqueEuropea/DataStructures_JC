import pytest


@pytest.fixture
def product_iphone(client):
    resp = client.post("/products/", json={"name": "Iphone", "price": 1000})
    return resp.json()


@pytest.fixture
def product_charger(client):
    resp = client.post("/products/", json={"name": "Charger", "price": 50})
    return resp.json()


def test_create_order_success(client, product_iphone, product_charger):
    payload = {
        "items": [
            {"product_id": product_iphone["id"], "quantity": 1},
            {"product_id": product_charger["id"], "quantity": 2}
        ]
    }
    response = client.post("/orders/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "Pending"
    assert len(data["items"]) == 2
    assert data["items"][0]["product_id"] == product_iphone["id"]


def test_create_order_product_not_found(client):
    payload = {
        "items": [{"product_id": 9999, "quantity": 1}]
    }
    response = client.post("/orders/", json=payload)

    assert response.status_code == 409
    assert "does not exist" in response.json()["message"]


def test_create_order_duplicate_products(client, product_iphone):
    payload = {
        "items": [
            {"product_id": product_iphone["id"], "quantity": 1},
            {"product_id": product_iphone["id"], "quantity": 2}
        ]
    }
    response = client.post("/orders/", json=payload)
    assert response.status_code == 422


def test_get_all_orders(client, product_iphone):
    payload = {"items": [{"product_id": product_iphone["id"], "quantity": 1}]}
    client.post("/orders/", json=payload)
    client.post("/orders/", json=payload)

    response = client.get("/orders/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_order_status(client, product_iphone):
    create_resp = client.post("/orders/", json={"items": [{"product_id": product_iphone["id"], "quantity": 1}]})
    order_id = create_resp.json()["id"]

    update_payload = {"status": "Shipped"}
    response = client.put(f"/orders/{order_id}", json=update_payload)
    assert response.status_code == 200
    assert response.json()["status"] == "Shipped"

    get_resp = client.get(f"/orders/{order_id}")
    assert get_resp.json()["status"] == "Shipped"


def test_update_order_items(client, product_iphone, product_charger):
    create_resp = client.post("/orders/", json={"items": [{"product_id": product_iphone["id"], "quantity": 1}]})
    order_id = create_resp.json()["id"]

    update_payload = {
        "items": [{"product_id": product_charger["id"], "quantity": 5}]
    }
    response = client.put(f"/orders/{order_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == product_charger["id"]
    assert data["items"][0]["quantity"] == 5


def test_delete_order(client, product_iphone):
    create_resp = client.post("/orders/", json={"items": [{"product_id": product_iphone["id"], "quantity": 1}]})
    order_id = create_resp.json()["id"]

    response = client.delete(f"/orders/{order_id}")
    assert response.status_code == 200

    get_resp = client.get(f"/orders/{order_id}")
    assert get_resp.status_code == 404
