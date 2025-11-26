# López Reyes José Roberto
# Parte 4: Filtrado de reseñas en inglés

import pandas as pd
from langdetect import detect, DetectorFactory

# Para obtener resultados consistentes
DetectorFactory.seed = 0


def es_ingles(texto):
    """
    Retorna True si el texto es detectado como Inglés.
    Retorna False si es otro idioma o si falla la detección.
    """
    try:
        # Si el texto es muy corto (ej: "GG"), langdetect puede fallar
        if len(texto) < 5:
            return True

        return detect(texto) == 'en'
    except:
        return False


# Cargar dataset
df = pd.read_csv('../data/processed/steam_reviews_balanced.csv')

print(f"Total antes de filtrar idiomas: {len(df)}")

# Aplicar el filtro
print("Detectando idiomas... (Paciencia, está leyendo cada review)")
df['is_english'] = df['review_text'].apply(es_ingles)

# Ver cuántos "impostores" encontramos
impostores = len(df[df['is_english'] == False])
print(f"--- Se encontraron {impostores} reseñas en otros idiomas ---")

# Quedarnos solo con Inglés
df_clean_lang = df[df['is_english'] == True].drop(columns=['is_english'])

print(f"Total final en Inglés puro: {len(df_clean_lang)}")

# Guardar
df_clean_lang.to_csv('../data/processed/steam_reviews_english_only.csv', index=False)
print("✅ Guardado: steam_reviews_english_only.csv")
