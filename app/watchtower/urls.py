# Watchtower URL Configuration

from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from django.urls import include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from watchtower_service.views import ListView, WebHookEventView
from watchtower_service.viewsets.repository.views import RepositoryViewSet
from watchtower_service.viewsets.installation.views import InstallationViewSet
from watchtower_service.viewsets.organization.views import OrganizationViewSet
from watchtower_service.viewsets.app.views import AppViewSet


router = routers.SimpleRouter()
router.register(r"repository", RepositoryViewSet, basename="repository")
router.register(r"app", AppViewSet, basename="app")
router.register(r"organization", OrganizationViewSet, basename="organization"),
router.register(r"installation", InstallationViewSet, basename="installation")
urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("api/v1/schema", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/v1/docs",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("admin/", admin.site.urls),
    re_path(r"^auth/", include("drf_social_oauth2.urls", namespace="drf")),
    path("webhook/", WebHookEventView.as_view()),
    path("ping/", ListView.as_view()),
]
