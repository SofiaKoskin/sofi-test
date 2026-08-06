
import allure
import pytest
from hamcrest import assert_that, has_entries, equal_to, not_none, contains_inanyorder, not_,is_in

from framework.api.handler.http.user.user import create, delete_user, update_user
from framework.factory.user.user_process import UserProcess
from framework.models.user import UserCreate, Gender, User, UserUpdate
from tests.user.conftest import created_valid_user, valid_user




