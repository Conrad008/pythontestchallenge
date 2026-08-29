import pytest

from .factories import UserFactory


@pytest.mark.django_db
def test_user_factory_creates_user():
    user = UserFactory()

    assert user.username is not None
    assert user.email is not None
    assert user.check_password("Password123!") is True