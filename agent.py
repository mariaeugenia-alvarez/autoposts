import random
import requests


def generate_content(topic):
    return random.randint(1, 1000)


def update_page_content(api_key, page_id, new_content):
    url = f"https://api.notion.com/v1/pages/{page_id}"

    headers = {
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key,
    }

    data = {
        "properties": {
            "Contenido": {"rich_text": [{"text": {"content": str(new_content)}}]}
        }
    }

    response = requests.patch(url, headers=headers, json=data)
    return response.status_code == 200
