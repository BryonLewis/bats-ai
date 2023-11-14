import datetime
from typing import Any

from django.contrib.gis.db.models.functions import AsGeoJSON
from django.contrib.postgres.aggregates import JSONBAgg
from django.db.models import Count, F, JSONField, Transform, Value
from django.db.models.functions import JSONObject  # type: ignore
from ninja import Schema
from ninja.pagination import RouterPaginated
from pydantic import UUID4

from bats_ai.core.models import SurveyEvent, AcousticFileBatch, AcousticFile, AcousticBatch

router = RouterPaginated()


class SurveysSchema(Schema):
    id: str
    startTime: datetime.datetime
    endTime: datetime.datetime
    createdDate: datetime.datetime
    modifiedDate: datetime.datetime
    createdBy: str
    modifiedBy: str
    uuid: UUID4
    eventGeom: Any
    # optional fields for surveySpecific data
    fileCount: int | None | str
    surveyTypeDesc: str | None
    surveyMapColor: str | None

class Species(Schema):
    speciesCode: str | None
    family: str | None
    genus: str | None
    species: str | None
    commonName: str | None

class Classifier(Schema):
    name: str | None
    description: str | None
    public: bool | None

class Software(Schema):
    name: str | None
    developer: str | None
    version: str | None

class SurveyDetails(Schema):
    id: str
    fileId: int
    batchId: int | None
    fileName: str
    auto: Species | None
    manual: Species | None
    software: Software | None
    classifier: Classifier | None
    annotationCount: int

@router.get('/', response=list[SurveysSchema], exclude_none=True)
def surveys(request):
    return SurveyEvent.objects.values().annotate(
        id=F('id'),
        eventGeom=JSONBAgg('event_geometry__geom'),
        startTime=F('start_time'),
        endTime=F('end_time'),
        createdDate=F('created_date'),
        modifiedDate=F('modified_date'),
        createdBy=F('created_by'),
        modifiedBy=F('modified_by'),
        uuid=F('uuid'),
        fileCount=Count('acousticbatch__acousticfilebatch__file'),
    )


@router.get('/{survey_uuid}/', response=list[SurveyDetails], exclude_none=True)
def get_survey(request, survey_uuid: UUID4):
    return (
        AcousticBatch.objects.filter(survey_event__uuid=survey_uuid)
        .prefetch_related('acousticfilebatch', 'species', 'acousticFile')
        .values()
        .annotate(
            id=F('id'),
            batchId=F('acousticfilebatch__id'),
            fileName=F('acousticfilebatch__file__file_name'),
            fileId=F('acousticfilebatch__file__id'),
            auto=JSONObject(
                speciesCode=F('acousticfilebatch__auto__species_code'),
                family=F('acousticfilebatch__auto__family'),
                genus=F('acousticfilebatch__auto__genus'),
                species=F('acousticfilebatch__auto__species'),
                commonName=F('acousticfilebatch__auto__common_name'),  
            ),
            manual=JSONObject(
                speciesCode=F('acousticfilebatch__manual__species_code'),
                family=F('acousticfilebatch__manual__family'),
                genus=F('acousticfilebatch__manual__genus'),
                species=F('acousticfilebatch__manual__species'),
                commonName=F('acousticfilebatch__manual__common_name'),  
            ),
            software=JSONObject(
                name=F('software__name'),
                developer=F('software__developer'),
                version=F('software__version_number'),
            ),
            classifier=JSONObject(
                name=F('classifier__name'),
                descriptions=F('classifier__description'),
                public=F('classifier__public'),
            ),
            annotationCount=Count('acousticfilebatch__file__acoustic_file_image__id')
        )
    )
