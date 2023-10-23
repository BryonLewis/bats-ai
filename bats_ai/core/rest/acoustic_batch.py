from django_filters import rest_framework as filters
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet

from bats_ai.core.models import AcousticBatch


class AcousticBatchSerializer(serializers.ModelSerializer):
    surveyType = serializers.CharField(source='survey_type.description')
    surveyTypeColor = serializers.CharField(source='survey_type.map_color')
    softwareName = serializers.CharField(source='software.name')
    softwareDeveloper = serializers.CharField(source='software.developer')
    softwareVersion = serializers.CharField(source='software.version_number')

    class Meta:
        model = AcousticBatch
        fields = [
            'id',
            'survey_event',
            'surveyType',
            'software',
            'surveyTypeColor',
            'softwareName',
            'softwareDeveloper',
            'softwareVersion',
            'processed_date',
            'processing_notes',
        ]


class AcousticBatchViewSet(ReadOnlyModelViewSet):
    queryset = AcousticBatch.objects.all()

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = AcousticBatchSerializer

    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['created_date', 'processed_date']

    pagination_class = PageNumberPagination
