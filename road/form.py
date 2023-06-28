from django import forms
from .models import *




class LieuForm(forms.ModelForm):
    class Meta:
        model = Lieu
        fields = ('nom',)
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'w3-input'}),
        }




class SearchForm(forms.ModelForm):
    class Meta:
        model = SearchForm
        fields = ['nom_depart', 'nom_arrive']
        widgets = {
            'nom_depart': forms.TextInput(attrs={'class': 'w3-input'}),
            'nom_arrive': forms.TextInput(attrs={'class': 'w3-input'}),
        }