from watchtower_service.models import *


def get_user_organizations(request):
    return Organization.objects.all()


def get_user_applications(request):
    return App.objects.all()


def get_user_installations(request):
    return Installation.objects.all()


def get_user_repositories(request):
    return Repository.objects.all()
