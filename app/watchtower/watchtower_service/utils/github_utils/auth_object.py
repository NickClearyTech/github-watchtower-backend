import settings
import os
from github import GithubIntegration, Github


def get_private_key():
    """
    Gives the github private key as a string
    :return: String of private key
    """
    with open(os.path.normpath(settings.GITHUB_PRIVATE_KEY_PATH), "r") as cert_file:
        return cert_file.read()


def get_github_integration() -> GithubIntegration:
    """
    Easy wrapper to grab a github integration object
    :return: A github integration object
    """
    return GithubIntegration(settings.GITHUB_APP_ID, get_private_key())


def get_github_api_object(
    installation_id: int, integration: GithubIntegration = None
) -> Github:
    """
    Returns a Github API object for a specified installation ID
    :param installation_id: Required installation ID
    :param integration: Optionally provide an integration to the function. If not provided, one will be created at runtime
    :return: Github object for specified installation
    """
    if integration is None:
        integration = get_github_integration()
    token: str = integration.get_access_token(installation_id).token
    return Github(token)
