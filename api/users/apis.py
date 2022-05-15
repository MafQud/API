from django.shortcuts import get_object_or_404
from rest_framework import permissions, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.common.utils import inline_serializer
from api.users.models import User
from api.users.selectors import get_user, get_user_cases
from api.users.services import create_user, set_national_id, update_user


class CreateUserApi(APIView):
    permission_classes = [permissions.AllowAny]

    class InputSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField()
        name = serializers.CharField()
        fcm_token = serializers.CharField()
        firebase_token = serializers.CharField()
        location = inline_serializer(
            fields={
                "gov": serializers.IntegerField(),
                "city": serializers.IntegerField(),
            }
        )

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_user(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)


class DetailUserApi(APIView):
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
        user = get_user(user_id)
        serializer = self.OutputSerializer(user)
        return Response(serializer.data)


class UpdateUserApi(APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)
        firebase_token = serializers.CharField(required=False)
        fcm_token = serializers.CharField(required=False)
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

        user = get_user(user_id)

        update_user(
            user=user,
            performed_by=request.user,
            data=serializer.validated_data,
        )
        return Response(status=status.HTTP_200_OK)


class UserCasesListApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        type = serializers.CharField()
        state = serializers.CharField(source="get_state_display")
        name = serializers.CharField(source="details.name")
        thumbnail = serializers.URLField()
        last_seen = serializers.DateField(source="details.last_seen")
        posted_at = serializers.DateTimeField()
        location = inline_serializer(
            fields={
                "gov": serializers.CharField(source="gov.name_ar"),
                "city": serializers.CharField(source="city.name_ar"),
            }
        )

    def get(self, request):

        # Listing all user cases
        cases = get_user_cases(request.user)

        # Serializing the results
        serializer = self.OutputSerializer(cases, many=True)

        return Response(serializer.data)


class SetNationalIdApi(APIView):
    class InputSerializer(serializers.Serializer):
        national_id = serializers.CharField()

    def post(self, request, user_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(User, pk=user_id)
        set_national_id(
            user=user,
            data=serializer.validated_data,
        )

        return Response(status=status.HTTP_200_OK)
