from github import GithubIntegration, Installation, NamedUser
import watchtower_service.models as models
from tasks.data_collection_tasks import (
    get_all_organization_repositories,
    get_organization_users_and_teams,
    get_organization_repo_permissions,
)

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
            task_one = get_all_organization_repositories.apply_async(
                args=[installation.id, installation.target_id]
            )
            task_two = get_organization_users_and_teams.apply_async(
                args=[installation.id, installation.target_id]
            )
            get_organization_repo_permissions.apply_async(
                args=[
                    installation.id,
                    installation.target_id,
                    [task_one.id, task_two.id],
                ]
            )
