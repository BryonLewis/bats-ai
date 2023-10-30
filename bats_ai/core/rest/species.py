from django_filters import rest_framework as filters
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet

from bats_ai.core.models import Species


class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = [
            'species_code',
            'family',
            'genus',
            'species',
            'common_name',
            'species_code_6',
        ]


class SpeciesViewSet(ReadOnlyModelViewSet):
    queryset = Species.objects.all()

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = SpeciesSerializer

    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['species_code', 'family', 'genus', 'species']

    pagination_class = PageNumberPagination
