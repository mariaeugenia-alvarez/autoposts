import os
import requests
from openai import OpenAI


def generate_content(topic):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"Escribe un frase de 5 palabras corta y atractivo sobre: {topic}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Eres un experto creador de contenido para redes sociales.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content


def update_page_content(api_key, page_id, new_content, file_upload_id=None):
    url = f"https://api.notion.com/v1/pages/{page_id}"

    headers = {
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key,
    }

    properties = {"Contenido": {"rich_text": [{"text": {"content": str(new_content)}}]}}

    # Si tenemos un ID de archivo subido a Notion, lo usamos para la propiedad Imagen
    if file_upload_id:
        properties["Imagen"] = {
            "files": [{"type": "file_upload", "file_upload": {"id": file_upload_id}}]
        }

    data = {"properties": properties}

    response = requests.patch(url, headers=headers, json=data)
    return response.status_code == 200
