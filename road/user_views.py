from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm, UpdateForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .views import get_location, get_public_ip
import folium
from django.http import JsonResponse



def default_lieu():
    print('pas de lieu donne ok \n Recherche des coordonnees en fonction de l\'ip :')
    ip = get_public_ip()
    print("L'adresse ip est :", ip)

    # Obtenir la latitude et la longitude de l'adresse IP
    lat, lon = get_location(ip)

    print('Coordonnees geographique:', lon, lat)

    # Créer une carte Folium centrée sur la position obtenue
    map = folium.Map(location=[lat, lon], zoom_start=20)

    # Ajouter un marqueur à la position obtenue
    folium.Marker([lat, lon], popup='Position actuelle du server').add_to(map)

    # Convertir la carte en HTML
    map = map._repr_html_()

    return map

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('road:login')
    else:
        form = RegisterForm()
        map = default_lieu()
    return render(request, 'road/register.html', {'form': form, 'carte':map})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('road:index')
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        map = default_lieu()
        form = LoginForm()
    return render(request, 'road/login.html', {'form': form, 'carte':map})

def user_logout(request):
    logout(request)
    return redirect('road:login')


@login_required
def update_profile(request):
    user = request.user
    utilisateur = user.utilisateur
    if request.method == 'POST':
        form = UpdateForm(request.POST, request.FILES, instance=request.user.utilisateur)
        if form.is_valid():
            form.save()
            return redirect('road:detail')
    else:
        map = default_lieu()
        form = UpdateForm(instance=request.user.utilisateur)
    return render(request, 'road/update.html', {'form': form, 'carte':map})



@login_required(login_url="road:login")
def utilisateur_detail(request):
    utilisateur = request.user.utilisateur  # Récupère l'objet Utilisateur associé à l'utilisateur connecté
    map = default_lieu()
    context = {'utilisateur': utilisateur, 'carte':map}
    return render(request, 'road/utilisateur_detail.html', context)



def reload(request):
    if request.method == 'POST':
        print("recepteption ds donnees par ajax")
        lon =request.POST.get('longitude')
        lat =request.POST.get('latitude')
        print("lon: ", lon, "lat :", lat)
        map = folium.Map(location=[lat, lon], zoom_start=30)

        # Ajouter un marqueur à la position obtenue
        folium.Marker([lat, lon], popup='Position actuelle').add_to(map)

        # Convertir la carte en HTML
        map = map._repr_html_()
        return JsonResponse({'map':map})
