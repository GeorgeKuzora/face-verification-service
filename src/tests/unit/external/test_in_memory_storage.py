import pytest

from app.core.models import User
from tests.unit.conftest import invalid_user, test_user, user_list2objects


class TestCreateUser:
    """Тестируем метод create_user."""

    @pytest.mark.parametrize(
        'user, expected, expected_user_id', (
            pytest.param(test_user, test_user, 0, id='get user in response'),
        ),
    )
    def test_create_user_returns_indexed_user(
        self, user: User, expected: User, expected_user_id, storage,
    ):
        """Тестирует что возвращается пользователь с верным id."""
        response_user: User = storage.create_user(user)

        assert response_user.username == expected.username
        assert response_user.user_id == expected_user_id

    @pytest.mark.parametrize(
        'user_list, expected_last_user_id', (
            pytest.param(user_list2objects, 1, id='index increases'),
        ),
    )
    def test_create_user_db_index_increases(
        self, user_list: list[User], expected_last_user_id, storage,
    ):
        """Тестирует что индекс при создании пользователя растет."""
        for user in user_list:
            response_user: User = storage.create_user(user)

        users_db_len = len(storage.users)

        assert response_user.user_id == expected_last_user_id
        # index starts at 0
        assert users_db_len == expected_last_user_id + 1


class TestGetUser:
    """Тестирует метод get_user."""

    @pytest.mark.parametrize(
        'user, repository_state_factory, expected_user', (
            pytest.param(
                user_list2objects[0],
                'single_user_in_repo_facrory',
                user_list2objects[0],
                id='first user in repo',
            ),
            pytest.param(
                user_list2objects[1],
                'two_users_in_repo_facrory',
                user_list2objects[1],
                id='second user in repo',
            ),
        ),
    )
    def test_get_user(
        self, user: User, repository_state_factory, expected_user, request,
    ):
        """Тетстирует получение пользователя."""
        repository, users_in_db = request.getfixturevalue(
            repository_state_factory,
        )
        expected_user_id = users_in_db - 1

        respose_user: User | None = repository.get_user(user)

        if respose_user is None:
            raise AssertionError
        assert respose_user.username == expected_user.username
        assert respose_user.user_id == expected_user_id

    @pytest.mark.parametrize(
        'invalid_user, repository_state_factory, expected', (
            pytest.param(
                invalid_user,
                'two_users_in_repo_facrory',
                None,
                id='second user in repo',
            ),
        ),
    )
    def test_get_user_returns_none(
        self, invalid_user: User, repository_state_factory, expected, request,
    ):
        """Тестирует что возвращен None если пользователь не найден."""
        repository, _ = request.getfixturevalue(
            repository_state_factory,
        )

        respose_user: User | None = repository.get_user(invalid_user)

        assert respose_user == expected


class TestUpdateUser:
    """Тестирует update_user."""

    @pytest.mark.parametrize(
        'user, repository_state_factory, expected_user, expected_id', (
            pytest.param(
                user_list2objects[0],
                'single_user_in_repo_facrory',
                user_list2objects[0],
                0,
                id='user found and updated',
            ),
            pytest.param(
                user_list2objects[1],
                'single_user_in_repo_facrory',
                user_list2objects[1],
                1,
                id='user not found and created',
            ),
        ),
    )
    def test_update_user(  # noqa: WPS211 neede these arguments
        self,
        user: User,
        repository_state_factory,
        expected_user,
        expected_id,
        request,
    ):
        """Тетстирует обновление пользователя."""
        repository, _ = request.getfixturevalue(
            repository_state_factory,
        )
        representation = [{'233': 233}]

        response_user: User = repository.update_user(
            representation, user.username,
        )

        if response_user is None:
            raise AssertionError
        assert response_user.user_id == expected_id
        assert response_user.is_verified is True
