from google.cloud import storage
from google.oauth2 import service_account
credentials = service_account.Credentials.from_service_account_file(r'C:\Users\ahmed\Documents\Summer2019\GCPCredentials\images\outfitgenerator-470f47e0556c.json')


def create_bucket(bucket_name):
    print(credentials)
    storage_client = storage.Client(project = "outfitgenerator",credentials = credentials)
    bucket = storage_client.create_bucket(bucket_name)

    print("Bucket {} created.".format(bucket.name))

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client(project = "outfitgenerator",credentials = credentials)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))

#create_bucket('my-test-outfit-bucket')
#source = r"C:\Users\ahmed\Documents\Summer2019\OutfitGenerator\media\training_data\test.jpg"
#upload_blob("my-test-outfit-bucket",source,"test")