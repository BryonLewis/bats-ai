# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow
#   * Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.gis.db import models


class Species(models.Model):
    species_code = models.CharField(max_length=10, blank=True, null=True)
    family = models.CharField(max_length=50, blank=True, null=True)
    genus = models.CharField(max_length=50, blank=True, null=True)
    species = models.CharField(max_length=100, blank=True, null=True)
    common_name = models.CharField(max_length=100, blank=True, null=True)
    species_code_6 = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'species'


class AcousticBatch(models.Model):
    survey_event = models.ForeignKey('SurveyEvent', models.DO_NOTHING)
    survey_type = models.ForeignKey('SurveyType', models.DO_NOTHING)
    software = models.ForeignKey('Software', models.DO_NOTHING, blank=True, null=True)
    classifier = models.ForeignKey('Classifier', models.DO_NOTHING, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    processed_date = models.DateTimeField(blank=True, null=True)
    processing_notes = models.TextField(blank=True, null=True)
    transaction_uuid = models.UUIDField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acoustic_batch'


class AcousticFile(models.Model):
    id = models.BigAutoField(primary_key=True)
    recording_time = models.DateTimeField(blank=True, null=True)
    recording_location = models.GeometryField(srid=0, blank=True, null=True)
    file_name = models.CharField(max_length=255)
    s3_verified = models.BooleanField(blank=True, null=True)
    project = models.ForeignKey('Project', models.DO_NOTHING)
    length_ms = models.IntegerField(blank=True, null=True)
    size_bytes = models.IntegerField(blank=True, null=True)
    survey_event = models.ForeignKey('SurveyEvent', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acoustic_file'
        unique_together = (('project', 'file_name'),)


class AcousticFileBatch(models.Model):
    id = models.BigAutoField(primary_key=True)
    file = models.ForeignKey(AcousticFile, models.DO_NOTHING)
    batch = models.ForeignKey(AcousticBatch, models.DO_NOTHING)
    auto = models.ForeignKey(
        Species, models.DO_NOTHING, related_name='%(class)s_species_auto', blank=True, null=True
    )
    manual = models.ForeignKey(
        Species, models.DO_NOTHING, related_name='%(class)s_species_manual', blank=True, null=True
    )
    recording_night = models.DateField()
    vetter = models.CharField(max_length=255, blank=True, null=True)

    # A unique constraint could not be introspected.
    class Meta:
        managed = False
        db_table = 'acoustic_file_batch'
        unique_together = (
            ('file', 'batch', 'auto'),
            ('file', 'batch', 'auto', 'manual'),
        )


class AcousticFileImage(models.Model):
    id = models.BigAutoField(primary_key=True)
    acoustic_file = models.ForeignKey(
        AcousticFile, models.DO_NOTHING, related_name='acoustic_file_image'
    )
    offset_milliseconds = models.IntegerField()
    frequency = models.IntegerField()
    image = models.TextField()

    class Meta:
        managed = False
        db_table = 'acoustic_file_image'


class Classifier(models.Model):
    name = models.CharField(unique=True, max_length=100)
    description = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    public = models.BooleanField(blank=True, null=True)
    project_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'classifier'


class EventGeometry(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    survey_type = models.ForeignKey('SurveyType', models.DO_NOTHING, blank=True, null=True)
    geom = models.GeometryField(srid=0, blank=True, null=True)
    project_id = models.IntegerField()
    created_date = models.DateTimeField(blank=True, null=True)
    transaction_uuid = models.UUIDField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event_geometry'


class Project(models.Model):
    project_key = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255)
    description = models.TextField()
    created_date = models.DateTimeField(blank=True, null=True)
    organization_id = models.IntegerField()
    sample_design_id = models.IntegerField(blank=True, null=True)
    sample_design_details = models.TextField(blank=True, null=True)
    sample_frame_id = models.IntegerField()
    soft_delete = models.BooleanField(blank=True, null=True)
    archive = models.BooleanField(blank=True, null=True)
    grts_priority = models.BooleanField(blank=True, null=True)
    test = models.BooleanField(blank=True, null=True)
    protocols = models.BooleanField(blank=True, null=True)
    endangered = models.BooleanField(blank=True, null=True)
    control = models.BooleanField(blank=True, null=True)
    batamp = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project'


class Software(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    developer = models.CharField(max_length=100, blank=True, null=True)
    version_number = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'software'


class Survey(models.Model):
    project = models.ForeignKey(Project, models.DO_NOTHING)
    start_date = models.DateField(blank=True, null=True)
    grts_cell_id = models.IntegerField(blank=True, null=True)
    sample_frame = models.TextField(blank=True, null=True)
    transaction_uuid = models.UUIDField(blank=True, null=True)
    grts_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'survey'
        unique_together = (('project', 'grts_id'),)


class SurveyEvent(models.Model):
    id = models.BigAutoField(primary_key=True)
    survey = models.ForeignKey(Survey, models.DO_NOTHING)
    survey_type = models.ForeignKey('SurveyType', models.DO_NOTHING)
    event_geometry = models.ForeignKey(EventGeometry, models.DO_NOTHING, blank=True, null=True)
    transaction_uuid = models.UUIDField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    modified_by = models.CharField(max_length=255, blank=True, null=True)
    uuid = models.UUIDField()

    class Meta:
        managed = False
        db_table = 'survey_event'


class SurveyType(models.Model):
    description = models.CharField(max_length=255, blank=True, null=True)
    map_color = models.CharField(max_length=7, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'survey_type'
