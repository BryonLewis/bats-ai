from django.contrib.postgres.aggregates import JSONBAgg
from django.db.models import Count, F
from ninja import Schema
from ninja.pagination import RouterPaginated

from bats_ai.core.models import Project

router = RouterPaginated()


class ProjectsSchema(Schema):
    projectKey: str
    name: str
    description: str
    grtsIds: list[int]
    grtsCellIds: list[int]
    surveyUUID: list[str]
    surveys: int


@router.get('/', response=list[ProjectsSchema], exclude_none=True)
def hello(request):
    return (
        Project.objects.prefetch_related(
            'survey',
        )
        .values()
        .annotate(
            projectKey=F('project_key'),
            name=F('project_name'),
            description=F('description'),
            grtsIds=JSONBAgg('survey__grts_id', distinct=True),
            grtsCellIds=JSONBAgg('survey__grts_cell_id', distinct=True),
            surveys=Count('survey__surveyevent'),
            surveyUUID=JSONBAgg('survey__surveyevent__uuid'),
        )
    )
