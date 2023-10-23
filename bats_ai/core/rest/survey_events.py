from django_filters import rest_framework as filters
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet

from bats_ai.core.models import SurveyEvent


class SurveyEventSerializer(serializers.ModelSerializer):
    surveyType = serializers.CharField(source='survey_type.description')
    surveyTypeColor = serializers.CharField(source='survey_type.map_color')

    class Meta:
        model = SurveyEvent
        fields = [
            'id',
            'survey',
            'surveyType',
            'surveyTypeColor',
            'event_geometry',
            'start_time',
            'end_time',
            'created_date',
            'modified_date',
            'created_by',
            'modified_by',
            'uuid',
        ]


class SurveyEventViewSet(ReadOnlyModelViewSet):
    queryset = SurveyEvent.objects.all()

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = SurveyEventSerializer

    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = [
        'start_time',
        'end_time',
        'created_date',
        'modified_date',
        'created_by',
        'modified_by',
    ]

    pagination_class = PageNumberPagination
