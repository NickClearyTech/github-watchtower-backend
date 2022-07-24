from settings import *


def check_valid_oauth_credentials() -> bool:
    """
    Check if OAuth credentials are properly setup and are not None
    :return: True if both secrets are not None, False one or both are None
    """
    if GITHUB_OAUTH_CLIENT_ID is None or GITHUB_OAUTH_CLIENT_SECRET is None:
        return False
    return True
