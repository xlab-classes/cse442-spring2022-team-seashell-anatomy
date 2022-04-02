import requests

def get_songs_by_year(year, limit=None):
    url = f'https://api.spotify.com/v1/search?q=year%3D{year}&type=track'
    if limit:
        url += f'&limit={limit}'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer BQCvCJag29HUdPYou8VxiVYNWZODep8s0qmwGAhZ29WSmJYP4KkHBbY_AN6Y4hugKQb49Ewlfq75N2JfXei9lJ8H8oF7lDqEgrBUHsltBmZAyfwkgT8DzDocdTXNZaE8vjtAsbLvfA2tQ1DtPPA6QUmOONmYUwJnG3c'
    }
    response = requests.get(url, headers=headers)
    json_response = response.json()
    tracks = json_response['tracks']
    next = tracks['next']
    items = tracks['items']

    while tracks:
        response = requests.get(next, headers=headers)
        json_response = response.json()
        print(json_response)
        if 'tracks' not in json_response:
            break
        tracks = json_response['tracks']
        next = tracks['next']
        items += tracks['items']
 
    print(len(items))
    return tracks



def get_songs(n):
    while n > 0:
        songs = get_songs_by_year(2022, 1_000)


if __name__ == '__main__':
    get_songs_by_year(2021)
