import os
from dotenv import load_dotenv
from notion.client import get_notion_texts


def main():
    # Cargar variables de entorno desde el archivo .env
    load_dotenv()

    database_id = "2d6f99825fef8046b59af865011fb0b9"
    notion_api = os.getenv("NOTION_API_KEY")

    ideas = get_notion_texts(notion_api, database_id)
    for idea in ideas:
        print(idea)


if __name__ == "__main__":
    main()
