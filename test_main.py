import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base, get_db

TEST_DATABASE_URL = "sqlite:///./test1.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def get_token():
    response = client.post("/login/", data={"username": "admin", "password": "pass@123"})
    assert response.status_code == 200
    return response.json()["access_token"]


def test_health_check():
    response = client.get("/health/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_login():
    response = client.post("/login/", data={"username": "admin", "password": "pass@123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_create_user(get_token):
    headers = {"Authorization": f"Bearer {get_token}"}
    payload = {"name": "Mohan Raj", "email": "Mohan@Raj.com", "age": 23}
    response = client.post("/user/", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == payload["name"]

def test_get_user(get_token):
    headers = {"Authorization": f"Bearer {get_token}"}
    payload = {"name": "Mohan Get", "email": "Mohan@Get.com", "age": 23}
    response = client.post("/user/", json=payload, headers=headers)
    user_id = response.json()["user_id"]

    response = client.get(f"/user/{user_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == payload["name"]

def test_update_user(get_token):
    headers = {"Authorization": f"Bearer {get_token}"}
    payload = {"name": "Mohan Update", "email": "Mohan@Update.com", "age": 24}
    response = client.post("/user/", json=payload, headers=headers)
    user_id = response.json()["user_id"]

    update_payload = {"name": "Updated Mohan", "email": "updated@mohan.com", "age": 23}
    response = client.put(f"/user/{user_id}", json=update_payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Mohan"

def test_delete_user(get_token):
    headers = {"Authorization": f"Bearer {get_token}"}
    payload = {"name": "Delete Mohan", "email": "delete@mohan.com", "age": 23}
    response = client.post("/user/", json=payload, headers=headers)
    user_id = response.json()["user_id"]

    response = client.delete(f"/user/{user_id}", headers=headers)
    assert response.status_code == 204

    response = client.get(f"/user/{user_id}", headers=headers)
    assert response.status_code == 404

