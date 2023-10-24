import json
from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from django.core.files.storage import default_storage
from bats_ai.core.models.nabatsModels import (
    AcousticFile,
    AcousticFileBatch,
    AcousticFileImage,
    SurveyEvent,
)


class Spectrogram(APIView):
    def get_object(self, pk):
        try:
            return AcousticFile.objects.get(id=pk)
        except AcousticFile.DoesNotExist:
            raise Http404

    """
    Using a fileId it gets an presigned S3 URL as well as all annotation information for the file
    """

    def get(self, request, pk, format=None):
        print(pk)
        acoustic_file = self.get_object(pk)
        file_images = AcousticFileImage.objects.filter(acoustic_file=acoustic_file.pk)
        acoustic_file_batches = AcousticFileBatch.objects.filter(file=acoustic_file)
        survey_event = acoustic_file.survey_event
        if survey_event:
            survey_type = survey_event.survey_type
        
        batches = []
        for item in acoustic_file_batches:
            sub_data = { 'vetter': item.vetter}
            if item.auto:
                sub_data['auto'] = {
                        'species': item.auto.species,
                        'species_code': item.auto.species_code,
                        'family': item.auto.family,
                        'genus': item.auto.genus,
                        'common_name': item.auto.common_name,
                    }
            if item.manual:
                sub_data['manual'] = {
                        'species': item.manual.species,
                        'species_code': item.manual.species_code,
                        'family': item.manual.family,
                        'genus': item.manual.genus,
                        'common_name': item.manual.common_name,
                    }
            batches.append(sub_data)

        annotations = []
        for item in file_images:
            annotations.append({
                'offset': item.offset_milliseconds,
                'frequency': item.frequency,
            })


        # projectId Number is used in the S3 file path
        project_num = acoustic_file.project.pk
        s3_path = f'{project_num}/{acoustic_file.file_name}'
        if default_storage.exists(s3_path):
            presigned_url = default_storage.url(s3_path)
        data = {
            'filename': acoustic_file.file_name,
            'project': project_num,
            'annotations': annotations,
            'batches': batches

        }
        if presigned_url:
            data['url'] = presigned_url
        if survey_event and survey_type:
            data['survey'] = {
                'type': {
                    'description': survey_type.description,
                    'mapColor': survey_type.map_color,
                }
            }
        
        return HttpResponse(json.dumps(data))