from django.db import models


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
    