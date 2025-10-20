import json
import boto3
import urllib3
import os
from datetime import datetime

s3 = boto3.client('s3')
http = urllib3.PoolManager()

def lambda_handler(event, context):
    bucket_name = os.environ.get("BUCKET_NAME")
    
    # Obtener parámetros del event 
    api_source = os.environ.get("API_SOURCE", "users") # Uses default "users" if not set
    api_url = event.get("api_url", "https://jsonplaceholder.typicode.com/users") # Default API URL
    
    response = http.request("GET", api_url)
    data = json.loads(response.data.decode('utf-8'))
    
    # Manejar diferentes estructuras de API
    if isinstance(data, dict) and 'results' in data:
        users = data['results']  # Para APIs como randomuser.me
    else:
        users = data  # Para APIs como jsonplaceholder

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{api_source}/{api_source}_{timestamp}.json" # Dynamic folder/filename

    s3.put_object(
        Bucket=bucket_name,
        Key=filename,
        Body="\n".join([json.dumps(user) for user in users]), # JSONL format
        ContentType='application/json'
    )

    return {
        "statusCode": 200,
        "body": f"{len(users)} {api_source} saved to {filename} in {bucket_name}"
    }