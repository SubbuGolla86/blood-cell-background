from google.cloud import datastore

datastore_client = datastore.Client()
kind_name = "blood-cell-db"


def fetch_blood_cell_record(record_id):
    key = datastore_client.key(kind_name, record_id)
    entity = datastore_client.get(key)
    return entity

def update_blood_cell_record(record_id,result):
    key = datastore_client.key(kind_name, record_id)
    entity = datastore_client.get(key)

    if not entity:
        print(f"Record with ID {record_id} not found.")
        return False

    entity["status"] = "success"
    entity["result"] = result

    datastore_client.put(entity)
    return True
