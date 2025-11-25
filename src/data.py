# López Reyes José Roberto
# Parte 1: Obtención de datos

import requests
import pandas as pd
import time
import urllib.parse

# --- LISTA EXTENDIDA Y BALANCEADA ---
GAMES = [
    # --- LOS AMADOS (Positivas / Overwhelmingly Positive) ---
    ("Terraria", 105600),  # El estándar de oro de reseñas positivas
    ("Stardew Valley", 413150),  # Nadie odia este juego
    ("Left 4 Dead 2", 550),  # Clásico atemporal
    ("Hollow Knight", 367520),  # Indie perfecto
    ("Resident Evil 4", 2050650),  # (Remake) Muy aclamado

    # --- LOS POLÉMICOS / MIXTOS (Mixed / Variadas) ---
    # Estos son ORO para NLP porque el lenguaje es complejo y matizado.
    ("Starfield", 1716740),  # Muy divisivo (aburrido vs expansivo)
    ("PUBG: BATTLEGROUNDS", 578080),  # Aman el juego, odian los hackers/bugs
    ("Dead by Daylight", 381210),  # Relación amor-odio tóxica de la comunidad
    ("Rust", 252490),  # Comunidad tóxica, lenguaje agresivo
    ("Call of Duty HQ", 1938090),  # Siempre tienen reseñas mixtas

    # --- LOS CASTIGADOS (Negativas / Mayormente Negativas) ---
    # Necesitamos palabras como "refund", "crash", "scam", "greedy".
    ("Overwatch 2", 2357570),  # Fue bombardeado con negativas (perfecto para esto)
    ("NBA 2K24", 2338770),  # Odiado por microtransacciones
    ("Battlefield 2042", 1517290),  # Lanzamiento desastroso
    ("Redfall", 1294810),  # Considerado muy malo técnicamente
    ("Mortal Kombat 1", 1971870),  # Recientes quejas por monetización
]

MAX_REVIEWS_PER_GAME = 5000
REVIEWS_PER_REQUEST = 100


# Función para obtener las reseñas
def get_reviews(app_id, game_name):
    reviews_data = []
    cursor = '*'  # El cursor inicial es un asterisco

    print(f"--- Iniciando descarga para: {game_name} ({app_id}) ---")

    while len(reviews_data) < MAX_REVIEWS_PER_GAME:
        try:
            # Encoding del cursor para que viaje bien en la URL
            encoded_cursor = urllib.parse.quote(cursor)

            url = (f"https://store.steampowered.com/appreviews/{app_id}"
                   f"?json=1&filter=recent&language=english&num_per_page={REVIEWS_PER_REQUEST}"
                   f"&cursor={encoded_cursor}&purchase_type=all")

            response = requests.get(url)

            if response.status_code != 200:
                print(f"Error {response.status_code}. Reintentando en 5 seg...")
                time.sleep(5)
                continue

            data = response.json()

            # Validación: ¿Hay reviews?
            if 'reviews' not in data or not data['reviews']:
                print("No hay más reviews disponibles.")
                break

            # Validar si el cursor no cambió (loop infinito de Steam)
            if 'cursor' in data:
                new_cursor = data['cursor']
                if new_cursor == cursor:
                    print("Se alcanzó el final de la paginación.")
                    break
                cursor = new_cursor
            else:
                break

            # Guardar data útil
            for review in data['reviews']:
                reviews_data.append({
                    'game_name': game_name,
                    'app_id': app_id,
                    'review_id': review['recommendationid'],
                    'review_text': review['review'],
                    'voted_up': review['voted_up'],  # True=Positivo, False=Negativo
                    'votes_up': review['votes_up'],  # Cuánta gente le dio like a la review
                    'playtime_forever': review['author']['playtime_forever']  # Minutos jugados
                })

            print(f"Bajadas: {len(reviews_data)} / {MAX_REVIEWS_PER_GAME}")

            # DESCANSO PARA NO SER BANEADO (IMPORTANTE)
            time.sleep(1.5)

        except Exception as e:
            print(f"Error inesperado: {e}")
            break

    # Guardar en CSV individual
    if reviews_data:
        df = pd.DataFrame(reviews_data)
        filename = f"reviews_{game_name.replace(' ', '_')}.csv"
        df.to_csv(filename, index=False)
        print(f"✅ Guardado: {filename} con {len(df)} reseñas.\n")
    else:
        print(f"⚠️ No se bajó nada para {game_name}.\n")


# --- EJECUCIÓN DEL BUCLE MAESTRO ---
if __name__ == "__main__":
    print("Iniciando la cosecha de datos... 🚜\n")
    for name, app_id in GAMES:
        get_reviews(app_id, name)
    print("¡Proceso terminado! Revisa tus archivos CSV.")
