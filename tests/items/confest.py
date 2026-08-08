import random

import pytest
from faker.proxy import Faker

from framework.factory.items.item_process import ItemProcess
from framework.models.item import Item, ItemCreate

faker = Faker("ru_RU")


@pytest.fixture
def valid_item() -> ItemCreate:
    return ItemCreate(name=faker.word(), description=faker.text(max_nb_chars=50), price=str(random.randint(100, 10000)))


@pytest.fixture
def created_valid_item(valid_item: ItemCreate) -> Item:
    return ItemProcess.create_item(item=valid_item)


@pytest.fixture
def created_items(valid_item: ItemCreate) -> tuple[Item, Item, Item]:
    item1 = ItemProcess.create_item(item=valid_item)

    same_name = valid_item.model_copy()
    same_name.description = faker.text(max_nb_chars=50)
    same_name.price = str(random.randint(100, 10000))
    item2 = ItemProcess.create_item(item=same_name)

    other_name = valid_item.model_copy()
    other_name.name = "Другой самокат"
    item3 = ItemProcess.create_item(item=other_name)

    return item1, item2, item3
