import random
from datetime import UTC, datetime

from framework.models.user import User


import pytest
from faker.proxy import Faker

from framework.factory.user.user_process import UserProcess
from framework.models.user import Gender, UserCreate

faker = Faker("ru_RU")


@pytest.fixture
def valid_user() -> UserCreate:
    age = random.randint(18, 100)
    return UserCreate(
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
def created_valid_user(valid_user: UserCreate) -> User:
    return UserProcess.create_user(user=valid_user)


@pytest.fixture
def created_users(valid_user: UserCreate) -> tuple[User, User, User]:
    user1 = UserProcess.create_user(user=valid_user)

    same_name = valid_user.model_copy()
    same_name.email = faker.email(safe=True)
    same_name.phone = faker.numerify("+7##########")
    user2 = UserProcess.create_user(user=same_name)

    other_name = valid_user.model_copy()
    other_name.name = "Олег"
    other_name.email = faker.email(safe=True)
    other_name.phone = faker.numerify("+7##########")
    user3 = UserProcess.create_user(user=other_name)

    return  user1, user2, user3
