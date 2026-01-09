import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from notion.client import get_notion_texts, update_page_status
from agent_txt import update_page_content
from agent_img import generate_image_hf
from notion_uploader import upload_file_to_notion


def main():
    # Cargar variables de entorno desde el archivo .env
    load_dotenv()

    database_id = "2d6f99825fef8046b59af865011fb0b9"
    notion_api = os.getenv("NOTION_API_KEY")

    # --- Pipeline LCEL puro sin lambdas ---

    # 1. Generación de texto
    prompt = ChatPromptTemplate.from_template(
        "Eres un experto creador de contenido para redes sociales. "
        "Escribe un frase de 5 palabras corta y atractivo sobre: {topic}"
    )
    model = ChatOpenAI(model="gpt-4o-mini")
    text_chain = prompt | model | StrOutputParser()

    # 2. Runnables wrapping de tools
    gen_image = RunnableLambda(lambda x: generate_image_hf.invoke(x))

    upload_image = RunnableLambda(
        lambda x: upload_file_to_notion.invoke(
            {"api_key": notion_api, "file_content": x}
        )
    )

    update_content = RunnableLambda(lambda x: update_page_content.invoke(x))

    update_status = RunnableLambda(lambda x: update_page_status.invoke(x))

    # 3. Composición del pipeline como expresión LCEL
    pipeline = (
        RunnablePassthrough.assign(content={"topic": lambda x: x["text"]} | text_chain)
        | RunnableLambda(
            lambda x: {**x, "image_bytes": generate_image_hf.invoke(x["content"])}
        )
        | RunnableLambda(
            lambda x: {
                **x,
                "file_upload_id": (
                    upload_file_to_notion.invoke(
                        {"api_key": notion_api, "file_content": x["image_bytes"]}
                    )
                    if x["image_bytes"]
                    else None
                ),
            }
        )
        | RunnableLambda(
            lambda x: {
                **x,
                "content_updated": update_page_content.invoke(
                    {
                        "api_key": notion_api,
                        "page_id": x["id"],
                        "new_content": x["content"],
                        "file_upload_id": x["file_upload_id"],
                    }
                ),
            }
        )
        | RunnableLambda(
            lambda x: {
                **x,
                "status_updated": update_page_status.invoke(
                    {
                        "api_key": notion_api,
                        "page_id": x["id"],
                        "new_status": "Borrador",
                    }
                ),
            }
        )
    )

    # Ejecución
    items = get_notion_texts(notion_api, database_id)
    for item in items:
        print(f"--- Procesando: {item['text']} ---")
        try:
            result = pipeline.invoke(item)
            print(f"✓ Contenido actualizado: {result['content_updated']}")
            print(f"✓ Estado actualizado: {result['status_updated']}\n")
        except Exception as e:
            print(f"✗ Error: {e}\n")


if __name__ == "__main__":
    main()
