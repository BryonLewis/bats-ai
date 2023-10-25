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


class BatsDBRouter:
    ROUTED_MODELS = [
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
    ]

    def db_for_read(self, model, **hints):
        if model in self.ROUTED_MODELS:
            return 'batsdb'
        return None

    def db_for_write(self, model, **hints):
        if model in self.ROUTED_MODELS:
            return 'batsdb'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1 in self.ROUTED_MODELS or obj2 in self.ROUTED_MODELS:
            return True
        return None
