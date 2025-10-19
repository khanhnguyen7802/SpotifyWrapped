from databricks.sdk.runtime import *
from azure.storage.blob import BlobServiceClient

def mounting_all_containers(storage_account,  key): 
    # Connect to Azure Blob Storage
    blob_service_client = BlobServiceClient(
        f"https://{storage_account}.blob.core.windows.net", credential=key
    )

    # Get all containers
    containers = [container.name for container in blob_service_client.list_containers()]

    # Mount ADLS only if the container is not already mounted
    for container in containers:
        source = f"wasbs://{container}@{storage_account}.blob.core.windows.net/"
        mount_folder = f"/mnt/{storage_account}/{container}"  
        config = {"fs.azure.account.key." + storage_account + ".blob.core.windows.net" : key}

        if not any(mount.mountPoint == mount_folder for mount in dbutils.fs.mounts()): 
            try:
                dbutils.fs.mount(
                    source = source,
                    mount_point = mount_folder,
                    extra_configs = config)
                print(f"Mount to {mount_folder} succeeded!")
            except Exception as e:    
                print(f"Mount to {mount_folder} failed: {e}")
     
     


     