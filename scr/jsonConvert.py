from bs4 import BeautifulSoup
import unicodedata
import re
import json
import os

def convertToJSON(httpResponse, date):
    """Découpe la page pour récupéréer tous les évennements de la page

    Args:
        httpResponse (requests.Response): réponse d'une requête http récupérer par getPage()
        date (string): date identique que celle de getPage()

    Returns:
        [liste]: liste d'objets
    """
    jsonArr =[]

    soup = BeautifulSoup(httpResponse.content.decode('utf-8'), 'html.parser')
    content_div = soup.find('div', id = "content")
    event_div_Array = content_div.find_all('div', class_=(re.compile("^evt evt-")))

    for evt in event_div_Array:
        time = ''
        title = ''
        organe= ''
        desc= ''
        lieu = ''
        contact= ''

        try:
            time = evt.find('div', class_='time').get_text()
        except:
            pass

        try:
            title = evt.find('div', class_='titre').get_text()
        except:
            pass

        try:
            organe = evt.find('div', class_='organe').get_text()
        except:
            pass

        try:
            desc = evt.find('div', class_='objet').get_text()
        except:
            pass
        
        try:
            lieu = evt.find('div', class_='lieu').get_text()
        except:
            pass

        try:
            contact = evt.find('div', class_='contact').get_text()
        except:
            pass

        
        #Conditions sur chaque format d'heure (time) obtenu sur page (non-exhaustifs)

        if time.startswith('De') and ('et' in time): # ex "De 1 h 30 à 13 h 20 et de 14 h 50 à 16 heures"
            t = time.split('et')

            t1 = t[0]
            t1 = t1[3:].split('à')[0].split('h')

            
            t1[0] = unicodedata.normalize("NFKD", t1[0]).strip()
            if len(t1[0])==1:
                t1[0] = '0'+t1[0]

            t1[1] = unicodedata.normalize("NFKD", t1[1]).strip()

            t2 = t[1]
            t2 = t2[4:].split('à')[0].split('h')

            t2[0] = unicodedata.normalize("NFKD", t2[0]).strip()
            if len(t2[0])==1:
                t2[0] = '0'+t2[0]

            t2[1] = unicodedata.normalize("NFKD", t2[1]).strip()

            time = ['T'+t1[0]+':'+t1[1]+':00Z','T'+t2[0]+':'+t2[1]+':00Z']

            for t in time:
                jsonArr = jsonAppend(jsonArr ,date, t, title, organe, desc, lieu, contact)

        elif len(time)==5 or len(time)==4: #HHhmm ou Hhmm
            time = time.split('h')

            h = time[0]
            if len(h)==1:
                h= '0'+h
            time = 'T'+h+':'+ time[1]+':00Z'

            jsonArr = jsonAppend(jsonArr ,date, time, title, organe, desc, lieu, contact)

        elif time.startswith('De') and ('et' not in time): #ex 'De 16 h 30 à 18 heures'
            t = time[3:].split('à')[0].split('h')
            
            t[0] = unicodedata.normalize("NFKD", t[0]).strip()
            if len(t[0])==1:
                t[0] = '0'+t[0]

            t[1] = unicodedata.normalize("NFKD", t[1]).strip()

            time = 'T'+t[0]+':'+ t[1]+':00Z'

            jsonArr = jsonAppend(jsonArr ,date, time, title, organe, desc, lieu, contact)

        else:
            #time = ''
            jsonArr = jsonAppend(jsonArr ,date, time, title, organe, desc, lieu, contact)
        

        return jsonArr
    


def jsonAppend(jsonArr ,date, time, title, organe, desc, lieu, contact):
    """Ajoute un onjet dans la liste

    Args:
        jsonArr (liste): liste à agrandir 
        date (string): date
        time (string): horraire format: 'Thh:mm:ssZ"
        title (string): titre de l'évennement
        organe (string): organe concerné
        desc (string): description
        lieu (string): lieu
        contact (string)): contact.s

    Returns:
        [liste]: la liste complétée
    """
    jsonArr.append({
            'date': date[4:]+date[2]+date[3]+date[:2]+'T',
            'time': time,
            'title': unicodedata.normalize("NFKD",title),
            'organe':unicodedata.normalize("NFKD",organe.strip()),
            'desc': unicodedata.normalize("NFKD",desc),
            'lieu': unicodedata.normalize("NFKD",lieu),
            'contact': unicodedata.normalize("NFKD",contact)  
        })
    return jsonArr


def saveJSON(fileName, jsonArr):
    """
    Enregistrer le fichier JSON
    Args:
        fileName (string): nom du fichier
        jsonArr (liste): liste à enrigistrer en JSON
    """
    with open(fileName,'w', encoding='utf-8') as f:
        json.dump(jsonArr, f)


def jsonConvert(httpResponse ,date):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    jsonArr = convertToJSON(httpResponse, date)
    saveJSON(dir_path+'/../data/agenda.json',jsonArr)