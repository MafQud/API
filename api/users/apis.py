from rest_framework import permissions, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.common.permissions import IsVerified
from api.common.utils import get_object, inline_serializer
from api.users.models import User
from api.users.services import create_user, update_user


class CreateUserApi(APIView):
    permission_classes = [permissions.AllowAny]

    class InputSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField()
        name = serializers.CharField()
        email = serializers.EmailField(required=False)
        gov_id = serializers.IntegerField()
        city_id = serializers.IntegerField()
        fcm_token = serializers.CharField()
        firebase_token = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_user(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)


class DetailUserApi(APIView):
    permission_classes = [IsVerified]

    class OutputSerializer(serializers.Serializer):
        username = serializers.CharField()
        name = serializers.CharField()
        email = serializers.CharField()
        location = inline_serializer(
            fields={
                "address": serializers.CharField(),
                "gov": inline_serializer(
                    fields={
                        "name_ar": serializers.CharField(),
                        "name_en": serializers.CharField(),
                    }
                ),
                "city": inline_serializer(
                    fields={
                        "name_ar": serializers.CharField(),
                        "name_en": serializers.CharField(),
                    }
                ),
            }
        )

    def get(self, request, user_id):
        user = get_object(User, id=user_id)
        serializer = self.OutputSerializer(user)
        return Response(serializer.data)


class UpdateUserApi(APIView):
    permission_classes = [permissions.IsAdminUser]

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)
        email = serializers.CharField(required=False)
        gov_id = serializers.IntegerField(required=False)
        city_id = serializers.IntegerField(required=False)

    def post(self, request, user_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        update_user(
            user_id=user_id,
            data=serializer.validated_data,
        )
        return Response(status=status.HTTP_200_OK)
