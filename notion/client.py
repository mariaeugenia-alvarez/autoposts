import requests
from langchain_core.tools import tool


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
        results = []
        for result in response.json().get("results", []):
            rich_text_list = (
                result.get("properties", {}).get("Texto", {}).get("rich_text", [])
            )
            full_text = "".join([item.get("plain_text", "") for item in rich_text_list])
            if full_text:
                results.append({"id": result["id"], "text": full_text})
        return results
    else:
        return []


@tool
def update_page_status(api_key: str, page_id: str, new_status: str) -> bool:
    """
    Updates the status of a Notion page.

    Args:
        api_key: The Notion API key.
        page_id: The ID of the page to update.
        new_status: The new status name (e.g., "Borrador").

    Returns:
        True if the update was successful, False otherwise.
    """
    url = f"https://api.notion.com/v1/pages/{page_id}"

    headers = {
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key,
    }

    data = {"properties": {"Estado": {"status": {"name": new_status}}}}

    response = requests.patch(url, headers=headers, json=data)
    return response.status_code == 200
