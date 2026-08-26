import allure
from hamcrest import (
    assert_that,
    contains_inanyorder,
    equal_to,
    has_entries,
    has_item,
    has_length,
    none,
    not_,
    not_none,
)

from framework.factory.user.user_process import UserProcess
from framework.models.models_user import User, UserRequest


@allure.feature("Тестирование менеджмента пользователей")
class TestUser:
    @allure.title("Создание валидного пользователя")
    @allure.link("https://link-to-some-ticket.com")
    def test_create_user(self, valid_user: UserRequest):

        with allure.step("Создание пользователя"):
            created_user_response = UserProcess.create_user(user=valid_user)
            assert_that(
                created_user_response.id,
                not_none(),
                "После создания пользователя не вернулся id",
            )

        with allure.step("Поиск и проверка пользователя"):
            found_user = UserProcess.get_user_by_id(user_id=created_user_response.id)

            assert_that(
                found_user.model_dump(),
                has_entries(**valid_user.model_dump()),
                f"Данные пользователя id={created_user_response.id} не совпадают после получения",
            )

        with allure.step("Получение всех пользователей и поиск зозданного"):
            all_users = UserProcess.get_all_users()

            created_user_from_list = None

            for user in all_users:
                if user.id == created_user_response.id:
                    created_user_from_list = user
                    break

            assert_that(
                created_user_from_list,
                not_none(),
                f"Пользователь id={created_user_response.id} не найден в списке пользователей",
            )

            assert_that(
                created_user_from_list,
                equal_to(found_user),
                f"Пользователь id={created_user_response.id} из списка не совпадает с пользовавтелем, созданным через POST",
            )

    @allure.title("Удаление пользователя")
    def test_delete_user(self, created_valid_user: User):
        UserProcess.delete_user(user_id=created_valid_user.id)

        with allure.step("Проверка, что пользоваетль удален"):
            UserProcess.get_user_by_id(user_id=created_valid_user.id, serialize=False, expected_status=404)

        with allure.step("Проверка, что пользователя нет в списке"):
            all_users = UserProcess.get_all_users()
            deleted_user = None
            for user in all_users:
                if user.id == created_valid_user.id:
                    deleted_user = user
                    break

            assert_that(deleted_user, none(), f"Пользователь id={created_valid_user.id} найден в списке после удаления")

    @allure.title("Изменение пользователя")
    def test_update_user(self, created_valid_user: User, valid_user: UserRequest):

        update_user = valid_user.model_copy()
        update_user.age = 25

        with allure.step("Обновление пользователя"):
            UserProcess.update_user(user_id=created_valid_user.id, user=update_user)

        with allure.step("Проверка обновленных данных"):
            updated_user = UserProcess.get_user_by_id(user_id=created_valid_user.id)

        assert_that(updated_user.age, equal_to(25), f"Данные пользователя id={created_valid_user.id} не обновились")

    @allure.title("Получение пользователей по имени")
    def test_get_users_by_name(self, created_users: tuple[User, User, User]):

        user1, user2, user3 = created_users

        with allure.step("Получение пользователей по имени"):
            found_users = UserProcess.get_users_by_name(name=user1.name)

            assert_that(found_users, has_length(2), "Количество найденных пользователей не соотвествует ожидаемому")

            assert_that(
                found_users,
                contains_inanyorder(user1, user2),
                "Получены не те пользователи",
            )

            assert_that(
                found_users, not_(has_item(user3)), "Пользователь с другим именем был найден в результатах поиска"
            )
