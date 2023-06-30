from django.urls import path
from . import views, user_views


app_name = "road"


urlpatterns = [
    path("reload", user_views.reload, name="reload"),
    path('register/', user_views.register, name='register'),
    path('login/', user_views.user_login, name='login'),
    path('logout/', user_views.user_logout, name='logout'),
    path('update/', user_views.update_profile, name='update'),
    path('detail/', user_views.utilisateur_detail, name='detail'),
]+[
    path("", views.index, name="index"),
    path("recherche_lieu", views.recherche_lieu, name="recherche"),
    path("recherche_itineraire", views.search, name="itineraire"),
    path("recherche_taxi", views.recherche_taxi, name="recherche_taxi"),
]
