from bats_ai.core.models.nabatsModels import AcousticBatch, AcousticFile, AcousticFileBatch, AcousticFileImage, Classifier, EventGeometry, Project, Software, Species, Survey, SurveyEvent, SurveyType

class BatsDBRouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """

    ROUTED_MODELS = [AcousticBatch, AcousticFile, AcousticFileBatch, AcousticFileImage, Classifier, EventGeometry, Project, Software, Species, Survey, SurveyEvent, SurveyType]


    def db_for_read(self, model, **hints):
        """
        Attempts to read scoring and contenttypes models go to batsdb.
        """
        if model in self.ROUTED_MODELS:
            return 'batsdb'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write batsdb models go to auth_db.
        """
        if model in self.ROUTED_MODELS:
            return 'batsdb'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the scoring app is
        involved.
        """
        if (
            obj1 in self.ROUTED_MODELS
            or obj2 in self.ROUTED_MODELS
        ):
            return True
        return None
