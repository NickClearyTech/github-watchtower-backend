from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter

from watchtower_service.api_goodies.api_exceptions import InvalidParameterException

from logging import getLogger

logger = getLogger(__name__)


class ListWithOptionsMixin:
    """
    List a Queryset, but allow for the "exclude", "fields", and "depth" options
    """

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="fields",
                description="List of model fields to include, as a comma separated listed (no spaces)",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="exclude",
                description="List of model fields to exclude, as a comma separated listed (no spaces)",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="depth",
                description="Number of levels deep to serialize of subfields",
                required=False,
                type=str,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        # Get parameters
        depth = request.query_params.get("depth", None)
        fields = request.query_params.get("fields", None)
        exclude = request.query_params.get("exclude", None)
        # Get queryset and filter it
        queryset = self.filter_queryset(self.get_queryset())
        # Paginate as necessary
        page = self.paginate_queryset(queryset)

        # Validate depth parameter
        try:
            if depth is not None:
                depth = int(depth)
        except ValueError:
            raise InvalidParameterException("depth", "should be an integer")
        if depth is not None and depth > 5:
            raise InvalidParameterException("depth", "must be >=5")

        # Handle fields
        if fields is not None:
            if " " in fields:
                raise InvalidParameterException("fields", "should not contain spaces")
            fields = fields.split(",")

        # Handle excludes
        if exclude is not None:
            if " " in exclude:
                raise InvalidParameterException("exclude", "should not contain spaces")
            exclude = exclude.split(",")

        # If the page is not None, return the page
        # Unless we for some reason remove pagination completely, this should always return not None
        if page is not None:
            serializer = self.get_serializer(
                page, many=True, depth=depth, fields=fields, exclude=exclude
            )
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            queryset, many=True, depth=depth, fields=fields, exclude=exclude
        )
        return Response(serializer.data)
