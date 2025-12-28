import requests
import os


def upload_file_to_notion(api_key, file_path):
    """
    Sube un archivo a Notion usando la API de File Uploads.
    Retorna el file_upload_id si es exitoso, o None si falla.
    """
    # Paso 1: Crear el objeto File Upload
    create_url = "https://api.notion.com/v1/file_uploads"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    try:
        # Paso 1
        response = requests.post(create_url, headers=headers, json={})
        if response.status_code != 200:
            print(
                f"Error creando file upload: {response.status_code} - {response.text}"
            )
            return None

        data = response.json()
        file_upload_id = data["id"]
        upload_url = data["upload_url"]

        # Paso 2: Subir el contenido del archivo
        # Nota: El endpoint de envío requiere multipart/form-data
        # Requests maneja el boundary automáticamente si pasamos 'files' y no seteamos Content-Type manualmente

        upload_headers = {
            "Authorization": f"Bearer {api_key}",
            "Notion-Version": "2022-06-28",
        }

        with open(file_path, "rb") as f:
            files = {"file": f}
            upload_response = requests.post(
                upload_url, headers=upload_headers, files=files
            )

            if upload_response.status_code == 200:
                print(f"Archivo subido exitosamente a Notion. ID: {file_upload_id}")
                return file_upload_id
            else:
                print(
                    f"Error subiendo contenido del archivo: {upload_response.status_code} - {upload_response.text}"
                )
                return None

    except Exception as e:
        print(f"Excepción en upload_file_to_notion: {e}")
        return None
