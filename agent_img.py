import os
from huggingface_hub import InferenceClient
from langchain_core.tools import tool


@tool
def generate_image_hf(prompt: str) -> bytes:
    """Generates an image using Hugging Face Inference API and returns the bytes."""
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    client = InferenceClient(token=api_key)

    try:
        # text-to-image returns a PIL Image by default in the python client
        image = client.text_to_image(
            prompt, model="stabilityai/stable-diffusion-xl-base-1.0"
        )

        # Convert PIL Image to bytes
        import io

        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format="PNG")
        return img_byte_arr.getvalue()

    except Exception as e:
        print(f"Error generando imagen con Hugging Face: {e}")
        return None
