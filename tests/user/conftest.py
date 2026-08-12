import random
from datetime import UTC, datetime

import pytest
from faker.proxy import Faker

from framework.factory.user.user_process import UserProcess
from framework.models.user import Gender, User, UserRequest

faker = Faker("ru_RU")


@pytest.fixture
def valid_user() -> UserRequest:
    age = random.randint(18, 100)
    return UserRequest(
        name=faker.name(),
        email=faker.email(safe=True),
        age=age,
        interests=faker.words(nb=5),
        gender=random.choice(list(Gender)),
        phone=faker.numerify("+7##########"),
        birth_date=datetime.combine(
            faker.date_of_birth(minimum_age=age, maximum_age=age),
            datetime.min.time(),
            tzinfo=UTC,
        ),
    )


@pytest.fixture
def created_valid_user(valid_user: UserRequest) -> User:
    created_user = UserProcess.create_user(user=valid_user)
    return UserProcess.get_user_by_id(user_id=created_user.id)


@pytest.fixture
def created_users(valid_user: UserRequest) -> tuple[User, User, User]:
    user1_id = UserProcess.create_user(user=valid_user).id
    user1 = UserProcess.get_user_by_id(user_id=user1_id)

    same_name = valid_user.model_copy()
    same_name.email = faker.email(safe=True)
    same_name.phone = faker.numerify("+7##########")

    user2_id = UserProcess.create_user(user=same_name).id
    user2 = UserProcess.get_user_by_id(user_id=user2_id)

    other_name = valid_user.model_copy()
    other_name.name = "Олег"
    other_name.email = faker.email(safe=True)
    other_name.phone = faker.numerify("+7##########")

    user3_id = UserProcess.create_user(user=other_name).id
    user3 = UserProcess.get_user_by_id(user_id=user3_id)

    return user1, user2, user3
