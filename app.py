import streamlit as st
import requests
import json

# Configuración de la página de Streamlit
st.set_page_config(page_title="Generador de Ensayos", page_icon="📝", layout="wide")

# Título de la aplicación
st.title("Generador de Ensayos Académicos")

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
        prompt = f"""Desarrolla un ensayo académico fluido y cohesivo sobre la siguiente tesis:

{thesis}

Directrices para la estructura y el contenido del ensayo:

1. Introducción:
   - Presenta la tesis de manera clara y atractiva.
   - Proporciona un breve contexto que establezca la importancia del tema.

2. Cuerpo del ensayo:
   - Desarrolla varios argumentos que apoyen la tesis de manera fluida y natural.
   - No utilices numeración, viñetas o subtítulos para los argumentos.
   - Cada párrafo debe centrarse en una idea principal que respalde la tesis.
   - Integra suavemente 15 citas relevantes de autores reconocidos a lo largo del texto.
   - Asegúrate de que haya transiciones suaves y lógicas entre los párrafos, creando un flujo coherente de ideas.
   - Aborda posibles contraargumentos de manera equilibrada, reforzando tu posición.

3. Conclusión:
   - Resume los puntos principales sin repetirlos textualmente.
   - Reafirma la tesis de manera convincente.
   - Ofrece una reflexión final o implicaciones más amplias del tema.

Estilo y tono:
- Mantén un estilo académico pero accesible, evitando jerga innecesaria.
- Usa un lenguaje preciso y variado para mantener el interés del lector.
- Asegúrate de que cada párrafo fluya naturalmente hacia el siguiente, sin transiciones abruptas o forzadas.

Genera un ensayo que siga estas directrices, manteniendo una estructura coherente y un argumento persuasivo a lo largo del texto, sin recurrir a enumeraciones o listados explícitos de puntos."""

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
            
            # Mostrar el ensayo generado sin encabezado adicional
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
4. El ensayo tendrá una estructura fluida con argumentos bien desarrollados e integrados, citas relevantes y transiciones suaves entre párrafos.
""")

# Nota sobre la API key
st.sidebar.info("Nota: La API key está segura en los secretos de Streamlit.")
