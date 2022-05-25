from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from api.apis.pagination import get_paginated_response
from api.notifications.selectors import list_user_notification


class NotificationListApi(APIView):
    class Pagination(PageNumberPagination):
        page_size = 15

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        body = serializers.CharField()
        title = serializers.CharField()
        level = serializers.CharField()
        created_at = serializers.DateTimeField()
        read_at = serializers.DateTimeField()
        sent_to = serializers.URLField(source="sent_to.get_absolute_url")

    def get(self, request):

        notifications = list_user_notification(user=request.user)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=notifications,
            request=request,
            view=self,
        )
