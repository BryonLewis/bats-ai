from ninja import NinjaAPI

from bats_ai.core import views

api = NinjaAPI()

api.add_router('/projects', views.projects.router)
