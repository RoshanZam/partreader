import json
import requests

def lambda_handler(event, context):
    # Define the FastAPI endpoint
    api_url = "http://host.docker.internal:8000/import-vehicle-parts"  # Use host.docker.internal for LocalStack

    # Make the POST request to the FastAPI API
    try:
        response = requests.post(api_url)
        response_data = response.json()

        return {
            "statusCode": response.status_code,
            "body": json.dumps(response_data)
        }
    except requests.exceptions.RequestException as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }