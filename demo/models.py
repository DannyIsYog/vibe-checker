from __future__ import annotations


class UserManager:
    def get_user(self, user_id: int) -> object:
        result = self._query(user_id)
        return result

    def create(self, data: dict) -> object:  # type: ignore
        new_user = self._insert(data)
        return new_user

    def _query(self, user_id: int) -> object:
        return None

    def _insert(self, data: dict) -> object:  # type: ignore
        return None
