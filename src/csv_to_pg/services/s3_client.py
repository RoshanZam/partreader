# src/csv_to_pg/services/s3_client.py

import boto3
import logging
from csv_to_pg.config import env

logger = logging.getLogger(__name__)

class S3Client:
    def __init__(self, bucket_name: str):
        self.bucket = bucket_name

        # Use LocalStack endpoint if defined, otherwise use default AWS endpoint
        endpoint_url = env.LOCALSTACK_ENDPOINT
        if endpoint_url:
            logger.info(f"Using LocalStack endpoint: {endpoint_url}")
        else:
            logger.info("Using default AWS endpoint")

        self.s3 = boto3.client(
            "s3",
            endpoint_url=endpoint_url,  # Connect to LocalStack if endpoint is set
            aws_access_key_id="test",  # Dummy credentials for LocalStack
            aws_secret_access_key="test",
            region_name="us-east-1"
        )
        logger.info(f"S3 client initialized for bucket: {self.bucket}")

    def download_file(self, s3_key: str, local_path: str):
        logger.info(f"Downloading {s3_key} to {local_path}")
        self.s3.download_file(self.bucket, s3_key, local_path)
        logger.info("Download complete")
