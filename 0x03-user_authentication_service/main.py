#!/usr/bin/env python3
"""main.py module for integration test on all endpoints"""

import requests

from app import AUTH

BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """Test the register user endpoint"""

    url = f"{BASE_URL}/users"
    data = {
        "email": email,
        "password": password
    }

    r = requests.post(url, data=data)

    assert r.json() == {"email": f"{email}", "message": "user created"}
    assert r.status_code == 200

    # send same request again, error expected
    r = requests.post(url, data=data)

    assert r.json() == {"message": "email already registered"}
    assert r.status_code == 400


def log_in_wrong_password(email: str, new_passwd: str) -> None:
    """Test log in with wrong password"""

    url = f"{BASE_URL}/sessions"
    data = {
        "email": email,
        "password": new_passwd
    }

    r = requests.post(url, data=data)

    assert r.status_code == 401


def profile_unlogged() -> None:
    """Test for when user is trying to access profile while not logged in"""

    url = f"{BASE_URL}/profile"

    r = requests.get(url)

    assert r.status_code == 403


def log_in(email: str, password: str) -> str:
    """Test for the login endpoint"""

    url = f"{BASE_URL}/sessions"
    data = {
        "email": email,
        "password": password
    }

    r = requests.post(url, data=data)

    if r.status_code == 401:
        return "Invalid login details"

    assert r.status_code == 200
    assert r.json() == {"email": f"{email}", "message": "logged in"}

    return r.cookies.get("session_id")


def profile_logged(session_id: str) -> None:
    """Test for when user is trying to access profile while logged in"""

    url = f"{BASE_URL}/profile"
    cookies = {"session_id": session_id}

    r = requests.get(url, cookies=cookies)

    assert r.status_code == 200
    assert "email" in r.json()

    user = AUTH.get_user_from_session_id(session_id)
    assert user.email == r.json()['email']


def log_out(session_id: str) -> None:
    """Test for the logout endpoint"""

    url = f"{BASE_URL}/sessions"
    cookies = {"session_id": session_id}
    headers = {
        "Content-Type": "application/json"
    }

    r = requests.delete(url, headers=headers, cookies=cookies)

    if r.status_code == 403:
        return "User not logged in"

    assert r.status_code == 200


def reset_password_token(email: str) -> str:
    """Test the get reset password token endpoint"""

    url = f"{BASE_URL}/reset_password"
    data = {"email": email}

    r = requests.post(url, data=data)

    if r.status_code == 403:
        return "User does not exist"

    assert r.status_code == 200
    token = r.json()['reset_token']
    assert r.json() == {"email": f"{email}", "reset_token": f"{token}"}

    return token


def update_password(email: str, reset_token: str, new_passwd: str) -> None:
    """Test the reset password endpoint"""

    url = "{}/reset_password".format(BASE_URL)
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_passwd
    }

    r = requests.put(url, data=data)

    if r.status_code == 403:
        return "Invalid data"

    assert r.json() == {"email": f"{email}", "message": "Password updated"}
    assert r.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
