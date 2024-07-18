#!/usr/bin/env python3
""" Main file """
import requests


BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    response = requests.post(
        f"{BASE_URL}/users", data={"email": email, "password": password})
    assert response.status_code == 200, f"\
        Register user failed: {response.text}"


def log_in_wrong_password(email: str, password: str) -> None:
    response = requests.post(
        f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert response.status_code == 401, f"\
        Log in with wrong password failed: {response.text}"


def log_in(email: str, password: str) -> str:
    response = requests.post(
        f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert response.status_code == 200, f"Log in failed: {response.text}"
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403, f"\
                                Profile unlogged failed: {response.text}"


def profile_logged(session_id: str) -> None:
    response = requests.get(
        f"{BASE_URL}/profile", cookies={"session_id": session_id})
    assert response.status_code == 200, f"\
        Profile logged failed: {response.text}"


def log_out(session_id: str) -> None:
    """Tests logging out of a session.
    """
    url = "{}/sessions".format(BASE_URL)
    req_cookies = {
        'session_id': session_id,
    }
    res = requests.delete(url, cookies=req_cookies)
    assert res.status_code == 200
    assert res.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    response = requests.post(
        f"{BASE_URL}/reset_password", data={"email": email})
    assert response.status_code == 200, f"\
        Reset password token failed: {response.text}"
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    response = requests.put(
        f"{BASE_URL}/reset_password",
        data={
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password})
    assert response.status_code == 200, f"\
        Update password failed: {response.text}"


if __name__ == "__main__":
    EMAIL = "guillaume@holberton.io"
    PASSWD = "b4l0u"
    NEW_PASSWD = "t4rt1fl3tt3"

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
