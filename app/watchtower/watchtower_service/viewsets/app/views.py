from rest_framework import viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend
from watchtower_service.serializers import AppSerializer
from watchtower_service.authorization.get_user_objects import get_user_applications
from rest_framework.filters import SearchFilter
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["App"])
class AppViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    serializer_class = AppSerializer

    def get_queryset(self):
        return get_user_applications(self.request)

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["name", "slug", "owner_id"]
    search_fields = ["name", "slug"]
