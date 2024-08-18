import logging

import pytest
from sqlalchemy.orm import Session

from app.external.postgres.models import User
from app.external.postgres.storage import DBStorage

logger = logging.getLogger(__name__)

test_user = {
    'username': 'george',
    'hashed_password': 'dsfawr23',
}


@pytest.fixture
def storage() -> DBStorage:
    """Создает объект DBStorage."""
    return DBStorage()


@pytest.fixture
def storage_with_user(storage: DBStorage):
    """Создает пользователя в storage."""
    with Session(storage.pool) as session:
        user = User(**test_user)
        session.add(user)
        session.commit()
    try:
        yield storage
    except Exception:
        logger.debug('exception in tests with storage_with_user')
    finally:
        with Session(storage.pool) as after_session:
            after_session.delete(user)
            after_session.commit()
