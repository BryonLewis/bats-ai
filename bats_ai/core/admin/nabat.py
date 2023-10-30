from django.contrib import admin
from django.utils.html import format_html

from bats_ai.core.models.nabatsModels import (
    AcousticBatch,
    AcousticFile,
    AcousticFileBatch,
    AcousticFileImage,
    Classifier,
    EventGeometry,
    Project,
    Software,
    Species,
    Survey,
    SurveyEvent,
    SurveyType,
)


@admin.register(Classifier)
class ClassifierAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_date', 'created_by', 'public')


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('species_code', 'family', 'genus', 'species', 'common_name', 'species_code_6')


@admin.register(AcousticFile)
class AccousticFileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'recording_time',
        'recording_location',
        'file_name',
        's3_verified',
        'project',
        'length_ms',
        'size_bytes',
        'survey_event',
    )


@admin.register(AcousticBatch)
class AcousticBatchAdmin(admin.ModelAdmin):
    list_display = (
        'survey_event',
        'survey_type',
        'software',
        'classifier',
        'created_date',
        'processed_date',
        'processing_notes',
        'transaction_uuid',
    )


@admin.register(AcousticFileBatch)
class AcousticFileBatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'batch', 'auto', 'manual', 'recording_night', 'vetter')


@admin.register(AcousticFileImage)
class AcousticFileImageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'acoustic_file',
        'audio_file',
        'image_spectro',
        'offset_milliseconds',
        'frequency',
    )
    readonly_fields = [
        'image_spectro',
    ]

    def image_spectro(self, obj):
        return format_html('<img src="data:;base64,{}">', obj.image)

    def audio_file(self, obj):
        return obj.acoustic_file.file_name


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'project_key',
        'project_name',
        'description',
        'created_date',
        'organization_id',
        'sample_design_id',
        'sample_design_details',
        'sample_frame_id',
        'soft_delete',
        'archive',
        'grts_priority',
        'test',
        'protocols',
        'endangered',
        'control',
        'batamp',
    )


@admin.register(EventGeometry)
class EventGeometryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'survey_type',
        'geom',
        'project_id',
        'created_date',
        'transaction_uuid',
    )


@admin.register(Software)
class SoftwareAdmin(admin.ModelAdmin):
    list_display = ('name', 'developer', 'version_number')


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = (
        'project',
        'start_date',
        'grts_cell_id',
        'sample_frame',
        'transaction_uuid',
        'grts_id',
    )


@admin.register(SurveyEvent)
class SurveyEventAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'survey',
        'survey_type',
        'event_geometry',
        'transaction_uuid',
        'start_time',
        'end_time',
        'created_date',
        'modified_date',
        'created_by',
        'uuid',
    )


@admin.register(SurveyType)
class SurveyTypeAdmin(admin.ModelAdmin):
    list_display = ('description', 'map_color')
