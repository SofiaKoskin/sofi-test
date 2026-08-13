from framework.api.client.http.http_client import APIClient


def create(*, data: dict, expected_status: int = 201) -> dict:
    client = APIClient()
    return client.post_json(path="/items", json=data, expected_status=expected_status)


def get_item_by_id(*, item_id: int, expected_status: int = 200) -> dict:
    client = APIClient()
    return client.get_json(path=f"items/{item_id}", expected_status=expected_status)


def get_all_items(*, expected_status: int = 200) -> list[dict]:
    client = APIClient()
    return client.get_json(path="/items", expected_status=expected_status)


def delete_item(*, item_id: int, expected_status: int = 204) -> dict:
    client = APIClient()
    return client.delete_json(path=f"/items/{item_id}", expected_status=expected_status)


def update_item(*, item_id: int, data: dict, expected_status: int = 200) -> None:
    client = APIClient()
    client.put(path=f"/items/{item_id}", json=data, expected_status=expected_status)


def get_item_by_name(*, name: str, expected_status: int = 200) -> list[dict]:
    client = APIClient()
    return client.post_json(path="/items/name", json={"name": name}, expected_status=expected_status)
