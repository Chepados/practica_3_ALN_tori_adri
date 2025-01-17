import pandas as pd
import requests
import time
import tqdm

from get_chord_progressions import my_key


def get_songs(auth_key, limit_page=10):
    songs_url_endpoint = f"https://api.hooktheory.com/v1/trends/songs"

    headers = {
        "Authorization": f"Bearer {auth_key}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    four_chord_progressions_df = pd.read_csv("four_chord_progressions.csv")

    progressions = four_chord_progressions_df["child_path"].tolist()

    songs_df = pd.DataFrame()

    for progression in tqdm.tqdm(progressions):
        page = 1
        while page <= limit_page:
            songs_url = f"{songs_url_endpoint}?cp={progression}&page={page}"
            time.sleep(1.5)
            songs_response = requests.get(songs_url, headers=headers)

            if songs_response.status_code == 200:
                songs_json = songs_response.json()
            elif songs_response.status_code == 500:
                time.sleep(3)
                print("Error del servidor")
                break
            else:
                raise Exception(f"Error al obtener canciones: {songs_response.status_code} - {songs_response.text}")

            if songs_response:

                songs_by_progression_df = pd.DataFrame(songs_json)
                songs_by_progression_df["progression"] = progression
                songs_df = pd.concat([songs_df, songs_by_progression_df], ignore_index=True)

            page += 1

        time.sleep(2)
        songs_df.to_csv("songs_df.csv", index=False)

my_key = "e02a2d8962a0c70fc763994e9fb41f02"
get_songs(my_key)

"""
def get_songs_by_progression(auth_key, progression):
    songs_url = f"https://api.hooktheory.com/v1/trends/songs?cp={progression}"

    headers = {
        "Authorization": f"Bearer {auth_key}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    songs_data = []
    page = 1

    while page <= 5:
        # Añadimos paginación en caso de que haya muchas canciones
        response = requests.get(songs_url + f"&page={page}", headers=headers)

        if response.status_code != 200:
            raise Exception(f"Error al obtener canciones: {response.status_code} - {response.text}")

        songs = response.json()

        if not songs:
            break  # Salimos si no hay más canciones en la siguiente página

        # Agregamos cada canción a nuestra lista
        for song in songs:
            songs_data.append({
                "artist": song["artist"],
                "song": song["song"],
                "section": song["section"],
                "url": song["url"],
                "progression": progression
            })

        time.sleep(1)
        page += 1  # Avanzamos a la siguiente página

    return songs_data


get_songs_by_progression(my_key, "4,1")"""