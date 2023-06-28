import osmnx as ox
import networkx as nx
import folium

from django.shortcuts import render
from geopy.geocoders import Nominatim
from geopy import distance


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
    graph = ox.graph_from_point(coords_origin, distance=500, network_type='all')

    # Obtenir les nœuds les plus proches des coordonnées de départ et d'arrivée
    origin_node = ox.distance.nearest_nodes(graph, coords_origin[1], coords_origin[0])
    destination_node = ox.distance.nearest_nodes(graph, coords_destination[1], coords_destination[0])

    # Calculer le meilleur itinéraire entre les nœuds de départ et d'arrivée
    route = nx.shortest_path(graph, origin_node, destination_node, weight='length')

    # Calculer la distance totale de l'itinéraire
    total_distance = sum(ox.utils_graph.get_route_edge_attributes(graph, route, 'length'))

    return route, total_distance


def search(request):
    if request.method == 'POST':
        form_data = request.POST
        origin = form_data.get('nom_depart')
        destination = form_data.get('nom_arrive')

        route, distance = calculate_distance(origin, destination)

        if route is not None:
            # Utiliser folium pour générer une carte interactive
            map_center = [(route[0][0] + route[-1][0]) / 2, (route[0][1] + route[-1][1]) / 2]
            m = folium.Map(location=map_center, zoom_start=12)

            # Ajouter les points de départ et d'arrivée à la carte
            folium.Marker(location=route[0], icon=folium.Icon(color='green')).add_to(m)
            folium.Marker(location=route[-1], icon=folium.Icon(color='red')).add_to(m)

            # Ajouter l'itinéraire à la carte en bleu
            folium.PolyLine(locations=route, color='blue').add_to(m)

            # Convertir la carte en HTML
            map_html = m._repr_html_()

            return render(request, 'result.html', {'distance': distance, 'map_html': map_html})
        else:
            # Gérer le cas où l'un ou les deux lieux n'ont pas pu être géocodés
            return render(request, 'error.html')

    return render(request, 'search.html')
