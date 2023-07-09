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
from .models import *
from .forms import *
import osmnx as ox
import networkx as nx
from geopy.geocoders import Nominatim
from geopy import distance
from notifications.signals import notify

def get_public_ip():
    print("recuperation de l'addresse ip\n")
    response = requests.get('http://ip.jsontest.com/')
    data = response.json()
    ip = data['ip']
    return ip

def get_location(ip):
    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'success':
        city = data['city']
        regionName = data['regionName']
        country = data['country']
        lat = data['lat']
        lon = data['lon']
        return f"{city}, {regionName}, {country}", lat, lon
    else:
        return None, None, None

def index(request):
    ip = ""
    # Obtenir l'adresse IP publique
    if request.method == "POST"  :
        ip = request.POST.get('ip')
    else:
        try:
            ip = get_public_ip()
        except:
            ConnectionError ()
            return render(request, 'index.html', {'carte': "<H3 style='padding:20%'>PAS DE CONNECTION INTERNET, VEILLEZ VOUS CONNECTER!!</H3>"})


    print("L'adresse ip  publique du server est :", ip)

    
    # Obtenir la latitude et la longitude de l'adresse IP
    lieu, lat, lon = get_location(ip)

    print('Coordonnees geographique:', lon, lat, lieu)

    # Créer une carte Folium centrée sur la position obtenue
    map = folium.Map(location=[lat, lon], zoom_start=15)

    # Ajouter un marqueur à la position obtenue
    folium.Marker([lat, lon], popup=f'Position actuelle:<br> {lieu}').add_to(map)

    # Convertir la carte en HTML
    map_html = map._repr_html_()
    
    u1 = User.objects.get(username="enfantin")
    u2 = User.objects.get(username="sergenoah")
    u3 = User.objects.get(username="bipbip")
    notify.send(u2, recipient=u3, verb='Salut bip, c\'est pour le test')

    # Passer le HTML de la carte au template
    return render(request, 'index.html', {'carte': map_html})





def recherche_lieu(request):
    if request.method == 'POST':
        form = LieuForm(request.POST)
        if form.is_valid():
            nom_lieu = form.cleaned_data['nom']
            
            # Effectuer une requête de géocodage à l'API de Nominatim d'OpenStreetMap
            response = requests.get(f'https://nominatim.openstreetmap.org/search?q={nom_lieu}&format=json')
            data = response.json()
            
            if data:
                lieu = data[0]
                print(data)
                
                # Extraire les coordonnées géographiques du lieu
                latitude = float(lieu['lat'])
                longitude = float(lieu['lon'])
                nom = lieu['display_name']
                typee = lieu['type']
                
                # Enregistrer le lieu dans la base de données
                lieu_obj = Lieu(nom_de_recherche=nom_lieu, nom=nom , latitude=latitude, longitude=longitude)
                lieu_obj.save()
                
                # Créer une carte Folium centrée sur la position obtenue
                map = folium.Map(location=[latitude, longitude], zoom_start=10)

                # Ajouter un marqueur à la position obtenue
                folium.Marker([latitude, longitude], popup=nom).add_to(map)

                # Convertir la carte en HTML
                map_html = map._repr_html_()

                # Passer le HTML de la carte au template
                return render(request, 'test.html', {'carte': map_html, 'nom':nom, 'type':type})
                
    
    else:
        print('pas de lieu donne ok \n Recherche des coordonnees en fonction de l\'ip :')
        ip = get_public_ip()
        print("L'adresse ip  publique du server est :", ip)

    
        # Obtenir la latitude et la longitude de l'adresse IP
        lieu, lat, lon = get_location(ip)

        print('Coordonnees geographique:', lon, lat, lieu)

        # Créer une carte Folium centrée sur la position obtenue
        map = folium.Map(location=[lat, lon], zoom_start=15)

        # Ajouter un marqueur à la position obtenue
        folium.Marker([lat, lon], popup=f'Position actuelle:<br> {lieu}').add_to(map)

        # Convertir la carte en HTML
        map_html = map._repr_html_()


        form = LieuForm()

    context = {'form': form, "carte":map }
    return render(request, 'test.html', context)



