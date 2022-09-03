from watchtower_service.utils.initializer_utils import (
    check_and_create_initial_superuser,
    check_and_create_oauth_application,
    run_startup_imports,
)


def run():
    check_and_create_initial_superuser()
    check_and_create_oauth_application()
    run_startup_imports()
