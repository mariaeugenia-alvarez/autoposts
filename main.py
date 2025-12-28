import os
from dotenv import load_dotenv
from notion.client import get_notion_texts, update_page_status
from agent_txt import generate_content, update_page_content
from agent_img import generate_image_hf
from notion_uploader import upload_file_to_notion


def main():
    # Cargar variables de entorno desde el archivo .env
    load_dotenv()

    database_id = "2d6f99825fef8046b59af865011fb0b9"
    notion_api = os.getenv("NOTION_API_KEY")

    items = get_notion_texts(notion_api, database_id)
    for item in items:
        print(f"Procesando: {item['text']}")

        content = generate_content(item["text"])
        print(f"Contenido generado: {content}")

        # Generar imagen (ahora devuelve los bytes de la imagen)
        image_bytes = generate_image_hf(content)

        file_upload_id = None
        if image_bytes:
            print(f"Imagen generada en memoria ({len(image_bytes)} bytes)")
            # Subir imagen a Notion usando la API de File Uploads
            file_upload_id = upload_file_to_notion(notion_api, image_bytes)

        update_page_content(notion_api, item["id"], content, file_upload_id)

        if update_page_status(notion_api, item["id"], "Borrador"):
            print("Estado actualizado a Borrador")
        else:
            print("Error al actualizar el estado")


if __name__ == "__main__":
    main()
