import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "creds.json"
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
from PIL import Image
from bucket import  download_file
from deep_learning import model_func,predict
from datastore import *

os.makedirs("uploaded", exist_ok=True)
os.makedirs("models", exist_ok=True)

model_path = "models/model_4.h5"
if not os.path.exists(model_path):
    download_file(model_path)

model_load = model_func(model_path)

timeout = 5.0

subscriber = pubsub_v1.SubscriberClient()
subscription_path = 'projects/spartan-vine-456818-e9/subscriptions/blood-cell-channel-sub'

def callback(message):
    record_id = message.data.decode('utf-8')
    print(f'Received message with record ID: {record_id}')
    path = fetch_blood_cell_record(record_id).get("image_path")
    print(f'Fetched image path: {path}')
    download_file(path)
    image = Image.open(path)
    result = predict(image,model_load)
    print(f'Prediction result: {result}')
    update_blood_cell_record(record_id, result)
    logging.info(f'Updated blood cell record for ID: {record_id} with result')
    message.ack()
    logging.info('Message acknowledged')
    

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f'Listening for messages on {subscription_path}')


with subscriber:
    try:
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()
