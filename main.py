import os
from dotenv import load_dotenv

import requests


def main():
    # Cargar variables de entorno desde el archivo .env
    load_dotenv()

    url = "https://api.notion.com/v1/databases/2d6f99825fef8046b59af865011fb0b9/query"

    notion_api = os.getenv("NOTION_API_KEY")

    headers = {
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + notion_api,
    }
    data = {"page_size": 10}

    response = requests.post(url, headers=headers, json=data)
    # Ver respuesta
    print(response.status_code)
    print(response.json())


if __name__ == "__main__":
    main()
