# src/csv_to_pg/routes/import_route.py

from fastapi import APIRouter, HTTPException, Depends
from csv_to_pg.services.import_service import VehiclePartImporter
from csv_to_pg.services.s3_client import S3Client
from csv_to_pg.services.parse_csv import import_csv_to_db
from csv_to_pg.config import env
from csv_to_pg.utils.response_codes import RESPONSE_CODES
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Dependency injection functions
def get_s3_client() -> S3Client:
    return S3Client(bucket_name=env.S3_BUCKET_NAME)

def get_csv_importer() -> callable:
    return import_csv_to_db

@router.post("/import-vehicle-parts")
def import_vehicle_parts(
    s3_client: S3Client = Depends(get_s3_client),
    csv_importer: callable = Depends(get_csv_importer)
):
    try:
        # Pass the dependencies to the VehiclePartImporter
        importer = VehiclePartImporter(
            bucket_name=env.S3_BUCKET_NAME,
            s3_key="vehicle_parts.csv",
            local_path=env.LOCAL_PATH,
            s3_client=s3_client,
            csv_importer=csv_importer
        )
        importer.run_import()
        return {"message": RESPONSE_CODES["IMPORT_SUCCESS"]["detail"]}
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise HTTPException(**RESPONSE_CODES["FILE_NOT_FOUND"])
    except ValueError as e:
        logger.error(f"Value error during import: {e}")
        raise HTTPException(**RESPONSE_CODES["INVALID_DATA_FORMAT"])
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(**RESPONSE_CODES["UNEXPECTED_ERROR"])
