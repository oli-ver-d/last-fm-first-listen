import requests
import pprint
import os
from dotenv import load_dotenv

load_dotenv()
root_url = "http://ws.audioscrobbler.com/2.0/"
api_key = os.getenv("API_KEY")

def main():
    print("Artist to search for: ")
    artist = input()

    print("User: ")
    user = input()
    
    init_response = query_page(1, 1, user)
    init_dict = init_response.json()
    total_pages = int(init_dict["recenttracks"]['@attr']['totalPages'])
    search_pages(total_pages, artist, user)


def search_pages(total_pages: int, artist: str, user: str):
    for i in range(total_pages, 0, -1):
        print(f"Querying page {(total_pages - i) + 1}/{total_pages}")
        response = query_page(i, 200, user)
        response_dict = response.json()
        tracks = sorted(response_dict['recenttracks']['track'], key=lambda x: x['date']['uts'])
        for track in tracks:
            track_artist = track["artist"]["#text"] 
            if track_artist.lower() == artist.lower():
                print(f"Artist {artist} found at {track['date']['#text']}")
                print(f"Track streamed: {track["name"]}")
                return


def query_page(page_number: int, limit: int, user: str) -> requests.Response:
    method = "user.getrecenttracks"
    limit = 200 # max limit
    query_url = f"{root_url}?method={method}&user={user}&api_key={api_key}&format=json&page={page_number}&limit={limit}"
    response = requests.get(query_url)
    print(response.status_code)
    if response.status_code != 200:
        pprint.pp(response.json())
    return response
    

if __name__ == "__main__":
    main()
