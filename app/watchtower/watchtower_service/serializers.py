from watchtower_service.models import *
from rest_framework.serializers import ModelSerializer, Serializer

from logging import getLogger

logger = getLogger(__name__)


class DynamicModelSerializer(ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed, and takes in a "depth" argument to
    specify the number of models deep to return
    """

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        exclude = kwargs.pop("exclude", None)
        depth = kwargs.pop("depth", None)

        # Sets a max depth, to prevent excessive depths and potential recursive serializing chains
        MAX_DEPTH = 3

        if depth is not None:
            if depth > MAX_DEPTH:
                self.Meta.depth = MAX_DEPTH
            self.Meta.depth = depth

        super(DynamicModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude is not None:
            for field_name in exclude:
                self.fields.pop(field_name)


class OrganizationSerializer(DynamicModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"
        depth = 2

        # TODO: Implement "apps" field
        # TODO: Implement installations field
        # TODO: Implement repositories field


class AppSerializer(DynamicModelSerializer):
    class Meta:
        model = App
        fields = "__all__"
        depth = 2


class Installation(DynamicModelSerializer):
    class Meta:
        model = Installation
        fields = "__all__"
        depth = 2

    # TODO: Implement "repositories" field


class RepositorySerializer(DynamicModelSerializer):
    class Meta:
        model = Repository
        fields = "__all__"
        depth = 2
