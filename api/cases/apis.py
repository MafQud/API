from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.cases.services import create_case
from api.common.utils import inline_serializer
from api.users.models import User


class CreateCaseApi(APIView):
    class InputSerializer(serializers.Serializer):
        type = serializers.CharField()
        photos_urls = serializers.ListField(child=serializers.URLField())
        location = inline_serializer(
            fields={
                "gov_id": serializers.IntegerField(),
                "city_id": serializers.IntegerField(),
                "address": serializers.CharField(required=False),
                "lon": serializers.DecimalField(
                    max_digits=9, decimal_places=6, required=False
                ),
                "lat": serializers.DecimalField(
                    max_digits=8, decimal_places=6, required=False
                ),
            }
        )
        details = inline_serializer(
            fields={
                "name": serializers.CharField(required=False),
                "gender": serializers.CharField(required=False),
                "age": serializers.IntegerField(required=False),
                "last_seen": serializers.DateField(required=False),
                "description": serializers.CharField(required=False),
                "location": inline_serializer(
                    required=False,
                    fields={**location.fields},
                ),
            }
        )

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_case(user=User.objects.all()[0], **serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)


class UpdateCaseApi(APIView):
    # TODO Add permissions

    class InputSerializer(serializers.Serializer):
        photos_urls = serializers.ListField(
            child=serializers.URLField(), required=False
        )
        location = inline_serializer(
            fields={
                "gov_id": serializers.IntegerField(required=False),
                "city_id": serializers.IntegerField(required=False),
                "lon": serializers.DecimalField(
                    max_digits=9, decimal_places=6, required=False
                ),
                "lat": serializers.DecimalField(
                    max_digits=8, decimal_places=6, required=False
                ),
                "address": serializers.CharField(required=False),
            }
        )


class DetailsCaseApi(APIView):
    class OutputSerializer(serializers.Serializer):
        user = serializers.IntegerField()
        type = serializers.CharField()
        state = serializers.CharField(source="get_state_display")
        photos_urls = serializers.ListField(child=serializers.URLField())
        location = inline_serializer(
            fields={
                "gov_id": serializers.IntegerField(),
                "city_id": serializers.IntegerField(),
                "address": serializers.CharField(),
                "lon": serializers.DecimalField(
                    max_digits=9,
                    decimal_places=6,
                ),
                "lat": serializers.DecimalField(
                    max_digits=8,
                    decimal_places=6,
                ),
            }
        )
        details = inline_serializer(
            fields={
                "name": serializers.CharField(),
                "gender": serializers.CharField(),
                "age": serializers.IntegerField(),
                "last_seen": serializers.DateField(),
                "description": serializers.CharField(),
                "location": location,
            }
        )
