'''
from django.shortcuts import render
import requests
import folium

def index(request):
    # Obtenez l'adresse IP de l'utilisateur depuis la demande
    #ip = request.META.get('REMOTE_ADDR')
    if request.method == 'POST':
        ip = request.POST.get('ip')

        # Utilisez une API pour obtenir les coordonnées géographiques basées sur l'adresse IP
        response = requests.get(f'http://ip-api.com/json/{ip}')
        print(response)
        data = response.json()
        print(data)
        if data['status'] =="success":
            lat = data['lat']
            lon = data['lon']

            # Créez une carte Folium centrée sur les coordonnées géographiques de l'utilisateur
            map = folium.Map(location=[lat, lon], zoom_start=12)

            # Ajoutez un marqueur à la position de l'utilisateur sur la carte
            folium.Marker([lat, lon], popup='Your Location').add_to(map)

            # Rendez le modèle avec la carte Folium dans le contexte
            return render(request, 'base.html', {'carte': map._repr_html_()})
    else :
        c = folium.Map(location=[ 43.6000, 1.433333])
        c = c.get_root()._repr_html_()
        return render(request, 'base.html', {'carte':c})


# Create your views here.
def index1(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # Créer une carte Folium centrée sur les coordonnées de la requête POST
        map = folium.Map(location=[latitude, longitude], zoom_start=12)

        # Ajouter un marqueur pour les coordonnées de la requête POST
        folium.Marker([latitude, longitude]).add_to(map)

        # Convertir la carte Folium en HTML
        map_html = map._repr_html_()

        # Passer la carte HTML à la template pour l'affichage
        context = {'carte': map_html}
        return render(request, 'carte.html', context)

    c = folium.Map(location=[ 43.6000, 1.433333])
    c = c.get_root()._repr_html_()
    return render(request, 'base.html', {'carte':c})'''


# views.py
import requests
from django.shortcuts import render
import folium

def get_public_ip():
    response = requests.get('https://api.ipify.org?format=json')
    data = response.json()
    ip = data['ip']
    return ip

def get_location(ip):
    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'success':
        lat = data['lat']
        lon = data['lon']
        return lat, lon
    else:
        return None, None

def index(request):
    # Obtenir l'adresse IP publique
    ip = get_public_ip()
    print("L'adresse ip est :", ip)

    # Obtenir la latitude et la longitude de l'adresse IP
    lat, lon = get_location(ip)

    print('Coordonnees geographique:', lon, lat)

    # Créer une carte Folium centrée sur la position obtenue
    map = folium.Map(location=[lat, lon], zoom_start=10)

    # Ajouter un marqueur à la position obtenue
    folium.Marker([lat, lon], popup='Position actuelle').add_to(map)

    # Convertir la carte en HTML
    map_html = map._repr_html_()

    # Passer le HTML de la carte au template
    return render(request, 'base.html', {'carte': map_html})
