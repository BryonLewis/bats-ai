from django.core.files.storage import default_storage
from django_filters import rest_framework as filters
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from bats_ai.core.models import AcousticFile


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

    @action(detail=False, methods=['get'])
    def s3_exists(
        self,
        request,
    ):
        # get all AcousticFiles take the project.pk filed and check if an S3 field exists
        s3_exists_list = []
        acoustic_files = AcousticFile.objects.select_related('project').all()
        for item in acoustic_files:
            s3_path = f'{item.project.pk}/{item.file_name}'
            if default_storage.exists(s3_path):
                print(f'Adding {s3_path}')
                s3_exists_list.append(item)

        # Apply pagination to the s3_exists_list
        page = self.paginate_queryset(s3_exists_list)
        if page is not None:
            serializer = AcousticFileSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response([], status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def annotations_exist(
        self,
        request,
    ):
        # get all AcousticFiles take the project.pk filed and check if an S3 field exists
        acoustic_files = (
            AcousticFile.objects.select_related('project')
            .filter(acoustic_file_image__isnull=False)
            .distinct()
        )
        # Apply pagination to the s3_exists_list
        page = self.paginate_queryset(acoustic_files)
        if page is not None:
            serializer = AcousticFileSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response([], status=status.HTTP_200_OK)
