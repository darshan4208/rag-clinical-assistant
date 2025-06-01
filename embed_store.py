import os
import requests

# === IBM Config ===
IBM_API_KEY = "your-ibm-api-key"  # Replace this with your actual API key
EMBED_URL = "https://us-south.ml.cloud.ibm.com"
MODEL_ID = "ibm/slate-125m-english-rtrvr"

def get_access_token():
    url = f"{EMBED_URL}/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={IBM_API_KEY}"
    response = requests.post(url, headers=headers, data=data)
    return response.json()["access_token"]

def read_documents(folder_path):
    docs = []
    for fname in os.listdir(folder_path):
        with open(os.path.join(folder_path, fname), 'r', encoding='utf-8') as f:
            text = f.read()
            docs.append((fname, text))
    return docs

def chunk_text(text):
    return text.split("\n\n")  # Very simple chunking by paragraph

def embed_chunks(chunks, access_token):
    url = f"{EMBED_URL}/ml/v1/text/embedding"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "model_id": MODEL_ID,
        "inputs": chunks
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# === MAIN ===
if __name__ == "__main__":
    access_token = get_access_token()
    docs = read_documents("data")
    for fname, content in docs:
        chunks = chunk_text(content)
        res = embed_chunks(chunks, access_token)
        print(f"\n{fname}: Embedded {len(res['data'])} chunks.")
