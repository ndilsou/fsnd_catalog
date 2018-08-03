import pytest
import os
import tempfile

import catalog
import catalog.models as models

# from test.setup_test_db import make_record


@pytest.fixture(scope="module")
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
def db_session(database):
    from catalog.database import Session
    return Session


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
def client(db_session):
    client = catalog.app.test_client()
    return client


def test_insert_user(db_session, make_record):
    print("INSERT USER")
    make_record(models.User, username="Admin", email="admin@admin.com")
    user = db_session.query(models.User).filter_by(username="Admin").first()
    assert user is not None


def test_empty_db(client):
    rv = client.get("/")
    page = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<header><h1>Welcome to the catalog</h1></header>
</body>
</html>"""
    assert page == rv.data.decode("utf-8")


def test_insert_category(db_session, make_record):
    print("INSERT CATEGORY")
    user = make_record(models.User, username="Admin", email="admin@admin.com")
    make_record(models.Category, name="Horse Riding", owner=user, description="Horse Riding Category.")

    category = db_session.query(models.Category).filter_by(name="Horse Riding").first()
    assert category is not None
    assert category.name == "Horse Riding"
    assert category.owner.username == "Admin"
