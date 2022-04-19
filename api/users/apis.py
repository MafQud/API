from rest_framework import permissions, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.users.services import create_user


class CreateUserApi(APIView):
    permission_classes = [permissions.AllowAny]

    class InputSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField()
        name = serializers.CharField()
        email = serializers.EmailField(required=False)
        gov_id = serializers.IntegerField()
        city_id = serializers.IntegerField()
        firebase_token = serializers.CharField()

    def post(self, request):
        print(request.data)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid()

        create_user(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)
