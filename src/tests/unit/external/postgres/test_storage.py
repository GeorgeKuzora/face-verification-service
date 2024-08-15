import pytest

from app.core.models import User
from app.external.postgres.storage import DBStorage
from tests.unit.external.postgres.conftest import test_user

stub_vector = [{'embed': 123}]
is_verified = True


class TestUpdateUser:
    """Тестирует метод update_user."""

    @pytest.mark.database
    @pytest.mark.parametrize(
        'storage_fixture, username, expected', (
            pytest.param(
                'storage_with_user',
                test_user['username'],
                test_user,
                id='storage with user',
            ),
            pytest.param(
                'storage',
                test_user['username'],
                None,
                id='storage without user',
            ),
        ),
    )
    def test_update_user(
        self, storage_fixture, username, expected: dict, request,
    ):
        """Тестирует что метод возвращает правильный объект."""
        storage: DBStorage = request.getfixturevalue(storage_fixture)

        user: User | None = storage.update_user(
            vector=stub_vector, username=username,
        )

        if user is None:
            assert user is expected
        else:
            assert user.username == expected['username']
            assert user.is_verified is is_verified
