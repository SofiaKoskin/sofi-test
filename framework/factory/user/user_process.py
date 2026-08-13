import allure

from framework.api.handler.http.user import client_user as user_handler
from framework.models.models_user import User, UserCreateResponse, UserRequest


class UserProcess:
    @staticmethod
    def create_user(*, user: UserRequest | dict, serialize: bool = True, expected_status: int = 201) -> UserCreateResponse | dict:
        with allure.step(f"Создание пользователя {user=}"):
            if isinstance(user, UserRequest):
                response = user_handler.create(data=user.model_dump(mode="json"), expected_status=expected_status)
            elif isinstance(user, dict):
                response = user_handler.create(data=user, expected_status=expected_status)
            else:
                raise ValueError("Непонятный тип у пользователя")

            if serialize:
                return UserCreateResponse.model_validate(response)
            else:
                return response

    @staticmethod
    def get_user_by_id(*, user_id: int, serialize: bool = True, expected_status: int = 200) -> User | dict:
        with allure.step(f"Получение пользователя по id: {user_id=}"):
            response = user_handler.get_user_by_id(user_id=user_id, expected_status=expected_status)

            if serialize:
                return User.model_validate(response)
            else:
                return response

    @staticmethod
    def get_all_users(*, serialize: bool = True, expected_status: int = 200) -> list[User] | list[dict]:
        with allure.step("Получение списка всех пользователей"):
            response = user_handler.get_all_users(expected_status=expected_status)

            if serialize:
                return [User.model_validate(user) for user in response]
            else:
                return response

    @staticmethod
    def delete_user(*, user_id: int, expected_status: int = 204) -> dict:
        with allure.step(f"Удаление пользователя по id:{user_id}"):
            return user_handler.delete_user(user_id=user_id, expected_status=expected_status)

    @staticmethod
    def update_user(
        *, user_id: int, user: UserRequest, expected_status: int = 200
    ) -> None:
        with allure.step(f"Обновление пользователяid={user_id}"):
            user_handler.update_user(
                user_id=user_id, data=user.model_dump(mode="json"), expected_status=expected_status
            )

    @staticmethod
    def get_users_by_name(*, name: str, serialize: bool = True, expected_status: int = 200) -> list[User] | list[dict]:
        with allure.step(f"Получение пользователей по имени: {name}"):
            response = user_handler.get_user_by_name(name=name, expected_status=expected_status)

            if serialize:
                return [User.model_validate(user) for user in response]
            else:
                return response
