import pytest
import catalog.models as models

from tests.fixtures import *


def test_insert_user(db_session, make_record):
    print("INSERT USER")
    make_record(models.User, username="Admin", email="admin@admin.com")
    user = db_session.query(models.User).filter_by(username="Admin").first()
    assert user is not None


def test_insert_category(db_session, make_record):
    user = make_record(models.User, username="Admin", email="admin@admin.com")
    make_record(models.Category, name="Horse Riding", owner=user, description="Horse Riding Category.")

    category = db_session.query(models.Category).filter_by(name="Horse Riding").first()
    assert category is not None
    assert category.name == "Horse Riding"
    assert category.owner.username == "Admin"


def test_insert_item(db_session, make_record):
    user = make_record(models.User, username="Admin", email="admin@admin.com")
    category = make_record(models.Category, name="Horse Riding", owner=user, description="Horse Riding Category.")
    make_record(models.Item, name="Stirrup", category=category, description="Gets you on a horse.")

    item = db_session.query(models.Item).filter_by(name="Stirrup").first()
    assert item is not None
    assert item.name == "Stirrup"
    assert item.category.name == "Horse Riding"


def test_serialize_entities(db_session, make_record):
    user = make_record(models.User, username="Admin", email="admin@admin.com")
    category = make_record(models.Category, name="Horse Riding", owner=user, description="Horse Riding Category.")
    item = make_record(models.Item, name="Stirrup", category=category, description="Gets you on a horse.")

    assert {"username": "Admin"} == user.to_dict()
    assert {"name": "Horse Riding", "description": "Horse Riding Category."} == category.to_dict()
    assert {"name": "Stirrup", "category": "Horse Riding", "description": "Gets you on a horse."} == item.to_dict()


def test_seeded_session(seeded_session):
    users = seeded_session.query(models.User).all()
    assert len(users) == 2
    categories = seeded_session.query(models.Category).all()
    assert len(categories) == 2
    items = seeded_session.query(models.Item).all()
    assert len(items) == 5


def test_category_is_back_populated(db_session, make_record):
    user = make_record(models.User, username="Admin1", email="admin1@admin.com")
    category = make_record(models.Category, name="Horse Riding", owner=user, description="Horse Riding Category.")
    item = make_record(models.Item, name="Stirrup", category=category, description="Gets you on a horse.")

    assert category.items[0] == item

