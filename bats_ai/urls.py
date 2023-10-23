from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from bats_ai.core.rest import (
    AcousticBatchViewSet,
    AcousticFileBatchViewSet,
    AcousticFileViewSet,
    ImageViewSet,
    ProjectViewSet,
    SpeciesViewSet,
    SurveyEventViewSet,
    SurveyViewSet,
)
from bats_ai.core.views import GalleryView, image_summary

router = routers.SimpleRouter()
router.register(r'images', ImageViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'surveys', SurveyViewSet)
router.register(r'survey_events', SurveyEventViewSet)
router.register(r'species', SpeciesViewSet)
router.register(r'acoustic_batch', AcousticBatchViewSet)
router.register(r'acoustic_file_batch', AcousticFileBatchViewSet)
router.register(r'acoustic_file', AcousticFileViewSet)


# Some more specific Api Requests
# OpenAPI generation
schema_view = get_schema_view(
    openapi.Info(title='bats-ai', default_version='v1', description=''),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('oauth/', include('oauth2_provider.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/s3-upload/', include('s3_file_field.urls')),
    path('api/v1/', include(router.urls)),
    path('api/docs/redoc/', schema_view.with_ui('redoc'), name='docs-redoc'),
    path('api/docs/swagger/', schema_view.with_ui('swagger'), name='docs-swagger'),
    path('summary/', image_summary, name='image-summary'),
    path('gallery/', GalleryView.as_view(), name='gallery'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
