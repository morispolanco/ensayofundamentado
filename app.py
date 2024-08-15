import streamlit as st
import requests
import json

# Configuración de la página de Streamlit
st.set_page_config(page_title="Generador de Ensayos", page_icon="📝", layout="wide")

# Título de la aplicación
st.title("Generador de Ensayos con Citas Integradas")

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
        
        # Prompt mejorado para el modelo
        prompt = f"""Escribe un ensayo académico detallado y bien estructurado sobre la siguiente tesis:

{thesis}

Instrucciones para el ensayo:

1. Comienza con una introducción que presente la tesis de manera clara y atractiva.

2. Desarrolla el cuerpo del ensayo con múltiples párrafos que apoyen la tesis. Cada párrafo debe presentar un argumento o idea principal que respalde la tesis.

3. Integra naturalmente 15 citas relevantes de autores reconocidos a lo largo del texto. Las citas deben reforzar los argumentos y estar bien contextualizadas.

4. Asegúrate de que haya transiciones suaves y lógicas entre los párrafos, creando un flujo coherente de ideas.

5. Concluye el ensayo resumiendo los puntos principales y reafirmando la tesis de manera convincente.

6. El estilo de escritura debe ser académico, pero accesible, evitando jerga innecesaria.

7. No uses subtítulos ni numeración explícita de argumentos. El ensayo debe fluir como un texto continuo y cohesivo.

Genera un ensayo que cumpla con estas instrucciones, manteniendo un tono académico y una estructura coherente a lo largo del texto."""

        # Datos para la solicitud
        data = {
            "model": "togethercomputer/llama-2-70b-chat",
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
4. El ensayo incluirá una introducción, argumentos bien desarrollados con citas integradas, y una conclusión.
""")

# Nota sobre la API key
st.sidebar.info("Nota: La API key está segura en los secretos de Streamlit.")
