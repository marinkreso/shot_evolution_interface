from azure.storage.blob import BlobServiceClient, ContentSettings
import os
from glob import glob
container_name = "shot-evolution-report"
# Define your SAS token and the account URL
def initialize_azure():
    #sas_token = "sp=racw&st=2024-08-16T17:54:54Z&se=2024-09-17T01:54:54Z&spr=https&sv=2022-11-02&sr=c&sig=IVktIeArekEV7EJnCddixap3BP%2FaeKjAZGwUPmLY6Y0%3D"
    #sas_token = 'sp=racwl&st=2024-08-16T19:26:20Z&se=2024-10-17T03:26:20Z&spr=https&sv=2022-11-02&sr=c&sig=MJ4hVvIfNPkjqS8LC2GR1OULGrg1jVSVfSyH94FRplA%3D'
    #sas_token = 'sp=rcwl&st=2025-01-03T18:08:06Z&se=2025-03-01T02:08:06Z&spr=https&sv=2022-11-02&sr=c&sig=JBdBPT0dkMkSN8K0hDsTBVqlsOqVEf5IyYDJNNluZ%2BA%3D'
    #sas_token = 'sp=racwl&st=2025-03-03T02:46:29Z&se=2025-06-01T09:46:29Z&spr=https&sv=2022-11-02&sr=c&sig=pRStAmqfA8hY0zoq3Ofb%2B1O1P2PPOD25aLAKjCJK%2BRw%3D'
    sas_token = 'sp=racwdlmeo&st=2025-06-01T15:21:26Z&se=2025-07-29T23:21:26Z&spr=https&sv=2024-11-04&sr=c&sig=%2BF08pzdGpHOYZ9GBsdqr5pCEoxkekldepdGXx7pvKik%3D'
    sas_token = 'sp=racwdlmeop&st=2025-08-04T21:36:56Z&se=2025-09-06T05:51:56Z&spr=https&sv=2024-11-04&sr=c&sig=QkJemW%2BCUXwPUPPPnnf3ZrRx62y2X6VGo4lcxZZzgxo%3D'
    sas_token = 'sp=racwdlmeop&st=2025-09-06T08:49:42Z&se=2025-10-30T18:04:42Z&spr=https&sv=2024-11-04&sr=c&sig=p%2FrsKYvFaLJywRRHv67CMNDSYyqzc0Qrhg%2FvLHc%2BGx0%3D'
    sas_token = 'sp=racwdlmeop&st=2025-10-31T11:29:37Z&se=2026-01-02T19:44:37Z&spr=https&sv=2024-11-04&sr=c&sig=bljEx5g3X7Mk7BxW9Xa9Um9%2BrKI2F6tOfKEaIwYht60%3D'
    sas_token = 'sp=racwdlmeop&st=2026-01-02T13:21:47Z&se=2026-04-01T20:36:47Z&spr=https&sv=2024-11-04&sr=c&sig=NR0kzXS3I74NJ3tepdDc0ozA6NuZ8Y95%2BeosoCWijzE%3D'
    sas_token = 'sp=racwdlmeop&st=2026-04-01T23:07:58Z&se=2026-12-25T08:22:58Z&spr=https&sv=2024-11-04&sr=c&sig=NuwPtt0i3N5%2FQwRzXD1eiYWEKs%2Bk4INl4vtHjl5HF14%3D'
    account_url = "https://operationslakedb.blob.core.windows.net"
    

    # Create a BlobServiceClient object using the account URL and SAS token
    blob_service_client = BlobServiceClient(account_url=account_url, credential=sas_token)
    # Create a ContainerClient object to interact with the specified container
    container_client = blob_service_client.get_container_client(container_name)
    return container_client

container_client = initialize_azure()
def azure_upload_file(container_client, filename):
    # Create the blob client for the image you want to upload
    content_settings = ContentSettings(
        content_type='text/html',
    )
    blob_name = f"{filename}"  # Name of the blob in the container
    file_blob_client = container_client.get_blob_client(blob_name)

    # Open the local file and upload it to the blob
    print(filename)
    with open(filename, "rb") as data:
        file_blob_client.upload_blob(data, overwrite=True, content_settings=content_settings)
def azure_folder_exist(container_client, folder_name):
    blob_list = container_client.list_blobs(name_starts_with=folder_name)
    return len(list(blob_list))

def azure_upload_docx(container_client, filename):
    # Create the blob client for the image you want to upload
    content_settings = ContentSettings(
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    )
    blob_name = f"{filename}"  # Name of the blob in the container
    file_blob_client = container_client.get_blob_client(blob_name)

    # Open the local file and upload it to the blob
    print(filename)
    with open(filename, "rb") as data:
        file_blob_client.upload_blob(data, overwrite=True, content_settings=content_settings)
