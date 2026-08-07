from symtable import Class

import allure
import pytest

from hamcrest import assert_that, has_entries, equal_to, not_none, contains_inanyorder, not_, is_in, empty

from framework.api.handler.http.item.item import create, delete_item, update_item
from framework.factory.items.item_process import ItemProcess
from framework.models.item import ItemCreate, Item, ItemUpdate
from tests.items.confest import created_valid_item, created_items, valid_item
from tests.items.test_items_happy_path import TestItem


@allure.feature("Негативное тестирование менеджмента товаров")
class TestItemNegative:

    @pytest.mark.parametrize(
        "name",
        [
            pytest.param("", id="empty_name"),
        ]
    )
    @allure.title("Создание товара с пустым названием")
    def test_create_item_empty_name(self, valid_item: ItemCreate, name: str):
        valid_item.name = name

        ItemProcess.create_item(
            item=valid_item,
            expected_status=400,
            serialize=False
        )

    @pytest.mark.parametrize(
        "description",
        [
            pytest.param("", id="empty_description"),
            pytest.param("ab", id="less_than_min"),
            pytest.param("a" * 101, id="more_than_max"),
        ]
    )
    @allure.title("Создание товара с некорректным описанием")
    def test_create_item_invalid_description(self, valid_item: ItemCreate, description: str):
        valid_item.description = description

        ItemProcess.create_item(
            item=valid_item,
            expected_status=400,
            serialize=False
        )

    @allure.title("Получение товара по несуществующему ID")
    def test_item_not_found(self):
        ItemProcess.get_item_by_id(
            item_id=9999999,
            expected_status=404,
            serialize=False
        )

    @pytest.mark.parametrize(
        "item_id",
        [
            pytest.param(-1, id="negative_one"),
            pytest.param(-100, id="negative_one_hundred"),
        ]
    )
    @allure.title("Получение товара с отрицательным ID")
    def test_get_item_negative_id(self, item_id: int):
        ItemProcess.get_item_by_id(
            item_id=item_id,
            expected_status=404,
            serialize=False
        )

    @allure.title("Обновление товара с пустым названием")
    def test_update_item_empty_name(self, created_valid_item: Item):
        created_valid_item.name = ""

        ItemProcess.update_item(
            item_id=created_valid_item.id,
            item=created_valid_item,
            expected_status=400,
            serialize=False
        )

    @allure.title("Обновление несуществующего товара")
    def test_update_non_existent_item(self, valid_item: ItemCreate):
        ItemProcess.update_item(
            item_id=9999999,
            item=valid_item,
            expected_status=404,
            serialize=False
        )

    @allure.title("Удаление несуществующего товара")
    def test_delete_non_existent_item(self):
        ItemProcess.delete_item(
            item_id=9999999,
            expected_status=404
        )

    @allure.title("Получение списка товаров")
    def test_get_all_items(self):
        items = ItemProcess.get_all_items()

        assert_that(
            items,
            not_(empty()),
            "Список товаров пустой"
        )