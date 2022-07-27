from django.contrib.auth.models import User
from oauth2_provider.models import Application

import settings
from watchtower_service.models import Installation
from settings import *


def check_and_create_initial_superuser() -> None:
    if (
        User.objects.filter(is_superuser=True, username=INITIAL_USER_USERNAME).count()
        >= 1
    ):
        print("Initial superuser exists, continuing")
        return
    superuser = User(
        username=INITIAL_USER_USERNAME,
        first_name=INITIAL_USER_FIRSTNAME,
        last_name=INITIAL_USER_LASTNAME,
        email=INITIAL_USER_EMAIL,
        is_superuser=True,
    )
    superuser.save()
    print("Initial superuser created")


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
        print("Initial OAuth application exists, continuing")
        return
    application = Application(
        client_type="public",
        authorization_grant_type="password",
        user_id=1,
        client_id=INITIAL_OAUTH_CLIENT_ID,
    )
    application.save()
    print("Initial OAuth application created")


def create_initial_installation() -> None:
    """
    Checks for an initial application install. If not present, creates it
    :return: None
    """
    if (
        Installation.objects.filter(
            installation_id=settings.GITHUB_APP_INSTALL_ID,
            installation_name="NickClearyTech",
        ).count()
        >= 1
    ):
        print("Initial Installation already exists")
        return
    installation = Installation(
        installation_id=settings.GITHUB_APP_INSTALL_ID,
        installation_name="NickClearyTech",
    )
    installation.save()
    print("Initial installation created")
