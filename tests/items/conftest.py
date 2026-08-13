import random

import pytest
from faker.proxy import Faker

from framework.factory.items.item_process import ItemProcess
from framework.models.models_items import Item, ItemRequest

faker = Faker("ru_RU")


@pytest.fixture
def valid_item() -> ItemRequest:
    return ItemRequest(name=faker.word(), description=faker.text(max_nb_chars=50), price=str(random.randint(100, 10000)))


@pytest.fixture
def created_valid_item(valid_item: ItemRequest) -> Item:
    created_item = ItemProcess.create_item(item=valid_item)
    return ItemProcess.get_item_by_id(item_id=created_item.id)

@pytest.fixture
def created_items(valid_item: ItemRequest) -> tuple[Item, Item, Item]:
    item1_id = ItemProcess.create_item(item=valid_item).id
    item1 = ItemProcess.get_item_by_id(item_id=item1_id)

    same_name = valid_item.model_copy()
    same_name.description = faker.text(max_nb_chars=50)
    same_name.price = random.randint(100, 10_000)

    item2_id = ItemProcess.create_item(item=same_name).id
    item2 = ItemProcess.get_item_by_id(item_id=item2_id)

    other_name = valid_item.model_copy()
    other_name.name = "Другой самокат"

    item3_id = ItemProcess.create_item(item=other_name).id
    item3 = ItemProcess.get_item_by_id(item_id=item3_id)

    return item1, item2, item3
