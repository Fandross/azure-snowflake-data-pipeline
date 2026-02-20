import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

load_dotenv()

def upload_to_azure(file_path, container_name, blob_name):
    connection_string = os.getenv("AZURE_CONNECTION_STRING")
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Cria a referencia para o arquivo na nuvem
    blob_client = blob_service_client.get_blob_client(container = container_name, blob = blob_name)

    print(F"Uploading {file_path} para o container {container_name}...")

    with open(file_path, 'rb') as data:
        blob_client.upload_blob(data, overwrite = True)

    print(F"Upload de {blob_name} concluido!")

# Teste com o arquivo de Business (que é menor que o Review)
if __name__ == "__main__":
    local_file = "data/yelp_academic_dataset_business.json"

    # Verifica se o arquivo existe localmente antes de tentar subir
    # Cria uma pasta virtual json/ no container para manter a organização
    if os.path.exists(local_file):
        upload_to_azure(local_file, "bronze", "json/yelp_academic_dataset_business.json")
    else:
        print(f"Arquivo {local_file} não encontrado na pasta data/")
