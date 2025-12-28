import os
import requests
from PIL import Image
from io import BytesIO


def generate_image_hf(prompt):
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    api_url = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {"inputs": prompt, "options": {"wait_for_model": True}}

    try:
        response = requests.post(api_url, headers=headers, json=payload)

        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            file_name = "imagen_generada.png"
            image.save(file_name)
            print(f"Imagen guardada como: {file_name}")
            return file_name
        else:
            print(
                f"Error en Hugging Face API: {response.status_code} - {response.text}"
            )
            return None

    except Exception as e:
        print(f"Error generando imagen con Hugging Face: {e}")
        return None
