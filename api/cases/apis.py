from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.apis.pagination import LimitOffsetPagination, get_paginated_response
from api.cases.models import Case
from api.cases.selectors import get_case, list_case, list_case_match, list_user_cases
from api.cases.services import create_case, publish_case
from api.common.utils import inline_serializer


class CreateCaseApi(APIView):
    class InputSerializer(serializers.Serializer):
        type = serializers.CharField()
        thumbnail = serializers.IntegerField()
        file_ids = serializers.ListField(child=serializers.IntegerField())
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
            required=False,
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
            },
        )

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_case(user=request.user, **serializer.validated_data)

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
        thumbnail = serializers.URLField(source="thumbnail.url")
        last_seen = serializers.DateField(source="details.last_seen")
        posted_at = serializers.DateTimeField()
        location = inline_serializer(
            fields={
                "gov": serializers.CharField(source="gov.name_ar"),
                "city": serializers.CharField(source="city.name_ar"),
            }
        )

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
        user = serializers.CharField(source="user.username")
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


class CaseMatchListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    def get(self, request, case_id):

        # Fetching our case
        case = get_case(pk=case_id, fetched_by=request.user)

        # Selecting which cases to serialize depending on case type
        case_source = "missing" if case.type == Case.Types.FOUND else "found"

        # Writing our serializer here because of case source decision
        class OutputSerializer(serializers.Serializer):
            case = inline_serializer(
                fields={
                    "id": serializers.IntegerField(),
                    "type": serializers.CharField(),
                    "name": serializers.CharField(source="details.name"),
                    "location": inline_serializer(
                        fields={
                            "gov": serializers.CharField(source="gov.name_ar"),
                            "city": serializers.CharField(source="city.name_ar"),
                        },
                    ),
                    "thumbnail": serializers.URLField(source="thumbnail.url"),
                    "last_seen": serializers.DateField(source="details.last_seen"),
                    "posted_at": serializers.DateTimeField(),
                },
                source=case_source,
            )
            score = serializers.IntegerField()

        # Listing all case matches
        matches = list_case_match(case=case, fetched_by=request.user)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=OutputSerializer,
            queryset=matches,
            request=request,
            view=self,
        )


class CasePublishApi(APIView):
    def get(self, request, case_id):
        case = get_case(pk=case_id, fetched_by=request.user)
        publish_case(case=case, performed_by=request.user)
        return Response(status=status.HTTP_200_OK)


class UserCasesListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        type = serializers.CharField()
        state = serializers.CharField(source="get_state_display")
        name = serializers.CharField(source="details.name")
        thumbnail = serializers.URLField(source="thumbnail.url")
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
        cases = list_user_cases(request.user)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=cases,
            request=request,
            view=self,
        )
