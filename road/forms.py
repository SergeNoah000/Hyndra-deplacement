from django.contrib.auth.models import User
from .models import *

from django import forms
from django.contrib.auth.forms import UserCreationForm




class RegisterForm(UserCreationForm):
    password1 = forms.CharField(label='Mot de passe:', widget=forms.PasswordInput(attrs={'class': 'w3-input w3-border'}))
    password2 = forms.CharField(label='Confirmer le mot de passe:', widget=forms.PasswordInput(attrs={'class': 'w3-input w3-border'}))
    first_name = forms.CharField(label='Prenom:', widget=forms.TextInput(attrs={'class': 'w3-input w3-border'}))
    last_name = forms.CharField(label='Votre nom:', widget=forms.TextInput(attrs={'class': 'w3-input w3-border'}))
    email = forms.CharField(label='Adresse mail:', widget=forms.EmailInput(attrs={'class': 'w3-input w3-border'}))

    age = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'w3-input w3-border'}))
    sexe = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'w3-input w3-border'}))
    quartier = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'w3-input w3-border'}))
    photo_profil = forms.ImageField(widget=forms.FileInput(attrs={'class': 'w3-input w3-border'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Nom d'utilisateur"
        self.fields['age'].label = "Âge"
        self.fields['sexe'].label = "Sexe"
        self.fields['quartier'].label = "Quartier"
        self.fields['photo_profil'].label = "Photo de profil"

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")

        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        if commit:
            user.save()
            utilisateur = Utilisateur.objects.create(
                user=user,
                age=self.cleaned_data['age'],
                sexe=self.cleaned_data['sexe'],
                quartier=self.cleaned_data['quartier'],
                photo_profil=self.cleaned_data['photo_profil']
            )
        return user








class UpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='Prénom:', widget=forms.TextInput(attrs={'class': 'w3-input w3-border'}))
    last_name = forms.CharField(label='Votre nom:', widget=forms.TextInput(attrs={'class': 'w3-input w3-border'}))
    email = forms.EmailField(label='Adresse mail:', widget=forms.EmailInput(attrs={'class': 'w3-input w3-border'}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'w3-input w3-border'}))
    sexe = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'w3-input w3-border'}))
    quartier = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'w3-input w3-border'}))
    photo_profil = forms.ImageField(widget=forms.FileInput(attrs={'class': 'w3-input w3-border'}))

    class Meta:
        model = Utilisateur
        fields = ['age', 'sexe', 'quartier', 'photo_profil']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        utilisateur = super().save(commit=False)
        user = utilisateur.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            utilisateur.save()
        return utilisateur

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'w3-input w3-border'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w3-input w3-border'}))



class TaxiCommandForm(forms.ModelForm):
    class Meta:
        model = TaxiCommand
        fields = ['arrivee','montant']
        widgets = {
            'arrivee': forms.TextInput(attrs={'class': 'w3-input w3-border'}),
            'montant': forms.TextInput(attrs={'class': 'w3-input w3-border'}),
        }

class LieuForm(forms.ModelForm):
    class Meta:
        model = Lieu
        fields = ('nom',)
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'w3-input w3-border'}),
        }




class SearchForm(forms.ModelForm):
    class Meta:
        model = SearchForm
        fields = ['nom_depart', 'nom_arrive']
        widgets = {
            'nom_depart': forms.TextInput(attrs={'class': 'w3-input w3-border'}),
            'nom_arrive': forms.TextInput(attrs={'class': 'w3-input w3-border'}),
        }