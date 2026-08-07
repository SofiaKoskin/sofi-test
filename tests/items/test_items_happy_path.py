
import allure
import pytest
from hamcrest import assert_that, has_entries, equal_to, not_none, contains_inanyorder, not_,is_in

from framework.api.handler.http.item.item import create, delete_item, update_item
from framework.factory.items.item_process import ItemProcess
from framework.models.item import ItemCreate, Item, ItemUpdate
from tests.items.confest import created_valid_item, valid_item


@allure.feature("Тестирование менеджмента товаров")
class TestItem:

    @allure.title("Создание валидного товара")
    def test_create_item(self, valid_item: ItemCreate):

        with allure.step("Создание товара"):
            created_item = ItemProcess.create_item(item=valid_item)

            assert_that(
                created_item.model_dump(),
                has_entries(**valid_item.model_dump()),
                "В итоговом товаре не совпадают поля с товаром из запроса"
            )


        with allure.step("Получение товара по id и проверка данных"):
            found_item = ItemProcess.get_item_by_id(item_id=created_item.id)

            assert_that(
                found_item.model_dump(),
                has_entries(**valid_item.model_dump()),
                f"Данные товара id={created_item.id} не совпадают после получения"

            )

            assert_that(
                found_item,
                equal_to(created_item),
                f"Товар из get id={found_item.id} не совпадает с товаром из post id={created_item.id}"
            )


        with allure.step("Получение всех товаров и поиск созданного"):
            all_items = ItemProcess.get_all_items()
            created_item_from_list = None

            for item in all_items:
                if item.id == created_item.id:
                    created_item_from_list = item
                    break


            assert_that(
                created_item_from_list,
                not_none(),
                f"Товар id={created_item.id} не найден в списке товаров"
            )


            assert_that(
                created_item_from_list,
                equal_to(created_item),
                f"Товар id={created_item.id} из списка не совпадает с созданным POST"
            )


    @allure.title("Удаление товара")
    def test_delete_item(self, created_valid_item: Item):
        ItemProcess.delete_item(item_id=created_valid_item.id)


        with allure.step("Проверка, что товар удален"):
            ItemProcess.get_item_by_id(item_id=created_valid_item.id,
            serialize=False, expected_status=404)


        with allure.step("Проверка, что товара нет в списке"):
            all_items =  ItemProcess.get_all_items()
            deleted_item = None

            for item in all_items:
                if item.id == created_valid_item.id:
                    deleted_item == item
                    break


            assert_that(
                deleted_item,
                equal_to(None),
                f"Товар id={created_valid_item.id} найден в списке после удаления"
            )





    @allure.title("Изменение товара")
    def test_update_item(self, created_valid_item: Item):
        created_valid_item.price = "999999"

        with allure.step("Обновление товара"):
            updated_item = ItemProcess.update_item(
                item_id=created_valid_item.id,
                item=created_valid_item)


            assert_that(
                updated_item,
                equal_to(created_valid_item),
                f"Данные товара id={created_valid_item.id} не обновились"
            )



