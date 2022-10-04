from github import NamedUser, Permissions
import watchtower_service.models as models
from django.utils.timezone import make_aware


def github_user_to_db_object(github_user: NamedUser) -> models.GithubUser:
    """
    A helper object that takes a github user object and returns a models.GithubUser
    Why? Since we have to do this twice
    :param github_user: A github user object
    :return: A github user model
    """
    created: bool
    user_object: models.GithubUser
    user_object, created = models.GithubUser.objects.update_or_create(
        user_id=github_user.id,
        defaults={
            "login": github_user.login,
            "name": github_user.name,
            "bio": github_user.bio,
            "company": github_user.company,
            "account_created": make_aware(github_user.created_at),
            "account_updated": make_aware(github_user.updated_at),
            "disk_usage": github_user.disk_usage,
            "email": github_user.email,
            "plan": github_user.plan,
            "site_admin": github_user.site_admin,
        },
    )
    return user_object


def convert_permission_object_string(permission: Permissions) -> str:
    """
    A helper function that takes a GitHub permissions object and converts it to a string representing the
    highest level permission (admin, write, or read)
    :param permission: Github permission object
    :return: "read", "write" or "admin"
    """
    if permission.admin:
        return "admin"
    if permission.push:
        return "write"
    if permission.pull:
        return "read"
    return ""