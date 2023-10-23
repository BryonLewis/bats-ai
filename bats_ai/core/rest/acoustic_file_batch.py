from django.http import HttpResponseRedirect
from django_filters import rest_framework as filters
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from bats_ai.core.models import AcousticFileBatch
from bats_ai.core.rest.species import SpeciesSerializer


class AcousticFileBatchSerializer(serializers.ModelSerializer):
    auto = SpeciesSerializer()
    manual = SpeciesSerializer()

    class Meta:
        model = AcousticFileBatch
        fields = [
            'id',
            'batch',
            'auto',
            'manual',
            'recording_night',
            'vetter',
        ]


class AcousticFileBatchViewSet(ReadOnlyModelViewSet):
    queryset = AcousticFileBatch.objects.all()

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = AcousticFileBatchSerializer

    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['recording_night', 'vetter']

    pagination_class = PageNumberPagination
