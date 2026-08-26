import allure
import pytest
from hamcrest import assert_that, empty, not_

from framework.factory.items.item_process import ItemProcess
from framework.models.models_items import ItemCreateResponse, ItemRequest


@allure.feature("Негативное тестирование менеджмента товаров")
class TestItemNegative:
    @allure.title("Создание товара с пустым названием")
    def test_create_item_empty_name(self, valid_item: ItemRequest):
        item = valid_item.model_copy(update={"name": ""})

        ItemProcess.create_item(item=item, expected_status=400, serialize=False)

    @pytest.mark.parametrize(
        "description",
        [
            pytest.param("", id="empty_description"),
            pytest.param("ab", id="less_than_min"),
            pytest.param("a" * 101, id="more_than_max"),
        ],
    )
    @allure.title("Создание товара с некорректным описанием")
    def test_create_item_invalid_description(self, valid_item: ItemCreateResponse, description: str):
        valid_item.description = description

        ItemProcess.create_item(item=valid_item, expected_status=400, serialize=False)

    @allure.title("Получение товара по несуществующему ID")
    def test_item_not_found(self):
        ItemProcess.get_item_by_id(item_id=9999999, expected_status=404, serialize=False)

    @allure.title("Получение товара с отрицательным ID")
    def test_get_item_negative_id(self):
        ItemProcess.get_item_by_id(item_id=-1, expected_status=404, serialize=False)

    @allure.title("Обновление товара с пустым названием")
    def test_update_item_empty_name(self, created_valid_item: ItemRequest):
        created_valid_item.name = ""
        ItemProcess.update_item(item_id=created_valid_item.id, item=created_valid_item, expected_status=400)

    @allure.title("Обновление несуществующего товара")
    def test_update_non_existent_item(self, valid_item: ItemCreateResponse):
        ItemProcess.update_item(item_id=9999999, item=valid_item, expected_status=404)

    @allure.title("Удаление несуществующего товара")
    def test_delete_non_existent_item(self):
        ItemProcess.delete_item(item_id=9999999, expected_status=404)

    @allure.title("Получение списка товаров")
    def test_get_all_items(self):
        items = ItemProcess.get_all_items()

        assert_that(items, not_(empty()), "Список товаров пустой")
