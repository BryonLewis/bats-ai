from django_filters import rest_framework as filters
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet

from bats_ai.core.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'project_key',
            'project_name',
            'description',
            'created_date',
            'organization_id',
            'archive',
        ]


class ProjectViewSet(ReadOnlyModelViewSet):
    queryset = Project.objects.all()

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProjectSerializer

    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['organization_id', 'archive']

    pagination_class = PageNumberPagination
