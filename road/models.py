from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from notifications.models import Notification


class Utilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    age = models.IntegerField()
    sexe = models.CharField(max_length=10)
    quartier = models.CharField(max_length=100)
    photo_profil = models.ImageField(upload_to='profile_photos/')

    def __str__(self):
        return self.user.username


class Lieu(models.Model):
    nom_de_recherche = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    date = models.DateTimeField( auto_now=False , auto_now_add=True)

    def __str__(self):
        return self.nom
    


class SearchForm(models.Model):
    nom_depart = models.CharField(max_length=100)
    nom_arrive = models.CharField(max_length=100)
    date = models.DateTimeField( auto_now=False , auto_now_add=True)


class TaxiCommand(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    arrivee = models.CharField(max_length=100)
    montant = models.DecimalField(max_digits=8, decimal_places=2)
    date_recherche = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commande de taxi - Utilisateur: {self.user.username} - Lieu: {self.arrivee} a {self.date_recherche} "




