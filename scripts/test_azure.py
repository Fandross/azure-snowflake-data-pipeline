import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

# Carrega as variáveis do arquivo
load_dotenv()
connection_string = os.getenv('AZURE_CONNECTION_STRING')

try:
    # Tentar conectar com a Azure
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Lista os containers para ver se o Bronze aparece
    containers = blob_service_client.list_containers()
    print('Conexão realizada com sucesso. Containers encontrados: ')
    for container in containers:
        print(F" - {container.name}")
except Exception as e:
    print(F"Erro de conexão {e}")
