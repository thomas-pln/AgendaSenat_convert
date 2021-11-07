import requests
import sys
from jsonConvert import jsonConvert

def getPage(date):
    """Récupère la page de l'ordre du jour du Sénat à la date donnée

    Args:
        date (string): date format: 'jjmmaaaa'

    Returns:
        [requests.Response]: réponse à la requête avec l'URL (contenu html: requests.get(url).content) 
    """
    url = 'https://www.senat.fr/aglae/Global/agl'+date+'.html'
    #print(url)
    return requests.get(url)



if len(sys.argv)>1:
    jsonConvert(getPage(sys.argv[1]), sys.argv[1])
