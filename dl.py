import logging
from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob import BlobServiceClient
import azure.functions as func
import os, json

def get_value_from_secret_file_json(key):
    """
    Retrieves a value from a JSON file containing secrets.

    Args:
        key (str): The key to retrieve from the JSON file.

    Returns:
        str or None: The value associated with the key, or None if the key is not found.
    """
    cwd = os.getcwd()
    secret_file = os.path.join(cwd, 'secret.json')
    with open(secret_file, 'r') as json_file:
        data = json.load(json_file)
        if key in data:
            return data[key]
        else:
            return None

def return_blobs_as_string():
    """
    Retrieves a list of blob names from Azure Blob Storage containers.

    Returns:
        str: A string containing the names of blobs in various containers.
    """
    blob_service_client = BlobServiceClient.from_connection_string(get_value_from_secret_file_json('conn_string'))
    all_containers = blob_service_client.list_containers()
    blobs_listing = ""
    for container in all_containers:
        blobs_listing += f"\n==== Blobs in container {container.name} ====\n"
        container_client = blob_service_client.get_container_client(container.name)
        try:
            for blob in container_client.list_blobs():
                blobs_listing += blob.name + "\n"
        except ResourceNotFoundError:
            blobs_listing += "Container not found."
    return blobs_listing

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function that handles HTTP requests.

    Args:
        req (HttpRequest): The HTTP request object.

    Returns:
        func.HttpResponse: The HTTP response object.
    """
    logging.info('Python HTTP trigger function processed a request.')
    conn_string = get_value_from_secret_file_json('conn_string')

    # Set the logging level to control log output
    logging.Logger.root.level = 10
    blobs = return_blobs_as_string()

    # Log the retrieved blobs
    logging.info(blobs)
    
    # Return an HTTP response
    return func.HttpResponse(blobs, mimetype="text/plain", status_code=200)

if __name__ == "__main__":
    main(None)
