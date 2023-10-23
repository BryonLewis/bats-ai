from django.http import HttpResponseRedirect
from django_filters import rest_framework as filters
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from bats_ai.core.models import Survey


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = [
            'project',
            'start_date',
            'grts_cell_id',
            'sample_frame',
            'grts_id',
        ]


class SurveyViewSet(ReadOnlyModelViewSet):
    queryset = Survey.objects.all()

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = SurveySerializer

    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['project', 'start_date']

    pagination_class = PageNumberPagination
