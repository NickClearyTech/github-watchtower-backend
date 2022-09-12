from rest_framework import viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend
from watchtower_service.serializers import RepositorySerializer
from watchtower_service.authorization.get_user_objects import get_user_repositories
from rest_framework.filters import SearchFilter
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Repository"])
class RepositoryViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    serializer_class = RepositorySerializer

    def get_queryset(self):
        return get_user_repositories(self.request)

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["archived", "is_fork", "owner_id", "name"]
    search_fields = ["name", "description"]
