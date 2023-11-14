from typing import Any

from django.contrib.postgres.aggregates import JSONBAgg
from django.db.models import Count, F
from ninja import Schema
from ninja.pagination import RouterPaginated
from pydantic import UUID4

from bats_ai.core.models import Project, SurveyEvent
from bats_ai.core.views.surveys import SurveysSchema

router = RouterPaginated()


class ProjectsSchema(Schema):
    projectKey: str
    name: str
    description: str
    grtsIds: list[int]
    grtsCellIds: list[int]
    surveyUUID: list[str]
    surveys: int
    eventGeometryName: list[str] | None
    eventGeometryDesc: list[str] | None
    eventGemoetryGeom: Any | None


@router.get('/', response=list[ProjectsSchema], exclude_none=True)
def projects(request):
    return (
        Project.objects.prefetch_related('survey', 'eventgeometry')
        .values()
        .annotate(
            projectKey=F('project_key'),
            name=F('project_name'),
            description=F('description'),
            grtsIds=JSONBAgg('survey__grts_id', distinct=True),
            grtsCellIds=JSONBAgg('survey__grts_cell_id', distinct=True),
            surveys=Count('survey__surveyevent'),
            surveyUUID=JSONBAgg('survey__surveyevent__uuid'),
            eventGeometryName=JSONBAgg('survey__surveyevent__event_geometry__name'),
            eventGeometryDesc=JSONBAgg('survey__surveyevent__event_geometry__description'),
            eventGemoetryGeom=JSONBAgg('survey__surveyevent__event_geometry__geom'),
        )
    )


@router.get('/{project_key}/', response=list[SurveysSchema], exclude_none=True)
def get_survey(request, project_key: UUID4):
    return (
        SurveyEvent.objects.filter(survey__project__project_key=project_key)
        .prefetch_related('acousticbatch', 'acousticfilebatch', 'species')
        .values()
        .annotate(
            id=F('id'),
            eventGeom=JSONBAgg('event_geometry__geom'),
            startTime=F('start_time'),
            endTime=F('end_time'),
            createdDate=F('created_date'),
            modifiedDate=F('modified_date'),
            createdBy=F('created_by'),
            modifiedBy=F('modified_by'),
            uuid=F('uuid'),
            surveyTypeDesc=F('survey_type__description'),
            surveyMapColor=F('survey_type__map_color'),
            fileCount=Count('acousticbatch__acousticfilebatch__file'),
        )
    )
