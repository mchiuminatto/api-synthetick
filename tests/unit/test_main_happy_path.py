import random
from string import ascii_uppercase, digits

from app.main import app
from fastapi.testclient import TestClient
import app.common.constants as const

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Synthetic": f"version {const.VERSION}"}


def test_request_data_date_records():
    response = client.post(
        "api/v1/forex/request/", json={
            "records": 1000,
            "spread_min": 0.0001,
            "spred_max": 0.001,
            "start_date": "2023-01-01T00:00:00",
            "symbol": "EURUSD",
            "trend": 0.1,
            "volatility": 0.01
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "EURUSD"
    assert data["start_date"] == "2023-01-01T00:00:00"
    assert data["records"] == 1000
    assert len(data["request_id"]) == 36


def test_request_data_date_end_date():
    response = client.post(
        "api/v1/forex/request/", json={
            "start_date": "2023-01-01T00:00:00",
            "end_date": "2023-01-10T00:00:00",
            "records": 1000,
            "spread_min": 0.0001,
            "spred_max": 0.001,
            "symbol": "USDJPY",
            "trend": 0.1,
            "volatility": 0.01
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "USDJPY"
    assert data["start_date"] == "2023-01-01T00:00:00"
    assert data["end-date"] == "2023-01-10T00:00:00"
    assert data["records"] == 1000  # Default value
    assert len(data["request_id"]) == 36
    assert data["message"] == "Data generation is not implemented yet."


def test_get_status():
    request_id_mock = "".join(
        random.choice(digits + ascii_uppercase)
        for _ in range(const.REQUEST_ID_SIZE))

    response = client.get(f"api/v1/forex/status/{request_id_mock}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "API is running"
    assert data["records-generated"] == 0


def test_get_actual_data():
    request_id_mock = "".join(
        random.choice(digits + ascii_uppercase)
        for _ in range(const.REQUEST_ID_SIZE))

    response = client.get(f"/forex/data/?request_id={request_id_mock}")
    assert response.status_code == 200
    data = response.json()
    assert data["data"] == []
    assert data["message"] == "Data retrieval is not implemented yet."
