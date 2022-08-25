from watchtower_service.utils.initializer_utils import (
    check_and_create_initial_superuser,
    check_and_create_oauth_application
)


def run():
    check_and_create_initial_superuser()
    check_and_create_oauth_application()
    # create_initial_installation()
