import pytest
import os
import tempfile

import catalog
from catalog import models


@pytest.fixture(scope="session")
def app():
    return catalog.app


@pytest.fixture(scope="module")
def database(app):
    try:

        db_fd, test_db = tempfile.mkstemp(suffix=".db")
        app.config["DATABASE"] = "sqlite:///{}".format(test_db)

        catalog.database.init_db(catalog.app)
        yield catalog.database

    finally:
        os.close(db_fd)
        os.unlink(test_db)


@pytest.fixture(scope="function")
def seeded_session(database):
    from catalog.database import Session
    try:
        session = Session()
        session.add(models.User(username='Admin', email='test@testmail.com'))
        session.add(models.User(username='John Doe', email='jon.jon.doe@testmail.com'))

        session.add(models.Category(name='Football', description='The real one from Europe.', owner_id=2))

        session.add(models.Item(name='Football ball', description='Rather hard to play without one init?', category_id=1))
        session.add(models.Item(name='Arsenal Jersey', description='You still there Arsene?', category_id=1))
        session.add(models.Item(name='Drama Classes', description='Falling on the grass is an art. It takes practice to '
                                                                  'master it.', category_id=1))

        session.add(models.Category(name='Boxing', description='If you''re up for a good fight.', owner_id=2))

        session.add(models.Item(name='Gloves', description='We''re fighters here, not brute.', category_id=2))
        session.add(models.Item(name='Jumping Rope', description='Just like Rocky.', category_id=2))
        session.commit()
        yield session

    except:
        session.rollback()
        raise
    finally:
        session.close()


@pytest.fixture(scope="function")
def db_session(database):
    from catalog.database import Session
    try:
        session = Session()
        yield session

    finally:
        session.rollback()
        session.close()


@pytest.fixture(scope="function")
def make_record(db_session):
    created_records = []

    def _make_record(entity, **kwargs):
        record = entity(**kwargs)
        db_session.add(record)
        created_records.append(record)
        db_session.commit()
        return record

    yield _make_record
    for record in created_records:
        record.query.delete()
    db_session.commit()


@pytest.fixture
def client(app):
    client = app.test_client()
    return client

