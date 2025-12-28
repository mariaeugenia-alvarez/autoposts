import os
from dotenv import load_dotenv


def main():
    # Cargar variables de entorno desde el archivo .env
    load_dotenv()

    # Obtener la variable de entorno
    message = os.getenv("MESSAGE", "No se encontró la variable MESSAGE")

    print(message)


if __name__ == "__main__":
    main()
