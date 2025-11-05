import os
import ZODB
import ZODB.FileStorage
from ZODB.blob import BlobStorage

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZODB_DIR = os.path.join(BASE_DIR, 'zodb_data')
BLOB_DIR = os.path.join(ZODB_DIR, 'blobs')
os.makedirs(ZODB_DIR, exist_ok=True)
os.makedirs(BLOB_DIR, exist_ok=True)
ZODB_FILE = os.path.join(ZODB_DIR, 'zodb.fs')

file_storage = ZODB.FileStorage.FileStorage(ZODB_FILE)
storage = BlobStorage(BLOB_DIR, file_storage)
db = ZODB.DB(storage)

# Get a fresh connection
def get_connection():
    connection = db.open()
    root = connection.root()
    return connection, root

def close_zodb():
    db.close()
    storage.close()
    file_storage.close()

