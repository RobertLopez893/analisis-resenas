# López Reyes José Roberto
# Parte 2: Unión de los datasets

import pandas as pd
import glob

# Buscar todos los archivos csv en la carpeta data
archivos = glob.glob('../data/raw/reviews_*.csv')

print(f"Se encontraron {len(archivos)} archivos para unir.")

# Lee cada uno y agrégalo a una lista
lista_dfs = []
for archivo in archivos:
    try:
        df_temp = pd.read_csv(archivo)
        lista_dfs.append(df_temp)
        print(f"-> Cargado: {archivo} ({len(df_temp)} filas)")
    except Exception as e:
        print(f"Error leyendo {archivo}: {e}")

# Concatena (une) todos en un solo DataFrame gigante
if lista_dfs:
    dataset_maestro = pd.concat(lista_dfs, ignore_index=True)

    print("\n" + "=" * 40)
    print(f"TOTAL DE RESEÑAS RECOLECTADAS: {len(dataset_maestro)}")
    print("=" * 40)

    # Vistazo rápido al balance de clases
    print("\nDistribución de Sentimiento (True=Positivo, False=Negativo):")
    print(dataset_maestro['voted_up'].value_counts())

    # Guardar el archivo maestro
    dataset_maestro.to_csv('../data/processed/steam_reviews_maestro.csv', index=False)
    print("\n✅ Guardado exitosamente como 'steam_reviews_maestro.csv'")
else:
    print("No se encontraron dataframes para unir.")
