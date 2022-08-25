import sys
import os

if sys.version_info >= (3, 5):
    DEFAULT_SOCKET_TIMEOUT = (20, 2000)  # type: ignore

    from azure.core.exceptions import (
        ResourceNotFoundError
    )
    from azure.storage.blob import BlobServiceClient

CONNECTION_STRING = sys.argv[1]
LOCAL_BLOB_PATH = "data"
DL_FILE_NAME = "dl.txt"


def return_blobs_as_string():
    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)

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


def save_blob(file_name, file_content):
    # Get full path to the file
    download_file_path = os.path.join(LOCAL_BLOB_PATH, file_name)

    # for nested blobs, create local path as well!
    os.makedirs(os.path.dirname(download_file_path), exist_ok=True)

    with open(download_file_path, "wb") as file:
        file.write(file_content)


def create_list_of_files_from_text_file(file_name):
    with open(file_name, "r") as file:
        lines = file.readlines()
        return lines


def blobs_download():
    container = input('Enter container name: ')
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    my_container = blob_service_client.get_container_client(container)
    my_blobs = my_container.list_blobs()

    blobs_to_download = create_list_of_files_from_text_file(DL_FILE_NAME)

    for my_blob in my_blobs:
        for blob_to_dl in blobs_to_download:
            if my_blob.name == blob_to_dl.strip():
                data = my_container.get_blob_client(my_blob).download_blob().readall()
                save_blob(my_blob.name, data)
                print("Downloaded blob: ", my_blob.name)


def main():
    """Pass connection string as a first parameter. See
    https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python?tabs=environment-variable
    -linux#get-the-connection-string """
    print(return_blobs_as_string())

    # Saving blobs to local folder
    saving_output_sure = input('\nDo you need to save listing of BLOBs (y/n): ').lower().strip() == 'y'
    if saving_output_sure:
        saving_output_file = input('\nSpecify file name to save this output: ')
        with open(saving_output_file, "wb") as file:
            file.write(return_blobs_as_string().encode())

    # Downloading blobs
    downloading_blobs_sure = input(f'\nDo you need to download BLOBs per {DL_FILE_NAME} (y/n): ').lower().strip() == 'y'
    if downloading_blobs_sure:
        print(f"Downloading BLOBs as instructed in {DL_FILE_NAME} ...")
        blobs_download()
    else:
        print("Not downloading BLOBs")


if "__main__" == __name__:
    main()
