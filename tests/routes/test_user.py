from fastapi.testclient import TestClient

from app.server.app import app
from app.server.database.security import verify_password, get_hashed_password
from app.server.auth.auth_handler import decodeJWT

from .faker import (fake_user_login, user_login, new_user_signup, existing_user_signup)

client = TestClient(app)

def test_login_success():
    """Test login is working"""
    response = client.post(
        "v1/users/login",
        json=user_login
    )
    jsonres = response.json()

    assert jsonres["access_token"] is not None
    assert response.status_code == 200
    
def test_login_fail():
    """Test token is not returned when login infos are incorrect"""
    response = client.post(
        "v1/users/login",
        json=fake_user_login
    )
    jsonres = response.json()

    assert jsonres["detail"] == "Wrong login details!"
    assert response.status_code == 401
    
def test_signup_fail():
    """Test signup with already existing user"""
    response = client.post("v1/users/signup",
        json=existing_user_signup
    )
    jsonres = response.json()

    assert jsonres["detail"] == "User Already Exists"
    assert response.status_code == 401
