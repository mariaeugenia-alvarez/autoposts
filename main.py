import os
from dotenv import load_dotenv
from notion.client import get_notion_texts, update_page_status


def main():
    # Cargar variables de entorno desde el archivo .env
    load_dotenv()

    database_id = "2d6f99825fef8046b59af865011fb0b9"
    notion_api = os.getenv("NOTION_API_KEY")

    items = get_notion_texts(notion_api, database_id)
    for item in items:
        print(f"Procesando: {item['text']}")
        if update_page_status(notion_api, item["id"], "En progreso"):
            print("Estado actualizado a 'En progreso'")
        else:
            print("Error al actualizar el estado")


if __name__ == "__main__":
    main()
