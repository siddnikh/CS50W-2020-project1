from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("random", views.rand, name = "random"),
    path("edit/<str:TITLE>", views.edit, name = "edit"),
    path("new", views.new, name = "new"),
    path("<str:TITLE>", views.entry, name = "entry")
]
