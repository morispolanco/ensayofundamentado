import streamlit as st
import requests
import json

# Configuración de la página de Streamlit
st.set_page_config(page_title="Generador de Ensayos", page_icon="📝", layout="wide")

# Título de la aplicación
st.title("Generador de Ensayos con Citas")

# Entrada de la tesis
thesis = st.text_area("Ingrese la tesis para el ensayo:", height=100)

# Botón para generar el ensayo
if st.button("Generar Ensayo"):
    if thesis:
        # Acceder a la API key desde los secretos de Streamlit
        api_key = st.secrets["TOGETHER_API_KEY"]
        
        # URL de la API de Together
        url = "https://api.together.xyz/v1/completions"
        
        # Headers para la solicitud
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Prompt para el modelo
        prompt = f"""Escribe un ensayo largo y detallado sobre la siguiente tesis:

{thesis}

El ensayo debe incluir:
1. Una introducción que presente la tesis.
2. Al menos 3 argumentos principales que apoyen la tesis.
3. 15 citas relevantes de autores reconocidos en el campo.
4. Una conclusión que resuma los puntos principales y reafirme la tesis.

Asegúrate de que el ensayo esté bien estructurado, con transiciones suaves entre las secciones y un flujo lógico de ideas."""

        # Datos para la solicitud
        data = {
            "model": "mistral-7b-instruct-v0.1",
            "prompt": prompt,
            "max_tokens": 2048,
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50,
            "repetition_penalty": 1,
            "stop": ["<human>", "<assistant>"]
        }
        
        # Realizar la solicitud a la API
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            essay = response.json()['choices'][0]['text']
            
            # Mostrar el ensayo generado
            st.subheader("Ensayo Generado:")
            st.markdown(essay)
        except requests.exceptions.RequestException as e:
            st.error(f"Error al generar el ensayo: {e}")
            if response.text:
                st.error(f"Respuesta de la API: {response.text}")
    else:
        st.warning("Por favor, ingrese una tesis antes de generar el ensayo.")

# Instrucciones de uso
st.sidebar.header("Instrucciones")
st.sidebar.write("""
1. Ingrese la tesis para su ensayo en el campo de texto.
2. Haga clic en el botón "Generar Ensayo".
3. El ensayo generado aparecerá debajo del botón.
4. El ensayo incluirá una introducción, argumentos principales, 15 citas relevantes y una conclusión.
""")

# Nota sobre la API key
st.sidebar.info("Nota: La API key está segura en los secretos de Streamlit.")
