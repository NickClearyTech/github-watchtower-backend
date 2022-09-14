from rest_framework import viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend
from watchtower_service.serializers import OrganizationSerializer
from watchtower_service.authorization.get_user_objects import get_user_organizations
from rest_framework.filters import SearchFilter
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Organization"])
class OrganizationViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        return get_user_organizations(self.request)

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["organization_login", "organization_name", "email", "company"]
    search_fields = [
        "organization_login",
        "organization_name",
        "email",
        "company",
        "description",
    ]
