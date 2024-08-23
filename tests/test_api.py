from fastapi.testclient import TestClient
from dotenv import load_dotenv
import os
from app.main import app

load_dotenv()

client = TestClient(app)


def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "Pong!"}


def test_resize_image_no_auth():
    response = client.post("/resize-image?width=100&height=100", files={"file": ("test.png", b"test image content")})
    assert response.status_code == 403


def test_resize_image_invalid_auth():
    headers = {"X-API-Key": "invalid_key"}
    response = client.post("/resize-image?width=100&height=100", headers=headers, files={"file": ("test.png", b"test image content")})
    assert response.status_code == 403


def test_resize_image_invalid_file_type():
    headers = {"X-API-Key": os.getenv("API_KEY")}
    with open("tests/test.txt", "rb") as image:
        files = {"file": ("test_image.txt", image, "text/plain")}
        response = client.post("/resize-image?width=100&height=100", headers=headers, files=files)
        assert response.status_code == 415


def test_resize_image_invalid_dimensions():
    headers = {"X-API-Key": os.getenv("API_KEY")}
    with open("tests/test.jpg", "rb") as image:
        files = {"file": ("test_image.jpg", image, "image/jpeg")}
        response = client.post("/resize-image?width=-100&height=100", headers=headers, files=files)
        assert response.status_code == 400


def test_resize_image_file_too_large():
    headers = {"X-API-Key": os.getenv("API_KEY")}
    with open("tests/test_large.png", "rb") as image:
        files = {"file": ("test_image.jpg", image, "image/jpeg")}
        response = client.post("/resize-image?width=100&height=100", headers=headers, files=files)
        assert response.status_code == 413


def test_resize_image():
    headers = {"X-API-Key": os.getenv("API_KEY")}
    with open("tests/test.jpg", "rb") as image:
        files = {"file": ("test_image.jpg", image, "image/jpeg")}
        response = client.post("/resize-image?width=100&height=100", headers=headers, files=files)
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/jpeg"
        assert response.headers["content-disposition"] == 'attachment; filename="resized_test_image.jpg"'
