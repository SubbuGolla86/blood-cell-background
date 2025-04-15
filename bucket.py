from google.cloud import  storage
import logging


logging.basicConfig(level=logging.INFO)

storage_client = storage.Client()
bucket_name = "blood_cell_bucket"
bucket = storage_client.bucket(bucket_name)

def download_file(file_name):
    logging.info(f"Starting download of '{file_name}' from bucket '{bucket_name}'...")

    image_blob = bucket.blob(file_name)
    image_blob.download_to_filename(file_name)

    logging.info(f"Download of '{file_name}' completed successfully.")
