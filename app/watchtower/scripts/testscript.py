import os

import github
from github import GithubIntegration, Github, GithubApp
from settings import GITHUB_OAUTH_CLIENT_ID, GITHUB_OAUTH_CLIENT_SECRET

app_id = 220599


def run():
    with open(
        os.path.normpath("/key.pem"), "r"
    ) as cert_file:
        app_key = cert_file.read()
    git_integration = GithubIntegration(
        app_id,
        app_key,
    )
    print(git_integration)
    token = git_integration.get_access_token(27464832).token
    print(token)
    org = github.Github(token).get_organization("NickClearyTech")
    print(
        github.Github(token).get_app(slug=str("test-github-app-nick-cleary-tech")).name
    )
    for repo in org.get_repos():
        print(repo.full_name)
