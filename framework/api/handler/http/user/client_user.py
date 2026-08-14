from framework.api.client.http.http_client import APIClient


def create(*, data: dict, expected_status: int = 201) -> dict:
    client = APIClient()
    return client.post_json(path="/users", json=data, expected_status=expected_status)


def get_user_by_id(*, user_id: int, expected_status: int = 200) -> dict:
    client = APIClient()
    return client.get_json(path=f"users/{user_id}", expected_status=expected_status)


def get_all_users(*, expected_status: int = 200) -> list[dict]:
    client = APIClient()
    return client.get_json(path="/users", expected_status=expected_status)


def delete_user(*, user_id: int, expected_status: int = 204) -> dict:
    client = APIClient()
    return client.delete_json(path=f"/users/{user_id}", expected_status=expected_status)


def update_user(*, user_id: int, data: dict, expected_status: int = 200) -> None:
    client = APIClient()
    client.put(path=f"/users/{user_id}", json=data, expected_status=expected_status)


def get_user_by_name(*, name: str, expected_status: int = 200) -> list[dict]:
    client = APIClient()
    return client.post_json(path="/users/name", json={"name": name}, expected_status=expected_status)
