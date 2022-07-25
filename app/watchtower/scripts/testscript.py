import os
from github import GithubIntegration, Github, GithubApp
from settings import GITHUB_OAUTH_CLIENT_ID, GITHUB_OAUTH_CLIENT_SECRET

app_id = 220599


def run():
    with open(os.path.normpath("/key.pem"), "r") as cert_file:
        app_key = cert_file.read()
    git_integration = GithubIntegration(
        app_id,
        app_key,
    )
    # print(git_integration)
