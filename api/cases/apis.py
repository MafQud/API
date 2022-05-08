from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.apis.pagination import LimitOffsetPagination, get_paginated_response
from api.cases.selectors import get_case, list_case
from api.cases.services import create_case
from api.common.utils import inline_serializer
from api.users.models import User


class CreateCaseApi(APIView):
    class InputSerializer(serializers.Serializer):
        type = serializers.CharField()
        photos_urls = serializers.ListField(child=serializers.URLField())
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


class CaseListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(serializers.Serializer):
        type = serializers.CharField(required=False)
        start_age = serializers.IntegerField(required=False)
        end_age = serializers.IntegerField(required=False)
        start_date = serializers.DateField(required=False)
        end_date = serializers.DateField(required=False)
        gov = serializers.IntegerField(required=False)
        name = serializers.CharField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        type = serializers.CharField()
        name = serializers.CharField(source="details.name")
        location = inline_serializer(
            fields={
                "gov": serializers.CharField(source="gov.name_ar"),
                "city": serializers.CharField(source="city.name_ar"),
            }
        )
        photos = serializers.ListField(source="photo_urls")
        last_seen = serializers.DateField(source="details.last_seen")
        posted_at = serializers.DateTimeField()

    def get(self, request):
        # Make sure the filters are valid, if passed
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        cases = list_case(filters=filters_serializer.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=cases,
            request=request,
            view=self,
        )


class DetailsCaseApi(APIView):
    class OutputSerializer(serializers.Serializer):
        user = serializers.IntegerField()
        type = serializers.CharField()
        state = serializers.CharField(source="get_state_display")
        photos = serializers.ListField(source="photo_urls")
        location = inline_serializer(
            fields={
                "gov": serializers.CharField(),
                "city": serializers.CharField(),
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

    def get(self, request, case_id):
        case = get_case(pk=case_id, fetched_by=request.user)

        serializer = self.OutputSerializer(case)

        return Response(serializer.data)
