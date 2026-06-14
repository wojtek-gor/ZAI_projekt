import requests
import xml.etree.ElementTree as ET
import time

BGG_URL = "https://boardgamegeek.com/xmlapi2/"
TOKEN = "45d82bef-3eb2-4ba6-878e-03b1aef87094"

def pobieranie_bgg_games(lista_id):
    zap = ",".join(map(str, lista_id))
    url = f"{BGG_URL}thing?id={zap}"
    naglowek = {
        "Authorization": f"Bearer {TOKEN}"
    }
    response = requests.get(url, headers=naglowek)
    while response.status_code == 202:
        time.sleep(3)
        response = requests.get(url)

    if response.status_code != 200:
        return []

    root = ET.fromstring(response.content)
    pobrane_gry = []

    for item in root.findall('item'):
        bgg_id = int(item.get('id'))

        tytul_szukany = item.find("name[@type='primary']")
        tytul = tytul_szukany.get('value') if tytul_szukany is not None else "Nieznany tytuł"
        min_graczy = int(item.find('minplayers').get('value')) if item.find('minplayers') is not None else None
        max_graczy = int(item.find('maxplayers').get('value')) if item.find('maxplayers') is not None else None
        czas_gry = int(item.find('playingtime').get('value')) if item.find('playingtime') is not None else None
        opis = item.find('description').text if item.find('description') is not None else None
        rok = int(item.find('yearpublished').get('value')) if item.find(
            'yearpublished') is not None else None

        pobrane_gry.append({
            'bgg_id': bgg_id,
            'tytul': tytul,
            'min_graczy': min_graczy,
            'max_graczy': max_graczy,
            'czas_gry': czas_gry,
            'opis': opis,
            'publikacja': rok
        })

    return pobrane_gry


def szukaj_po_nazwie_bgg(nazwa):
    url = f"{BGG_URL}search"
    naglowek = {
        "Authorization": f"Bearer {TOKEN}"
    }
    skladowe = {
        "query": nazwa,
        "type": "boardgame",
    }
    zwrot = requests.get(url, headers=naglowek, params=skladowe)

    if zwrot.status_code != 200:
        return []

    root = ET.fromstring(zwrot.content)
    bgg_ids = []

    for item in root.findall('item')[:3]:
        name_node = item.find("name")
        tytul = name_node.get('value') if name_node is not None else "Nieznany tytuł"
        bgg_id = int(item.get('id'))
        bgg_ids.append({
            "bgg_id": bgg_id,
            "tytul": tytul
        })

    return bgg_ids