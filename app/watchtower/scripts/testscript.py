import os

import github
from github import (
    GithubIntegration,
    Github,
    GithubApp,
    Organization,
    NamedUser,
    Repository,
)
import watchtower_service.models as models
from watchtower_service.utils.github_utils.auth_object import get_github_integration

app_id = 220599


def run():
    git_integration = get_github_integration()

    installation_id: int = git_integration.get_installations()[0].id
    token: str = git_integration.get_access_token(installation_id).token

    github_object: Github = github.Github(token)

    app_slug: str = git_integration.get_app_slug()
    github_app_object: GithubApp = github_object.get_app(slug=app_slug)

    app_owner_object = None
    _: bool = None

    if github_app_object.owner.type == "Organization":
        github_app_owner: Organization = github_object.get_organization(
            login=github_app_object.owner.login
        )
        app_owner_object: models.Organization
        app_owner_object, _ = models.Organization.objects.get_or_create(
            organization_id=github_app_owner.id,
            organization_login=github_app_owner.login,
        )

        app_owner_object.organization_name = github_app_owner.name
        app_owner_object.organization_type = github_app_owner.type
        app_owner_object.description = github_app_owner.description
        app_owner_object.company = github_app_owner.company
        app_owner_object.email = github_app_owner.email
        app_owner_object.avatar_url = github_app_owner.avatar_url
        app_owner_object.default_repository_permission = (
            github_app_owner.default_repository_permission
        )
        app_owner_object.disk_usage = github_app_owner.disk_usage
        app_owner_object.save()

    app_object: models.App
    app_object, _ = models.App.objects.get_or_create(
        app_id=github_app_object.id,
        owner_id=github_app_object.owner.id,
        owner_type="org" if github_app_object.owner.type == "Organization" else "user",
    )

    app_object.name = github_app_object.name
    app_object.slug = github_app_object.slug
    app_object.installation_count = github_app_object.installation_count

    for installation in git_integration.get_installations():
        installation_object: models.Installation
        installation_object, _ = models.Installation.objects.get_or_create(
            installation_id=installation.id,
            app=models.App.objects.get(app_id=installation.app_id),
            target_id=installation.target_id,
            target_type="org" if installation.target_type == "Organization" else "repo",
        )

    # repository: Repository = (
    #     github_object.get_repo(
    #         full_name_or_id="NickClearyTech/github-watchtower-backend"
    #     )
    #     .get_contents("Dockerfile")
    #     .decoded_content
    # )
    # print(repository)
