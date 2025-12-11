import pandas as pd
import re
from sklearn.utils import shuffle
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Preparar herramientas
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
# Protegemos las negaciones para que el modelo aprenda el sentimiento inverso
negations = {'no', 'not', 'nor', "didn't", "isn't", "wasn't", "aren't", "won't", "don't"}
stop_words = stop_words - negations


def limpiar_resena(texto):
    if not isinstance(texto, str):
        return ""

    texto = texto.lower()
    # Quitar BBCode de Steam ([b], [url], etc) y URLs
    texto = re.sub(r'\[.*?\]', '', texto)
    texto = re.sub(r'http\S+|www\.\S+', '', texto)

    # Dejar SOLO letras (Quitamos números y puntuación)
    texto = re.sub(r'[^a-z\s]', '', texto)

    # Tokenización y Limpieza
    palabras = texto.split()

    palabras_limpias = [
        lemmatizer.lemmatize(word)
        for word in palabras
        if word not in stop_words and len(word) > 2
    ]

    return " ".join(palabras_limpias)


# Carga del dataset con solo inglés
df = pd.read_csv('data/processed/steam_reviews_english_only.csv')

# Feature Selection
df = df[['review_text', 'voted_up']]

# Separar por clases para re-balancear
df_pos = df[df['voted_up'] == True]
df_neg = df[df['voted_up'] == False]

# Balanceo de la clase positiva
n_muestras = len(df_pos)
print(f"La clase más pequeña tiene {n_muestras} muestras. Re-balanceando...")

# Undersampling
df_neg_balanced = df_neg.sample(n=n_muestras, random_state=42)

# Unir y mezclar
df_balanced = pd.concat([df_pos, df_neg_balanced])
df_balanced = shuffle(df_balanced, random_state=42)

print("\n--- Balance Final 50/50 ---")
print(df_balanced['voted_up'].value_counts())
print(f"Total de reseñas limpias a procesar: {len(df_balanced)}")

# Limpieza del texto
print("\nLimpiando y Normalizando reseñas... ⏳")
df_balanced['review_clean'] = df_balanced['review_text'].apply(limpiar_resena)

# Último chequeo de nulos
df_final = df_balanced[['review_clean', 'voted_up']]
df_final = df_final[df_final['review_clean'].str.len() > 0]

# Guardar el dataset final
df_final.to_csv('data/final/final_data.csv', index=False)

print(f"Dataset guardado como 'final_data.csv' con {len(df_final)} filas.")
