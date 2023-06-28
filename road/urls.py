from django.urls import path
from . import views


app_name = "road"


urlpatterns = [
    path("", views.index, name="index"),
    path("recherche_lieu", views.recherche_lieu, name="recherche"),
    path("recherche_itineraire", views.search, name="itineraire"),
]
