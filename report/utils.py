import requests
from django.conf import settings
from django.core.cache import cache


def fetch_api_data(endpoint, params=None, timeout=5, cache_key=None, cache_timeout=300):
    """
    Fonction générique pour récupérer des données d'API avec mise en cache.
    """
    base_url = settings.API_BASE_URL
    url = f"{base_url}/{endpoint}"

    if cache_key and cache.get(cache_key):
        return cache.get(cache_key)

    try:
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        if cache_key:
            cache.set(cache_key, data, cache_timeout)
        return data
    except requests.RequestException as e:
        # Log l'erreur
        return None


def fetch_carte_info():
    return fetch_api_data('/carte-info/', cache_key='carte_info_data')


def fetch_carte_info_npi():
    return fetch_api_data('/carte-info/info/npi', cache_key='autre_info_data')
