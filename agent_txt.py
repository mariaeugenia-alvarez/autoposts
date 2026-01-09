import requests
from langchain_core.tools import tool


@tool
def update_page_content(
    api_key: str, page_id: str, new_content: str, file_upload_id: str = None
) -> bool:
    """
    Updates the content of a Notion page.

    Args:
        api_key: The Notion API key.
        page_id: The ID of the page to update.
        new_content: The new text content for the page.
        file_upload_id: Optional ID of an uploaded file to attach as an image.

    Returns:
        True if the update was successful, False otherwise.
    """
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
