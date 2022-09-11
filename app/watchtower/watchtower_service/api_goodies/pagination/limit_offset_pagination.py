from rest_framework.pagination import LimitOffsetPagination


class LimitOffsetFixed(LimitOffsetPagination):
    """
    This is overriding the default limit offset class because by default there is no way to specify a max limit
    nicleary 10/22
    """

    default_limit = 500
    max_limit = 10000
    template = None
