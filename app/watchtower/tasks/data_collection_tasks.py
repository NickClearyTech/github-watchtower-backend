from watchtower_service.celery import app as celery_app
from github import GithubIntegration, Github, Organization, Repository
from watchtower_service.utils.github_utils.auth_object import get_github_api_object
import watchtower_service.models as models

from logging import getLogger
from django.utils.timezone import make_aware

logger = getLogger(__name__)


@celery_app.task(bind=True)
def get_all_organization_repositories(
    self,
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
        created: bool
        repo_object: models.Repository
        repo_object, created = models.Repository.objects.get_or_create(
            repository_id=repo.id,
            installation=models.Installation.objects.get(
                installation_id=installation_id
            ),
        )
        repo_object.name = repo.name
        repo_object.archived = repo.archived
        repo_object.description = repo.description
        repo_object.is_fork = repo.fork
        repo_object.has_downloads = repo.has_downloads
        repo_object.has_issues = repo.has_issues
        repo_object.has_pages = repo.has_pages
        repo_object.has_wiki = repo.has_wiki
        repo_object.language = repo.language
        repo_object.master_branch = repo.master_branch
        repo_object.is_private = repo.private
        repo_object.last_pushed_at = make_aware(repo.pushed_at)
        repo_object.size = repo.size
        repo_object.subscribers_count = repo.subscribers_count
        repo_object.last_updated = make_aware(repo.updated_at)
        repo_object.owner_id = repo.owner.id
        repo_object.owner_type = "org" if repo.owner.type == "Organization" else "user"

        repo_object.save()
        logger.info(
            f"Retrieved and updated repository information for repository with ID {repo_object.repository_id}"
        )
