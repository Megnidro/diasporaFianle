from collections import Counter

from django.shortcuts import render
from django.views.generic import TemplateView
import requests


# Create your views here.

class HomeCarteInfo(TemplateView):
    template_name = 'home/demandes/listes_des_demandes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Envoyer une requête GET à l'API
        response = requests.get('http://10.206.3.185:8081/carte-info')

        # Vérifier si la requête a réussi
        if response.status_code == 200:
            # Récupérer les données de la réponse
            data = response.json()
            context['data'] = data
        else:
            # Gérer les erreurs de requête
            context['error'] = 'Erreur lors de la récupération des données'
        return context

class tableCarteInfo(TemplateView):
    template_name = 'home/table.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Envoyer une requête GET à l'API
        response = requests.get('http://10.206.3.185:8081/carte-info')

        # Vérifier si la requête a réussi
        if response.status_code == 200:
            # Récupérer les données de la réponse
            data = response.json()
            context['data'] = data

            pays_counts = Counter(item['pays_residence'] for item in data)
            ville_counts = Counter(item['ville_residence'] for item in data)
            genre_counts = Counter(item['genre'] for item in data)
            categorie_pro_counts = Counter(item['categorie_pro'] for item in data)


            context['pays_counts'] = dict(pays_counts)
            context['ville_counts'] = dict(ville_counts)
            context['genre_counts'] = dict(genre_counts)
            context['categorie_pro_counts'] = dict(categorie_pro_counts)

        else:
            # Gérer les erreurs de requête
            context['error'] = 'Erreur lors de la récupération des données'
        return context



def get_data(request):
    url = 'http://10.206.3.185:8081/carte-info/info/npi'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data


def juridition_list(request):
    data = get_data(request)
    juridictions = []
    for juridiction_name, juridiction_data in data.items():
        total = juridiction_data['total']
        npi = juridiction_data['NPI']
        not_npi = juridiction_data['NOT_NPI']
        juridictions.append({
            'name': juridiction_name
            , 'total': total
            , 'npi': npi
            , 'not_npi': not_npi,
            'detail_data': juridiction_data
        })
    context = {
        'juridictions': juridictions
    }
    return render(request, 'home/juridiction/liste_juridiction_final.html', context)


def get_detail_juridiction(request, juridiction_name):
    # Récupérer les données générales
    data = get_data(request)

    # Récupérer les données spécifiques à la juridiction
    juridiction_data = data.get(juridiction_name)

    if juridiction_data is not None:
        context = {
            'juridiction_name': juridiction_name,
            'juridiction_data': juridiction_data  # Passer les données à votre modèle HTML
        }
        return render(request, 'home/juridiction/liste_juridiction_detail.html', context)

"""
class ReportCarteInfoJuridction(TemplateView):
    template_name = 'home/listes_des_juridictions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        response = requests.get('http://10.206.3.185:8081/carte-info/info/npi')
        if response.status_code == 200:
            data = response.json()
            context['data'] = data
            print(data)
        else:
            context['error'] = 'Erreur lors de la récuperation'
        return context"""
