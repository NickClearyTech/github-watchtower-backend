from typing import List

from watchtower_service.celery import app as celery_app
from github import GithubIntegration, Github, Organization, Repository
from watchtower_service.utils.github_utils.auth_object import get_github_api_object
from watchtower_service.utils.data_utils import github_user_to_db_object
from watchtower_service.utils.celery_utils import check_all_tasks_complete
import watchtower_service.models as models

from logging import getLogger
from django.utils.timezone import make_aware
import time

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
        repo_object, created = models.Repository.objects.update_or_create(
            repository_id=repo.id,
            installation=models.Installation.objects.get(
                installation_id=installation_id
            ),
            defaults={
                "name": repo.name,
                "archived": repo.archived,
                "description": repo.description,
                "is_fork": repo.fork,
                "has_downloads": repo.has_downloads,
                "has_issues": repo.has_issues,
                "has_pages": repo.has_pages,
                "has_wiki": repo.has_wiki,
                "language": repo.language,
                "master_branch": repo.master_branch,
                "is_private": repo.private,
                "last_pushed_at": make_aware(repo.pushed_at),
                "size": repo.size,
                "subscribers_count": repo.subscribers_count,
                "last_updated": make_aware(repo.updated_at),
                "owner_id": repo.owner.id,
                "owner_type": "org" if repo.owner.type == "Organization" else "user",
            },
        )

        logger.info(
            f"Retrieved and updated repository information for repository with ID {repo_object.repository_id}"
        )


@celery_app.task(bind=True)
def get_organization_users_and_teams(
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
    # Github doesn't let us return a list of members with the attribute of admin or not, so we have to make two passes
    github_org_admins = github_organization.get_members(role="admin")
    for org_admin in github_org_admins:
        user_object: models.GithubUser
        created: bool
        user_object: models.GithubUser = github_user_to_db_object(org_admin)
        models.OrganizationMember.objects.update_or_create(
            user=user_object,
            organization=organization_object,
            defaults={"is_organization_admin": True},
        )

        logger.info(
            f"Retrieved and updated user information for user ID {user_object.user_id}"
        )

    all_org_users = github_organization.get_members(role="member")
    for org_user in all_org_users:
        user_object: models.GithubUser = github_user_to_db_object(org_user)
        models.OrganizationMember.objects.update_or_create(
            user=user_object,
            organization=organization_object,
            defaults={"is_organization_admin": False},
        )

        logger.info(
            f"Retrieved and updated user information for user ID {user_object.user_id}"
        )

    # Get teams
    # Just to make sure that any team which has a parent team is already in the database, we retrieve every team,
    # then start putting them in the database
    # We add every team to the database, then iterate over again to add parents
    teams_dict = {}
    # We store these in a dictionary to prevent having to reiterate through the github API
    for team in github_organization.get_teams():
        teams_dict[team.id] = team

    logger.info("Retrieved teams")

    for team_id in teams_dict.keys():
        team = teams_dict[team_id]
        team_object: models.Team
        created: bool
        team_object, created = models.Team.objects.update_or_create(
            team_id=team.id,
            organization=organization_object,
            defaults={
                "name": team.name,
                "slug": team.slug,
                "description": team.description,
            },
        )
        logger.info(f"Created team #{team.id}")
        # Add users to team
        for user in team.get_members():
            team_object.members.add(models.GithubUser.objects.get(user_id=user.id))
        team_object.save()
        logger.info(f"Added team members to team #{team.id}")

    # Iterate through team again and add parent team if necessary
    logger.info("Adding parent teams")
    for team_id in teams_dict.keys():
        team = teams_dict[team_id]
        if team.parent is None:
            continue
        team_object: models.Team = models.Team.objects.get(team_id=team.id)
        team_object.parent = models.Team.objects.get(team_id=team.parent.id)
        team_object.save()

    logger.info("Gathered teams parents")


@celery_app.task(bind=True)
def get_organization_repo_permissions(
    self,
    installation_id: int,
    organization_id: int,
    dependent_task_ids: List[str],
    integration_object: GithubIntegration = None,
):
    completed: bool = False
    fatal: bool = False
    while not completed and not fatal:
        time.sleep(5)
        completed, fatal = check_all_tasks_complete(dependent_task_ids)
        if not completed and not fatal:
            logger.info("Waiting on dependent tasks to be completed... sleeping")
        if not completed and fatal:
            logger.fatal("Error in completing dependent tasks, exiting")
            return
    logger.info("Tasks completed, running")


