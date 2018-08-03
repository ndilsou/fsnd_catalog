import pytest
import os
import tempfile

import catalog
import catalog.models as models

from test.setup_test_db import make_record


@pytest.fixture(scope="session")
def app():
    return catalog.app


@pytest.fixture(scope="module")
def db_session(app):
    from catalog.database import Session

    try:

        db_fd, test_db = tempfile.mkstemp(suffix=".db")
        app.config["DATABASE"] = "sqlite:///{}".format(test_db)

        catalog.database.init_db(catalog.app)
        yield Session

    finally:
        os.close(db_fd)
        os.unlink(test_db)


@pytest.fixture
def client(db_session):
    client = catalog.app.test_client()
    return client


def test_insert_user(db_session, make_record):
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
    user = make_record(models.User, username="Admin1", email="admin1@admin.com")
    make_record(models.Category, name="Horse Riding", owner=user)

    category = db_session.query(models.Category).filter_by(name="Horse Riding").first()
    assert category is not None
    assert category.name == "Horse Riding"
    assert category.owner.username == "Admin1"
