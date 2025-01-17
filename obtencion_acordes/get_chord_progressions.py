import requests
import time
import pandas as pd


#Necesitamos una clave de Autentificación para conectarnos a la API de Hooktheory
def get_auth_key(username, password):
    auth_url = "https://api.hooktheory.com/v1/users/auth"
    auth_data = {
        "username": username,
        "password": password
    }

    # Solicitar token de autenticación
    auth_response = requests.post(auth_url, json=auth_data)

    if auth_response.status_code == 200:
        return auth_response.json()["activkey"]
    else:
        raise Exception(f"Error en la autenticación: {auth_response.status_code} - {auth_response.text}")

my_key = get_auth_key("ivantoribio", "MusicIsForEveryone12")

print(my_key)


def get_one_chord_progression(auth_key):
    chords_url = "https://api.hooktheory.com/v1/trends/nodes"

    headers = {
        "Authorization": f"Bearer {auth_key}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    chords_response = requests.get(chords_url, headers=headers)

    if chords_response.status_code == 200:
        chords_json = chords_response.json()

    else:
        raise Exception(f"Error al obtener acordes: {chords_response.status_code} - {chords_response.text}")

    one_chord_progressions_df = pd.DataFrame(chords_json)

    #Filtramos aquellos acordes que no aportan tanta información porque se utilizan muy pocas veces
    one_chord_progressions_df = one_chord_progressions_df[one_chord_progressions_df["probability"] > 0.03]

    one_chord_progressions_df.to_csv("one_chord_progressions.csv", index=False)

get_one_chord_progression(my_key)

def get_two_chord_progression(auth_key):
    chords_url = "https://api.hooktheory.com/v1/trends/nodes"

    headers = {
        "Authorization": f"Bearer {auth_key}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    one_chord_progressions_df = pd.read_csv("one_chord_progressions.csv")

    two_chord_progressions_df = pd.DataFrame(columns=one_chord_progressions_df.columns)

    for cp in one_chord_progressions_df["child_path"].tolist():
        child_path_url = chords_url + "?cp=" + str(cp)
        chords_response = requests.get(child_path_url, headers=headers)
        if chords_response.status_code == 200:
            chords_json = chords_response.json()
        else:
            raise Exception(f"Error al obtener acordes: {chords_response.status_code} - {chords_response.text}")

        two_chord_progressions_df = pd.concat([two_chord_progressions_df, pd.DataFrame(chords_json)])

    two_chord_progressions_df = (two_chord_progressions_df[two_chord_progressions_df["probability"] > 0.03].reset_index(drop=True))

    two_chord_progressions_df.to_csv("two_chord_progressions.csv", index=False)


def get_three_chord_progression(auth_key):
    chords_url = "https://api.hooktheory.com/v1/trends/nodes"
    headers = {"Authorization": f"Bearer {auth_key}",
               "Accept": "application/json",
               "Content-Type": "application/json"}

    two_chord_progressions_df = pd.read_csv("two_chord_progressions.csv")

    three_chord_progressions_df = pd.DataFrame(columns=two_chord_progressions_df.columns)

    for cp in two_chord_progressions_df["child_path"].tolist():
        child_path_url = chords_url + "?cp=" + str(cp)
        chords_response = requests.get(child_path_url, headers=headers)
        if chords_response.status_code == 200:
            chords_json = chords_response.json()
        else:
            raise Exception(f"Error al obtener acordes: {chords_response.status_code} - {chords_response.text}")

        three_chord_progressions_df = pd.concat([three_chord_progressions_df, pd.DataFrame(chords_json)])

        three_chord_progressions_df = three_chord_progressions_df[
            three_chord_progressions_df["probability"] > 0.03].reset_index(drop=True)

        three_chord_progressions_df.to_csv("three_chord_progressions.csv", index=False)


#get_three_chord_progression(my_key)


def get_n_chord_progression(n: int, auth_key: str, threshold: float) -> None:
    assert 2 <= n <= 4, "Solo se permiten progresiones de hasta 4 acordes"

    get_one_chord_progression(auth_key)

    matches = {1: "one_chord_progressions.csv", 2 : "two_chord_progressions.csv", 3 : "three_chord_progressions.csv", 4 : "four_chord_progressions.csv"}

    chords_url = "https://api.hooktheory.com/v1/trends/nodes"
    headers = {"Authorization": f"Bearer {auth_key}",
               "Accept": "application/json",
               "Content-Type": "application/json"}

    before_chord_progressions_df = pd.read_csv(matches[n-1])

    n_chord_progressions_df = pd.DataFrame(columns=["chord_ID", "chord_HTML", "probability", "child_path"])

    for cp in before_chord_progressions_df["child_path"].tolist():
        child_path_url = chords_url + "?cp=" + str(cp)
        chords_response = requests.get(child_path_url, headers=headers)
        time.sleep(1)
        if chords_response.status_code == 200:
            chords_json = chords_response.json()
        else:
            raise Exception(f"Error al obtener acordes: {chords_response.status_code} - {chords_response.text}")

        n_chord_progressions_df = pd.concat([n_chord_progressions_df, pd.DataFrame(chords_json)])

        n_chord_progressions_df = n_chord_progressions_df[
            n_chord_progressions_df["probability"] > threshold].reset_index(drop=True)

        n_chord_progressions_df.to_csv(matches[n], index=False)


#get_n_chord_progression(4, my_key, 0.03)
