import allure
from hamcrest import assert_that, contains_inanyorder, equal_to, has_entries, is_in, not_, not_none

from framework.factory.items.item_process import ItemProcess
from framework.models.models_items import Item, ItemRequest


@allure.feature("Тестирование менеджмента товаров")
class TestItem:
    @allure.title("Создание валидного товара")
    def test_create_item(self, valid_item: ItemRequest):

        with allure.step("Создание товара"):
            created_item_response = ItemProcess.create_item(item=valid_item)

            assert_that(
                created_item_response.id,
                not_none(),
                "После создания товара не вернулся id",
            )

        with allure.step("Поиск и проверка товара"):
            found_item = ItemProcess.get_item_by_id(item_id=created_item_response.id)

            assert_that(
                found_item.model_dump(),
                has_entries(**valid_item.model_dump()),
                f"Данные товара id={created_item_response.id} не совпадают после получения",
            )

        with allure.step("Получение всех товаров и поиск созданного"):
            all_items = ItemProcess.get_all_items()
            created_item_from_list = None

            for item in all_items:
                if item.id == created_item_response.id:
                    created_item_from_list = item
                    break

            assert_that(
                created_item_from_list, not_none(), f"Товар id={created_item_response.id} не найден в списке товаров"
            )

            assert_that(
                created_item_from_list,
                equal_to(found_item),
                f"Товар id={created_item_response.id} из списка не совпадает с найденным товаром",
            )

    @allure.title("Удаление товара")
    def test_delete_item(self, created_valid_item: Item):
        ItemProcess.delete_item(item_id=created_valid_item.id)

        with allure.step("Проверка, что товар удален"):
            ItemProcess.get_item_by_id(item_id=created_valid_item.id, serialize=False, expected_status=404)

        with allure.step("Проверка, что товара нет в списке"):
            all_items = ItemProcess.get_all_items()
            deleted_item = None

            for item in all_items:
                if item.id == created_valid_item.id:
                    break

            assert_that(
                deleted_item, equal_to(None), f"Товар id={created_valid_item.id} найден в списке после удаления"
            )

    @allure.title("Изменение товара")
    def test_update_item(self, created_valid_item: Item, valid_item: ItemRequest):
        updated_item = valid_item.model_copy()
        updated_item.price = 999999

        with allure.step("Обновление товара"):
            ItemProcess.update_item(item_id=created_valid_item.id, item=updated_item)

        with allure.step("Проверка обновленных данных"):
            updated_item = ItemProcess.get_item_by_id(item_id=created_valid_item.id)

        assert_that(
            updated_item.price,
            equal_to(999999),
            f"Данные товара id={created_valid_item.id} не обновились",
        )

    @allure.title("Получение товаров по имени")
    def test_get_items_by_name(self, created_items: tuple[Item, Item, Item]):

        item1, item2, item3 = created_items

        with allure.step("Получение товаров по имени"):
            found_items = ItemProcess.get_items_by_name(name=item1.name)

            assert_that(len(found_items), equal_to(2), "Количество найденных товаров не соотвествует ожидаемому")

            assert_that(
                found_items,
                contains_inanyorder(item1, item2),
                f"Данные товары {item1} и {item2} не совпадают с созданными",
            )

            assert_that(
                item3,
                not_(is_in(found_items)),
                f"Товар id={item3.id} с именем '{item3.name}' был найден в результатах поиска",
            )
