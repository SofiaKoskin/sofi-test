import allure

from framework.api.handler.http.item import client_item as item_handler
from framework.models.models_items import Item, ItemCreateResponse, ItemRequest


class ItemProcess:
    @staticmethod
    def create_item(*, item: ItemRequest | dict, serialize: bool = True, expected_status: int = 201) -> ItemCreateResponse | dict:
        with allure.step(f"Создание товара {item=}"):
            if isinstance(item, ItemRequest):
                response = item_handler.create(data=item.model_dump(mode="json"), expected_status=expected_status)
            elif isinstance(item, dict):
                response = item_handler.create(data=item, expected_status=expected_status)
            else:
                raise ValueError("Непонятный тип у товара")

            if serialize:
                return ItemCreateResponse.model_validate(response)
            else:
                return response

    @staticmethod
    def get_item_by_id(*, item_id: int, serialize: bool = True, expected_status: int = 200) -> Item | dict:
        with allure.step(f"Получение товара по id: {item_id=}"):
            response = item_handler.get_item_by_id(item_id=item_id, expected_status=expected_status)

            if serialize:
                return Item.model_validate(response)
            else:
                return response

    @staticmethod
    def get_all_items(*, serialize: bool = True, expected_status: int = 200) -> list[Item] | list[dict]:
        with allure.step("Получение списка всех товаров"):
            response = item_handler.get_all_items(expected_status=expected_status)

            if serialize:
                return [Item.model_validate(item) for item in response]
            else:
                return response

    @staticmethod
    def delete_item(*, item_id: int, expected_status: int = 204) -> dict:
        with allure.step(f"Удаление товара по id:{item_id=}"):
            return item_handler.delete_item(item_id=item_id, expected_status=expected_status)

    @staticmethod
    def update_item(
        *, item_id: int, item: ItemRequest, expected_status: int = 200) -> None:
        with allure.step(f"Обновление товара id={item_id}"):
            item_handler.update_item(item_id=item_id,data=item.model_dump(mode="json"), expected_status=expected_status)

    @staticmethod
    def get_items_by_name(*, name: str, serialize: bool = True, expected_status: int = 200) -> list[Item] | list[dict]:
        with allure.step(f"Получение товара по имени: {name}"):
            response = item_handler.get_item_by_name(name=name, expected_status=expected_status)

            if serialize:
                return [Item.model_validate(item) for item in response]
            else:
                return response
