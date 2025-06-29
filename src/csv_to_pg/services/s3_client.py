# src/csv_to_pg/services/s3_client.py

import boto3

class S3Client:
    def __init__(self, bucket_name: str):
        self.bucket = bucket_name
        self.s3 = boto3.client("s3")

    def download_file(self, s3_key: str, local_path: str):
        self.s3.download_file(self.bucket, s3_key, local_path)
