from watchtower_service.celery import app as celery_app
from watchtower_service.utils.github_utils.auth_object import get_github_api_object


@celery_app.task
def test_task():
    get_github_api_object(124)
