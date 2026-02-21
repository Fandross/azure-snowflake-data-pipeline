# Script para ingestão de arquivos de alta volumetria (Dataset de Reviews do Yelp - 5.3GB)
# Desenvolvido para processar 7 milhões de registros utilizando upload em blocos.

import os
import warnings
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient, ContentSettings

warnings.filterwarnings("ignore", category = UserWarning)
load_dotenv()

def upload_large_file(local_file_path, container_name, blob_name):
    connection_string = os.getenv("AZURE_CONNECTION_STRING")
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container = container_name, blob = blob_name)

    print(f"Iniciando upload: {local_file_path}")

    # Define o tamanho do pedaço, 4MB nesse chunk, para ser mais resiliente
    chunk_size = 4 * 1024 * 1024

    with open(local_file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite = True, max_concurrency = 4)
        print(f"Upload completo do arquivo {blob_name}!")

if __name__ == "__main__":
    # Verifica se o arquivo está exatamente assim na pasta data/
    path = "data/yelp_academic_dataset_review.json"
    if os.path.exists(path):
        upload_large_file(path, "bronze", "json/review.json")
    else:
        print("Arquivo review.json não encontrado na pasta data.")