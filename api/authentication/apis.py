from rest_framework import permissions, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from api.authentication.selectors import validate_phone
from api.common.validators import is_phone


class MyTokenObtainPairView(TokenObtainPairView):
    class TokenSerializer(TokenObtainPairSerializer):
        @classmethod
        def get_token(cls, user):
            token = super().get_token(user)

            # Users Claims
            token["name"] = user.name
            token["phone"] = user.username
            token["national_id"] = user.national_id
            token["firebase_token"] = user.firebase_token
            token["gov"] = user.location.gov.name_ar
            token["city"] = user.location.city.name_ar
            return token

    serializer_class = TokenSerializer


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
