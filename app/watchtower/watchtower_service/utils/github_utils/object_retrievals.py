from github import GithubIntegration, Installation, Github, Organization, Repository
from watchtower_service.utils.github_utils.auth_object import get_github_api_object
import watchtower_service.models as models

from logging import getLogger

logger = getLogger(__name__)


def get_all_integration_installations(git_integration: GithubIntegration):
    installation: Installation
    for installation in git_integration.get_installations():
        installation_object: models.Installation
        installation_object, created = models.Installation.objects.get_or_create(
            installation_id=installation.id,
            app=models.App.objects.get(app_id=installation.app_id),
            target_id=installation.target_id,
            target_type="org" if installation.target_type == "Organization" else "repo",
        )

        logger.info(
            f"{'Created' if created else 'Found'} installation with ID {installation_object.installation_id}"
        )
        if installation.target_type == "Organization":
            get_all_organization_repositories(
                installation.id,
                installation.target_id,
                integration_object=git_integration,
            )
        # get_all_installation_repositories(installation.id, git_integration, installation_object)


def get_all_organization_repositories(
    installation_id: int,
    organization_id: int,
    integration_object: GithubIntegration = None,
):
    api_object: Github = get_github_api_object(
        installation_id, integration=integration_object
    )
    organization_object: models.Organization = models.Organization.objects.filter(
        organization_id=organization_id
    ).first()
    if organization_object is None:
        logger.error(f"Error: Unable to find organization with ID {organization_id}")
        return
    github_organization: Organization = api_object.get_organization(
        login=organization_object.organization_login
    )
    for repo in github_organization.get_repos():
        print(repo)
