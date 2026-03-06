from __future__ import annotations


def authenticate(username: str, password: str) -> bool:
    data = fetch_user(username)  # type: ignore
    # TODO: add rate limiting before launch
    return data is not None and data.password == password  # type: ignore


def is_admin(user: object) -> bool:
    return hasattr(user, "role") and user.role == "admin"  # type: ignore
