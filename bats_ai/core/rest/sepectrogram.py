from django.http import Http404
from rest_framework.views import APIView

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

    def get(self, pk):
        acoustic_file = self.get_object(pk)
        file_image = AcousticFileImage.objects.get(acoustic_file=acoustic_file)
        acoustic_file_batch = AcousticFileBatch.objects.get(file=acoustic_file)
        survey_event = acoustic_file.survey_event
        # projectId Number is used in the S3 file path
