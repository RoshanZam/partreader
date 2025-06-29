# src/csv_to_pg/services/import_service.py

import logging
from csv_to_pg.services.s3_client import S3Client
from csv_to_pg.services.parse_csv import import_csv_to_db

logger = logging.getLogger(__name__)

class VehiclePartImporter:
    def __init__(self, bucket_name: str, s3_key: str, local_path: str):
        self.bucket_name = bucket_name
        self.s3_key = s3_key
        self.local_path = local_path

    def run_import(self):
        logger.info("Starting vehicle parts import...")
        s3 = S3Client(self.bucket_name)
        s3.download_file(self.s3_key, self.local_path)
        import_csv_to_db(self.local_path)
        logger.info("Vehicle parts import completed.")
