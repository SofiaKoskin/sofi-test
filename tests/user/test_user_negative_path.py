import allure
import pytest
from hamcrest import assert_that, empty, not_

from framework.factory.user.user_process import UserProcess
from framework.models.models_user import User, UserRequest


@allure.feature("Негативное тестирование менеджмента пользователей")
class TestUserNegative:
    @pytest.mark.parametrize(
        "age, expected_status",
        [
            pytest.param(17, 400, id="17"),
            pytest.param(18, 201, id="18"),
            pytest.param(100, 201, id="100"),
            pytest.param(101, 400, id="101"),
        ],
    )
    @allure.title("Создание пользователя с разным возрастом")
    def test_create_user_age(self, valid_user: UserRequest, age: int, expected_status: int):
        valid_user.age = age
        UserProcess.create_user(user=valid_user, expected_status=expected_status, serialize=False)

    @pytest.mark.parametrize(
        "name",
        [
            pytest.param("", id="empty_name"),
        ],
    )
    @allure.title("Создание пользователя с пустым именем")
    def test_create_user_empty_name(self, valid_user: UserRequest, name: str):
        valid_user.name = name
        UserProcess.create_user(user=valid_user, expected_status=400, serialize=False)

    @pytest.mark.parametrize(
        "email",
        [
            pytest.param("meow", id="without_domain"),
            pytest.param("example.org", id="without_dog"),
            pytest.param("@example.org", id="without_login"),
            pytest.param("", id="empty_email"),
        ],
    )
    @allure.title("Создание пользователя с некорректным email")
    def test_create_user_invalid_email(self, valid_user: UserRequest, email: str):
        valid_user.email = email
        UserProcess.create_user(user=valid_user, expected_status=400, serialize=False)

    @pytest.mark.parametrize(
        "phone",
        [
            pytest.param("", id="empty_phone"),
            pytest.param("123", id="short_phone"),
            pytest.param("asdf", id="letter_phone"),
        ],
    )
    @allure.title("Создание пользователя с некорректным телефоном")
    def test_create_user_invalid_phone(self, valid_user: UserRequest, phone: str):
        valid_user.phone = phone
        UserProcess.create_user(user=valid_user, expected_status=400, serialize=False)

    @allure.title("Создание пользователя с существующим телефоном")
    def test_create_user_dublicate_phone(self, valid_user: UserRequest, created_valid_user: User):
        valid_user.phone = created_valid_user.phone
        UserProcess.create_user(user=valid_user, expected_status=400, serialize=False)

    @allure.title("Получение пользователя по несуществующему ID")
    def test_user_not_found(self):
        UserProcess.get_user_by_id(user_id=9999999, expected_status=404, serialize=False)

    @pytest.mark.parametrize(
        "user_id", [pytest.param(-1, id="negative_one"), pytest.param(-100, id="negative_one_hundred")]
    )
    @allure.title("Получение пользователя с отрицательным ID")
    def test_get_user_negative_id(self, user_id: int):
        UserProcess.get_user_by_id(user_id=user_id, expected_status=404, serialize=False)

    @allure.title("Обновление пользователя пустым именем")
    def test_update_user_empty_name(self, created_valid_user: User):
        created_valid_user.name = ""
        UserProcess.update_user(
            user_id=created_valid_user.id, user=created_valid_user, expected_status=400, serialize=False
        )

    @pytest.mark.parametrize(
        "email",
        [
            pytest.param("meow", id="invalid_text"),
            pytest.param("example.org", id="without_dog"),
            pytest.param("", id="empty_email"),
        ],
    )
    @allure.title("Обновление пользователя некорректным email")
    def test_update_user_invalid_email(self, created_valid_user: User, email: str):
        created_valid_user.email = email
        UserProcess.update_user(
            user_id=created_valid_user.id, user=created_valid_user, expected_status=400, serialize=False
        )

    @allure.title("Обновление несуществующего пользователя")
    def test_update_non_existent_user(self, valid_user: UserRequest):
        UserProcess.update_user(user_id=9999999, user=valid_user, expected_status=404, serialize=False)

    @allure.title("Удаление несуществующего пользователя")
    def test_delete_non_existent_user(self):
        UserProcess.delete_user(user_id=9999999, expected_status=404)

    @allure.title("получение списка пользователей")
    def test_get_all_users(self):
        users = UserProcess.get_all_users()

        assert_that(users, not_(empty()), "Список пользователей пустой")
