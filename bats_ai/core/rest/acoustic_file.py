from django.http import HttpResponseRedirect
from django_filters import rest_framework as filters
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from bats_ai.core.models import AcousticFile
from bats_ai.core.rest.species import SpeciesSerializer


class AcousticFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcousticFile
        fields = [
            'id',
            'recording_time',
            'recording_location',
            'file_name',
            's3_verified',
            'length_ms',
            'size_bytes',
            'survey_event',
        ]


class AcousticFileViewSet(ReadOnlyModelViewSet):
    queryset = AcousticFile.objects.all()

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = AcousticFileSerializer

    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = [
        'recording_time',
    ]

    pagination_class = PageNumberPagination
