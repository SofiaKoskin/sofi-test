import random
from framework.models.item import Item


import pytest
from faker.proxy import Faker

from framework.factory.items.item_process import ItemProcess
from framework.models.item import Item, ItemCreate

faker = Faker("ru_RU")



@pytest.fixture
def valid_item() -> ItemCreate:
    return ItemCreate(
        name = faker.word(),
        description = faker.text(max_nb_chars=50),
        price = str(random.randint(100,10000))
    )


@pytest.fixture
def created_valid_item(valid_item: ItemCreate) -> Item:
    return ItemProcess.create_item(item=valid_item)
