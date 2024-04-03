from google.cloud import firestore, storage
from dotenv import load_dotenv

# Load environement variables
load_dotenv()

def get_firestore_client():
     
    return firestore.Client()