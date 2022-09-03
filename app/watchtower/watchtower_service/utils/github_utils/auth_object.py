import settings
import os
from github import GithubIntegration


def get_private_key():
    with open(os.path.normpath(settings.GITHUB_PRIVATE_KEY_PATH), "r") as cert_file:
        return cert_file.read()


def get_github_integration() -> GithubIntegration:
    return GithubIntegration(settings.GITHUB_APP_ID, get_private_key())
