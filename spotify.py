from dotenv import load_dotenv
import os
import base64
import requests
from requests import post
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
token = os.getenv("TOKEN")


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    print(json_result)
    token = json_result["access_token"]
    return token

def get_header():
    return {"Authorization": "Bearer " + token}

def artist(artist_name):
    header = get_header()
    query_url = f"https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1"
    result = requests.get(query_url, headers=header)
    json_result = json.loads(result.content)
    return json_result['artists']['items'][0]['id']

def info_id(artistsid, req):
    header = get_header()
    url = f"https://api.spotify.com/v1/artists/{artistsid}"
    result = requests.get(url, headers = header)
    json_result = json.loads(result.content)
    if req == "followers":
        return json_result["followers"]["total"]
    else:
        return json_result[req]

def album(artistsid, token):
    header = get_header(token)
    url = f"https://api.spotify.com/v1/artists{artistsid}/albums"
    result = requests.get(url, headers = header)
    json_result = json.loads(result.content)
    res = []
    for i in range(len(json_result['items'])):
        res.append(tuple([json_result['items'][i]['name'], json_result['items'][i]['release_date']]))
    return res

def top_songs(artistsid, token):
    header = get_header(token)
    url = f"https://api.spotify.com/v1/artists{artistsid}/top-tracks?country=UA&limit=1"
    result = requests.get(url, headers = header)
    json_result = json.loads(result.content)
    res = []
    for i in range(len(json_result['tracks'])):
        res.append(json_result['track'][i]['name'])
    return res

if __name__ == "__main__":
    artist = input("Enter the name of an artist:")
    token = get_token()
    artistsid = artist(artist, token)
    list_of_answers = ['genres', 'popularity', 'followers', 'id', 'top-tracks', 'albums']
    print(['genres', 'popularity', 'followers', 'id', 'top-tracks', 'albums'])
    req = input("What would you like to know about the artist?")
    while req not in list_of_answers:
        print(['genres', 'popularity', 'followers', 'id', 'top-tracks', 'albums'])
        req = input("What would you like to know about the artist?")
    if req in ['genres', 'popularity', 'followers', 'id']:
        print(info_id(artistsid, token, req))
    elif req == 'albums':
        for i in album(artistsid, token):
            print(f'Albu name is-{i[0]}, release date of the album: {i[1]}')
    elif req == 'top-tracks':
        for i in range(len(top_songs(artistsid, token))):
            print(f'{i+1}. {top_songs(artistsid, token)[i]}')









# artistsid = get_artist("Eminem")
# info = get_info_id(artistsid, "followers")
# print(info)

