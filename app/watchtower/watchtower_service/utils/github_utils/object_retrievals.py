from github import GithubIntegration, Installation
import watchtower_service.models as models
from tasks.data_collection_tasks import get_all_organization_repositories
from tasks.data_collection_tasks import get_all_organization_repositories

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
            get_all_organization_repositories.apply_async(
                args=[installation.id, installation.target_id]
            )
        # get_all_installation_repositories(installation.id, git_integration, installation_object)
