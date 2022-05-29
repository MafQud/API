from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.apis.pagination import LimitOffsetPagination, get_paginated_response
from api.notifications.selectors import get_notification, list_user_notification
from api.notifications.services import read_notification


class NotificationListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 15

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        case_id = serializers.IntegerField(source="case.id")
        case_type = serializers.CharField(source="case.type")
        level = serializers.CharField()
        action = serializers.CharField()
        body = serializers.CharField()
        created_at = serializers.DateTimeField()
        read_at = serializers.DateTimeField()

    def get(self, request):

        notifications = list_user_notification(user=request.user)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=notifications,
            request=request,
            view=self,
        )


class NotificationReadApi(APIView):
    def get(self, request, notification_id):

        notification = get_notification(pk=notification_id, fetched_by=request.user)
        read_notification(notification)

        return Response(status=status.HTTP_200_OK)
