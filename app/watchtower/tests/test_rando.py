def test_first():
    assert 1 == 1


def func(x):
    return x + 1


def test_answer():
    assert func(3) == 4
    assert func(3) == 4


from watchtower_service.utils.github_utils.validations import (
    check_valid_oauth_credentials,
)


def test_test_oauth():
    assert check_valid_oauth_credentials() == False
