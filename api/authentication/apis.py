from rest_framework import permissions, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.authentication.selectors import validate_email, validate_phone
from api.users.validators import is_phone


class ValidatePhoneAPI(APIView):
    permission_classes = [permissions.AllowAny]

    class InputSerializer(serializers.Serializer):
        phone = serializers.CharField(validators=[is_phone])

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Raises validation error if phone is taken
        validate_phone(**serializer.validated_data)

        return Response(status=status.HTTP_200_OK)


class ValidateEmailAPI(APIView):
    permission_classes = [permissions.AllowAny]

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Raises validation error if email is taken
        validate_email(**serializer.validated_data)

        return Response(status=status.HTTP_200_OK)
