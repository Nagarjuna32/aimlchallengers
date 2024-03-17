from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Azure Blob Storage Configuration
connection_string = "DefaultEndpointsProtocol=https;AccountName=storageaimlchallenge;AccountKey=506H55R6NKPBCnWfGPkb9uFjJaMAtuGtEylrA+fehYW41mvoGG6qR7DU6es1aB4lFsAsZt2uFTYU+AStNaVf5g==;EndpointSuffix=core.windows.net"
container_name = "aimlchallengers"

blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

# Utility function to upload file to Azure Blob Storage
def upload_document(file_content, entity_name):
    blob_client = container_client.get_blob_client(f"{entity_name}.pdf")
    blob_client.upload_blob(file_content)


def upload_blob(file):
    """
    Upload file to Azure Blob Storage container
    """
    # Create a BlobServiceClient using the connection string
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Create a ContainerClient for the specified container
    container_client = blob_service_client.get_container_client(container_name)

    # Define the destination blob name
    destination_blob_name = file.filename

    print(f'File: {file.filename} to be uploaded to destination {destination_blob_name}')

    # Upload the file to the container
    blob_client = container_client.get_blob_client(destination_blob_name)
    with open(file.filename, "rb") as data:
        blob_client.upload_blob(data)

    print(f'File: {file.filename} uploaded to destination {destination_blob_name}')


def get_blob_url(blob_name):
    """
    Generate URL to access blob in Azure Blob Storage container
    """

    # Create a BlobServiceClient using the connection string
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Generate URL for the specified blob
    blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob_name}"
    return blob_url