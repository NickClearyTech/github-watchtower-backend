import os

import github
from github import GithubIntegration, Github, GithubApp
from settings import GITHUB_OAUTH_CLIENT_ID, GITHUB_OAUTH_CLIENT_SECRET

app_id = 220599


def run():
    with open(
        os.path.normpath("/Users/nicleary/.certs/github/bot_key.pem"), "r"
    ) as cert_file:
        app_key = cert_file.read()
    git_integration = GithubIntegration(
        app_id,
        app_key,
    )
    print(git_integration)
    print(f"JWT: {git_integration.create_jwt()}")
    for installation in git_integration.get_installations():
        print(installation.id)
    print("Sluggi!!!")
    print(git_integration.get_app_slug())
    token = git_integration.get_access_token(27464832).token
    org = github.Github(token).get_organization("NickClearyTech")
    print(github.Github(token).get_app(slug=git_integration.get_app_slug()).name)
    for repo in org.get_repos():
        print(repo.full_name)

    app = github.Github(token).get_app(git_integration.get_app_slug())
    print(app)
