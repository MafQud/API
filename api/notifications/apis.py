from rest_framework import permissions, serializers
from rest_framework.views import APIView

from api.apis.pagination import LimitOffsetPagination, get_paginated_response
from api.notifications.selectors import list_notification


class NotificationListApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        body = serializers.CharField()
        title = serializers.CharField()
        level = serializers.CharField()
        created_at = serializers.DateTimeField()
        read_at = serializers.DateTimeField()
        sent_to = serializers.URLField(source="sent_to.get_absolute_url")

    def get(self, request):

        notifications = list_notification(user=request.user)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=notifications,
            request=request,
            view=self,
        )
