import requests


def get_notion_texts(api_key, database_id):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"

    headers = {
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key,
    }
    data = {"page_size": 10}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        texts = []
        for result in response.json().get("results", []):
            rich_text_list = (
                result.get("properties", {}).get("Texto", {}).get("rich_text", [])
            )
            full_text = "".join([item.get("plain_text", "") for item in rich_text_list])
            if full_text:
                texts.append(full_text)
        return texts
    else:
        return []
