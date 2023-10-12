from bats_ai.core.models.nabatsModels import Classifier, Species, AcousticFile, AcousticBatch, AcousticFileBatch, AcousticFileImage, Project
from django.contrib import admin
from django.utils.html import format_html
import base64

@admin.register(Classifier)
class ClassifierAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_date', 'created_by', 'public')

@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('species_code', 'family', 'genus', 'species', 'common_name', 'species_code_6')

@admin.register(AcousticFile)
class AccousticFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'recording_time', 'recording_location', 'file_name', 's3_verified', 'project', 'length_ms', 'size_bytes', 'survey_event')

@admin.register(AcousticBatch)
class AcousticBatchAdmin(admin.ModelAdmin):
    list_display = ('survey_event', 'survey_type', 'software', 'classifier', 'created_date', 'processed_date', 'processing_notes', 'transaction_uuid')

@admin.register(AcousticFileImage)
class AcousticFileImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'acoustic_file', 'image_spectro', 'offset_milliseconds', 'frequency')
    readonly_fields = ["image_spectro",]
    def image_spectro(self, obj):
        return format_html('<img src="data:;base64,{}">', obj.image)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_key', 'project_name', 'description', 'created_date', 'organization_id', 'sample_design_id', 'sample_design_details', 'sample_frame_id', 'soft_delete', 'archive', 'grts_priority', 'test', 'protocols', 'endangered', 'control', 'batamp')