def recherche_taxi(request):
    if request.method == 'POST':
        form = TaxiCommandForm(request.POST)
        if form.is_valid():
            arrive = form.cleaned_data['arrive']
            montant = form.cleaned_data['montant']
            #Prevennir les taxis autours
           
    else:
        print('pas de lieu donne ok \n Recherche des coordonnees en fonction de l\'ip :')
        ip = get_public_ip()
        print("L'adresse ip  publique du server est :", ip)

    
        # Obtenir la latitude et la longitude de l'adresse IP
        lieu, lat, lon = get_location(ip)

        print('Coordonnees geographique:', lon, lat, lieu)

        # Créer une carte Folium centrée sur la position obtenue
        map = folium.Map(location=[lat, lon], zoom_start=15)

        # Ajouter un marqueur à la position obtenue
        folium.Marker([lat, lon], popup=f'Position actuelle:<br> {lieu}').add_to(map)

        # Convertir la carte en HTML
        map_html = map._repr_html_()

        form = TaxiCommandForm()

    context = {'form': form, "carte":map }
    return render(request, 'test.html', context)




def calculate_distance(origin, destination):
    # Utiliser geopy pour obtenir les coordonnées géographiques des lieux
    geolocator = Nominatim(user_agent="my-app")
    location_origin = geolocator.geocode(origin)
    location_destination = geolocator.geocode(destination)

    if location_origin is None or location_destination is None:
        return None

    coords_origin = (location_origin.latitude, location_origin.longitude)
    coords_destination = (location_destination.latitude, location_destination.longitude)

    # Utiliser osmnx pour récupérer les données du graphe de rue depuis OpenStreetMap
    graph = ox.graph_from_point(coords_origin, network_type='all')

    # Obtenir les nœuds les plus proches des coordonnées de départ et d'arrivée
    origin_node = ox.distance.nearest_nodes(graph, coords_origin[1], coords_origin[0])
    destination_node = ox.distance.nearest_nodes(graph, coords_destination[1], coords_destination[0])

    # Calculer le meilleur itinéraire entre les nœuds de départ et d'arrivée
    route = nx.shortest_path(graph, origin_node, destination_node, weight='length')

    # Calculer la distance totale de l'itinéraire
    total_distance = sum(ox.utils_graph.get_route_edge_attributes(graph, route, 'length'))
    nodes_coordinates = [graph.nodes[node_id] for node_id in route]


    coordinates_list = []

    for node in nodes_coordinates:
        lon = node['y']
        lat = node['x']
        coordinates_list.append([lon, lat])
    print(coordinates_list)

    return coordinates_list, total_distance


def search(request):
    if request.method == 'POST':
        form_data = request.POST
        origin = form_data.get('nom_depart')
        destination = form_data.get('nom_arrive')

        route, distance = calculate_distance(origin, destination)

        if route is not None:
            print("route:", route)
            print("distance:", distance)
            # Utiliser folium pour générer une carte interactive
            map_center = [(route[0][0] + route[-1][0]) / 2, (route[0][1] + route[-1][1]) / 2]
            m = folium.Map(location=map_center, zoom_start=12)

            # Ajouter les points de départ et d'arrivée à la carte
            folium.Marker(location=route[0], icon=folium.Icon(color='green'), popup=origin).add_to(m)
            folium.Marker(location=route[-1], icon=folium.Icon(color='red'), popup=destination).add_to(m)

            # Ajouter l'itinéraire à la carte en bleu
            folium.PolyLine(locations=route, color='blue').add_to(m)

            # Convertir la carte en HTML
            map_html = m._repr_html_()
            form = SearchForm(request.POST or None)

            return render(request, 'test.html', {'distance': distance, 'carte': map_html, 'nom':origin, 'type':destination, 'form':form})
        else:
            # Gérer le cas où l'un ou les deux lieux n'ont pas pu être géocodés

            form = SearchForm(request.POST or None)
            return render(request, 'test.html', {'form':form})

    else:
        print('pas de lieu donne ok \n Recherche des coordonnees en fonction de l\'ip :')

        ip = get_public_ip()
        prprint("L'adresse ip  publique du server est :", ip)

    
        # Obtenir la latitude et la longitude de l'adresse IP
        lieu, lat, lon = get_location(ip)

        print('Coordonnees geographique:', lon, lat, lieu)

        # Créer une carte Folium centrée sur la position obtenue
        map = folium.Map(location=[lat, lon], zoom_start=15)

        # Ajouter un marqueur à la position obtenue
        folium.Marker([lat, lon], popup=f'Position actuelle:<br> {lieu}').add_to(map)

        # Convertir la carte en HTML
        map_html = map._repr_html_()

        form = SearchForm()

    context = {'form': form, "carte":map }
    return render(request, 'test.html', context)

