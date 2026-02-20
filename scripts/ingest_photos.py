import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

load_dotenv()

def upload_folder_to_azure(local_folder, container_name, azure_folder):
    connection_string = os.getenv("AZURE_CONNECTION_STRING")
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Lista todos os arquivos da sua pasta local
    files = [f for f in os.listdir(local_folder) if os.path.isfile(os.path.join(local_folder, f))]

    print(f"Iniciando o upload de {len(files)} fotos para {container_name}/{azure_folder}...")

    for file_name in files:
        local_path = os.path.join(local_folder, file_name)
        # Define o caminho na Azure: fotos/nome_da_foto.jpg
        blob_path = f"{azure_folder}/{file_name}"

        blob_client = blob_service_client.get_blob_client(container = container_name, blob = blob_path)

        with open(local_path, "rb") as data:
            blob_client.upload_blob(data, overwrite = True)
            print(f"Enviado: {file_name}")

if __name__ == "__main__":
    local_dir = "data/photos_sample"
    if os.path.exists(local_dir):
        upload_folder_to_azure(local_dir, "bronze", "fotos")
    else:
        print("PAsta de fotos não encontrada.")