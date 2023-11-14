from ninja import NinjaAPI

from bats_ai.core import views

api = NinjaAPI()

api.add_router('/project', views.projects.router)
api.add_router('/survey', views.surveys.router)
