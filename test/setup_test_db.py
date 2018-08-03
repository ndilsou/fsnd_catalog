import pytest


@pytest.fixture
def make_record(db_session):
    created_records = []

    def _make_record(entity, **kwargs):
        record = entity(**kwargs)
        db_session.add(record)
        db_session.commit()
        return record

    yield _make_record

    for record in created_records:
        record.delete()
    db_session.commit()
