# src/csv_to_pg/services/s3_client.py

import boto3
import logging

logger = logging.getLogger(__name__)

class S3Client:
    def __init__(self, bucket_name: str):
        self.bucket = bucket_name
        self.s3 = boto3.client("s3")
        logger.info("S3 client initialized for bucket: {self.bucket}")

    def download_file(self, s3_key: str, local_path: str):
        logger.info(f"Downloading {s3_key} to {local_path}")
        self.s3.download_file(self.bucket, s3_key, local_path)
        logger.info(f"Download complete")
