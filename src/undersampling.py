# López Reyes José Roberto
# Parte 3: Undersampling de clase Positiva

# Hay demasiadas clases positivas, balanceamos el dataset

import pandas as pd
from sklearn.utils import shuffle

# Cargar dataset maestro
df = pd.read_csv('../data/processed/steam_reviews_maestro.csv')

# Separar por clases
df_pos = df[df['voted_up'] == True]
df_neg = df[df['voted_up'] == False]

print(f"Positivas originales: {len(df_pos)}")
print(f"Negativas originales: {len(df_neg)}")

# Undersampling
df_pos_balanced = df_pos.sample(n=len(df_neg), random_state=42)

# Unir y mezclar
df_balanced = pd.concat([df_pos_balanced, df_neg])
df_balanced = shuffle(df_balanced, random_state=42)

print("\n--- NUEVO BALANCE ---")
print(df_balanced['voted_up'].value_counts())

# Guardar el dataset listo para entrenar
df_balanced.to_csv('../data/processed/steam_reviews_balanced.csv', index=False)
print("✅ Dataset balanceado guardado como 'steam_reviews_balanced.csv'")
