# src/csv_to_pg/services/import_service.py

import logging
from fastapi import Depends
from csv_to_pg.services.s3_client import S3Client
from csv_to_pg.services.parse_csv import import_csv_to_db
from botocore.exceptions import BotoCoreError, ClientError  # For S3-related errors
import csv  # For CSV parsing errors
import os  # For file-related errors

logger = logging.getLogger(__name__)

class VehiclePartImporter:
    def __init__(
        self,
        bucket_name: str,
        s3_key: str,
        local_path: str,
        s3_client: S3Client = Depends(),
        csv_importer: callable = Depends(import_csv_to_db),
    ):
        """
        Initialize the VehiclePartImporter with injected dependencies.

        :param bucket_name: Name of the S3 bucket.
        :param s3_key: Key of the file in the S3 bucket.
        :param local_path: Local path to save the downloaded file.
        :param s3_client: Injected S3Client instance.
        :param csv_importer: Injected function to import CSV data into the database.
        """
        self.bucket_name = bucket_name
        self.s3_key = s3_key
        self.local_path = local_path
        self.s3_client = s3_client
        self.csv_importer = csv_importer

    def run_import(self):
        """
        Run the import process: download the file from S3 and import its contents into the database.
        """
        try:
            logger.info("Starting vehicle parts import...")

            # Use the injected S3 client to download the file
            try:
                logger.info(f"Downloading {self.s3_key} from bucket {self.bucket_name} to {self.local_path}")
                self.s3_client.download_file(self.s3_key, self.local_path)
            except (BotoCoreError, ClientError) as e:
                logger.error(f"Error downloading file from S3: {e}")
                raise RuntimeError("Failed to download file from S3") from e

            # Use the injected CSV importer to process the file
            try:
                logger.info(f"Importing data from {self.local_path}")
                self.csv_importer(self.local_path)
            except (csv.Error, ValueError) as e:
                logger.error(f"Error parsing CSV file: {e}")
                raise RuntimeError("Failed to parse CSV file") from e

            logger.info("Vehicle parts import completed successfully.")

        except FileNotFoundError as e:
            logger.error(f"Local file not found: {e}")
            raise RuntimeError("Local file not found") from e
        except PermissionError as e:
            logger.error(f"Permission error: {e}")
            raise RuntimeError("Permission denied while accessing the file") from e
        except Exception as e:
            logger.error(f"Unexpected error during import: {e}")
            raise RuntimeError("An unexpected error occurred during the import process") from e
