import pytest
from sqlalchemy.orm import exc as sqla_exc
import catalog.models as models

from tests.fixtures import *


def test_submit_item_add_creates_new_record(client, db_session, make_record):
    make_record(models.User, username='John Doe', email='jon.jon.doe@testmail.com')
    make_record(models.Category, name='Football', description='The real one from Europe.', owner_id=1)

    res = client.post("/catalog/items/add",
                      data=dict(name='TestProduct', category='Football', description='TestyTestusTester'),
                      follow_redirects=True)
    item = db_session.query(models.Item).filter_by(name="TestProduct").one_or_none()
    assert item
    assert item.name == "TestProduct"


def test_submit_item_delete_record(client, db_session, make_record):
    make_record(models.User, username='John Doe', email='jon.jon.doe@testmail.com')
    make_record(models.Category, name='Boxing', description='If you''re up for a good fight.', owner_id=1)
    make_record(models.Item, name='Gloves', description='We''re fighters here, not brute.', category_id=1)

    res = client.post("/catalog/Gloves/delete", follow_redirects=True)
    with pytest.raises(sqla_exc.NoResultFound):
        db_session.query(models.Item).filter_by(name="Gloves").one()


def test_submit_item_edit_record(client, seeded_session, make_record):
    expected_description = "NEW TEST DESCRIPTION"
    # make_record(models.User, username='John Doe', email='jon.jon.doe@testmail.com')
    # make_record(models.Category, name='Boxing', description='If you''re up for a good fight.', owner_id=1)
    # make_record(models.Item, name='Gloves', description='We''re fighters here, not brute.', category_id=1)

    res = client.post("/catalog/Gloves/edit",
                      data=dict(name="Gloves", description=expected_description, category="Boxing"),
                      follow_redirects=True)

    item = seeded_session.query(models.Item).filter_by(name="Gloves").one_or_none()
    assert item
    assert item.description == expected_description
