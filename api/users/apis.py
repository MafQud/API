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
        location = inline_serializer(
            fields={
                "gov": serializers.IntegerField(),
                "city": serializers.IntegerField(),
            }
        )
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
        location = inline_serializer(
            fields={
                "address": serializers.CharField(),
                "gov": serializers.CharField(source="gov.name_ar"),
                "city": serializers.CharField(source="city.name_ar"),
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
        location = inline_serializer(
            fields={
                "gov": serializers.IntegerField(),
                "city": serializers.IntegerField(),
                "address": serializers.CharField(required=False),
                "lon": serializers.DecimalField(
                    max_digits=9, decimal_places=6, required=False
                ),
                "lat": serializers.DecimalField(
                    max_digits=8, decimal_places=6, required=False
                ),
            },
            required=False,
        )

    def post(self, request, user_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        update_user(
            user_id=user_id,
            data=serializer.validated_data,
        )
        return Response(status=status.HTTP_200_OK)
