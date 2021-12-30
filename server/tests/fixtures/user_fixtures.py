import pytest
from db.user import User


@pytest.fixture
def user_1():
    return {"email": "user_1@email.com"}


@pytest.fixture
def user_2():
    return {"email": "user_2@email.com"}


@pytest.fixture
def seed_users(fixture_db, user_1, user_2):
    """Seeds the db with 2 users.

    Returns:
        (list[int]): list of their ids.
    """

    user_1_db = User(**user_1)
    user_2_db = User(**user_2)
    fixture_db.add(user_1_db)
    fixture_db.add(user_2_db)
    fixture_db.commit()

    return [user_1_db.id, user_2_db.id]