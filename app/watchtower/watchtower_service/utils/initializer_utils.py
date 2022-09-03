from django.contrib.auth.models import User
from oauth2_provider.models import Application
import github
from github import (
    GithubIntegration,
    Github,
    GithubApp,
    Organization,
    NamedUser,
    Repository,
)
from watchtower_service.utils.github_utils.auth_object import get_github_integration
from watchtower_service.utils.github_utils.object_retrievals import (
    get_all_integration_installations,
)
import watchtower_service.models as models
from settings import *

from logging import getLogger

logger = getLogger(__name__)


def check_and_create_initial_superuser() -> None:
    if (
        User.objects.filter(is_superuser=True, username=INITIAL_USER_USERNAME).count()
        >= 1
    ):
        logger.info("Initial superuser exists, continuing")
        return
    superuser = User(
        username=INITIAL_USER_USERNAME,
        first_name=INITIAL_USER_FIRSTNAME,
        last_name=INITIAL_USER_LASTNAME,
        email=INITIAL_USER_EMAIL,
        is_superuser=True,
    )
    superuser.save()
    logger.info("Initial superuser created")


def check_and_create_oauth_application() -> None:
    if (
        Application.objects.filter(
            client_type="public",
            authorization_grant_type="password",
            user_id=1,
            client_id=INITIAL_OAUTH_CLIENT_ID,
        ).count()
        >= 1
    ):
        logger.info("Initial OAuth application exists, continuing")
        return
    application = Application(
        client_type="public",
        authorization_grant_type="password",
        user_id=1,
        client_id=INITIAL_OAUTH_CLIENT_ID,
    )
    application.save()
    logger.info("Initial OAuth application created")


def run_startup_imports():
    git_integration = get_github_integration()

    installation_id: int = git_integration.get_installations()[0].id
    token: str = git_integration.get_access_token(installation_id).token

    github_object: Github = github.Github(token)

    app_slug: str = git_integration.get_app_slug()
    github_app_object: GithubApp = github_object.get_app(slug=app_slug)

    logger.info("Obtained initial startup information")

    app_owner_object = None
    created: bool = None

    if github_app_object.owner.type == "Organization":
        github_app_owner: Organization = github_object.get_organization(
            login=github_app_object.owner.login
        )
        app_owner_object: models.Organization
        app_owner_object, created = models.Organization.objects.get_or_create(
            organization_id=github_app_owner.id,
            organization_login=github_app_owner.login,
        )

        logger.info(
            f"{'Created' if created else 'Found'} organization object with ID {app_owner_object.organization_id}"
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
        logger.info(
            f"Updated all information for organization object with ID {app_owner_object.organization_id}"
        )
    else:
        logger.error("Unable to import github app with owner type of User")

    app_object: models.App
    app_object, created = models.App.objects.get_or_create(
        app_id=github_app_object.id,
        owner_id=github_app_object.owner.id,
        owner_type="org" if github_app_object.owner.type == "Organization" else "user",
    )

    logger.info(f"{'Created' if created else 'Found'} app with ID {app_object.app_id}")

    app_object.name = github_app_object.name
    app_object.slug = github_app_object.slug
    app_object.installation_count = github_app_object.installation_count

    logger.info(f"Updated all information for app object with ID {app_object.app_id}")

    get_all_integration_installations(git_integration)
