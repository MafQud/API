from rest_framework import permissions, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from api.locations.selectors import list_governorate, list_governorate_cities


class GovernorateListApi(APIView):
    permission_classes = [permissions.AllowAny]

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name_ar = serializers.CharField()
        name_en = serializers.CharField()

    def get(self, request):

        # Listing all user cases
        govs = list_governorate()

        # Serializing the results
        serializer = self.OutputSerializer(govs, many=True)

        return Response(serializer.data)


class GovernorateCitiesListApi(APIView):
    permission_classes = [permissions.AllowAny]

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name_ar = serializers.CharField()
        name_en = serializers.CharField()

    def get(self, request, gov_id):

        # Listing all user cases
        cities = list_governorate_cities(gov_id)

        # Serializing the results
        serializer = self.OutputSerializer(cities, many=True)

        return Response(serializer.data)
