import requests
from django.views.generic import TemplateView
from django.shortcuts import render

from . import utils


class HomeView(TemplateView):
    template_name = 'home/accueil/accueil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Récupérer les données de la première API
        carte_info = utils.fetch_carte_info()
        if carte_info:
            context['carte_info'] = carte_info
            context.update(self.process_carte_info(carte_info))
        else:
            context = self.handle_api_error(context)

        # Récupérer les données de la deuxième API
        npi_info = utils.fetch_carte_info_npi()
        if npi_info:
            context['npi_info'] = npi_info
        else:
            context = self.handle_api_error(context)

        return context

    def process_carte_info(self, data):
        total_personnes = 0
        total_npi = 0
        total_not_npi = 0

        for personne in data:
            total_personnes += 1
            if personne['npi'] is not None:
                total_npi += 1
            else:
                total_not_npi += 1

        return {
            'total_personnes': total_personnes,
            'total_npi': total_npi,
            'total_not_npi': total_not_npi
        }


    def handle_api_error(self, context):
        # Gérer les erreurs de requête
        # Vous pouvez personnaliser cette méthode pour gérer les erreurs d'API spécifiques
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
    return render(request, 'home/accueil/accueil.html', context)




