import streamlit as st
import joblib
import os
import pandas as pd

# Limpieza de reseñas
try:
    from src.final_data import limpiar_resena
except ImportError:
    st.error("⚠️ Error: No se encuentra 'src/preprocessing.py'. Verifica tu estructura de carpetas.")
    st.stop()

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Steam Sentinel AI",
    page_icon="🎮",
    layout="centered",  # 'centered' o 'wide'
    initial_sidebar_state="collapsed"
)

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
<style>
    .stTextArea textarea {
        background-color: #1b2838; /* Color de fondo de Steam */
        color: #c7d5e0; /* Color de texto de Steam */
        border-radius: 10px;
        border: 1px solid #2a475e;
    }
    .stApp {
        background-color: #0f1922; /* Fondo general oscuro */
        color: white;
    }
    h1 {
        color: #66c0f4; /* Azul Steam */
        text-align: center;
    }
    .prediction-text {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .positive { color: #66c0f4; }
    .negative { color: #ff4c4c; }
</style>
""", unsafe_allow_html=True)


# Carga del modelo
@st.cache_resource
def load_model():
    path = 'model/model.pkl'
    if not os.path.exists(path):
        st.error(f"⚠️ Error: No se encuentra el archivo '{path}'.")
        st.stop()
    return joblib.load(path)


# Cargar el cerebro
pipeline = load_model()

# Imágenes de clasificación
img_like = "assets/like.png"
img_dislike = "assets/dislike.png"
img_wait = "assets/waiting.png"

# Interfaz Principal
st.title("🎮 Steam Sentinel AI")
st.write("Escribe tu reseña (en inglés) y ve cómo la IA detecta tu furia o tu amor en tiempo real.")

# Usamos columnas para organizar el layout
col1, col2 = st.columns([2, 1])

with col1:
    # Área de texto
    user_input = st.text_area("Tu reseña:", height=200, placeholder="Ej: Best game ever, totally addicted!")

with col2:
    st.write("")
    st.write("")

    # LÓGICA DE PREDICCIÓN
    if user_input:
        # Limpiar el texto usando
        cleaned_text = limpiar_resena(user_input)

        # Verificar que quedó algo de texto después de limpiar
        if len(cleaned_text.strip()) == 0:
            st.warning("🤔 Escribe algo con palabras en inglés.")
            st.image("https://i.imgur.com/y23T32h.png", width=200)

        else:
            # Predecir
            prediction = pipeline.predict([cleaned_text])[0]  # True (Pos) o False (Neg)
            proba = pipeline.predict_proba([cleaned_text])[0]  # [Prob_Neg, Prob_Pos]

            # Mostrar resultados
            if prediction == True:
                confidence = proba[1]
                st.markdown(f'<p class="prediction-text positive">👍 POSITIVA ({confidence:.1%})</p>',
                            unsafe_allow_html=True)
                st.image(
                    "https://community.akamai.steamstatic.com/public/shared/images/userreviews/icon_thumbsUp_v6.png",
                    width=200)

            else:
                confidence = proba[0]
                st.markdown(f'<p class="prediction-text negative">👎 NEGATIVA ({confidence:.1%})</p>',
                            unsafe_allow_html=True)
                st.image(
                    "https://community.akamai.steamstatic.com/public/shared/images/userreviews/icon_thumbsDown_v6.png",
                    width=200)
    else:
        # Estado inicial
        st.info("👈 Esperando reseña...")
        st.image("https://i.imgur.com/y23T32h.png", width=200, caption="La IA está durmiendo...")

# Footer
st.divider()
st.caption("Proyecto de NLP - Steam Sentiment Analysis. Modelo: Logistic Regression (Accuracy ~87%).")
