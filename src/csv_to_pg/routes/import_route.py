# src/csv_to_pg/routes/import_route.py

from fastapi import APIRouter, HTTPException
from csv_to_pg.services.import_service import VehiclePartImporter
from csv_to_pg.config import env
from csv_to_pg.utils.response_codes import RESPONSE_CODES
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/import-vehicle-parts")
def import_vehicle_parts():
    try:
        importer = VehiclePartImporter(
            bucket_name=env.S3_BUCKET_NAME,
            s3_key="vehicle_parts.csv",
            local_path=env.LOCAL_PATH
        )
        importer.run_import()
        return {"message": RESPONSE_CODES["IMPORT_SUCCESS"]["detail"]}
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise HTTPException(RESPONSE_CODES["FILE_NOT_FOUND"])
    except ValueError as e:
        logger.error(f"Value error during import: {e}")
        raise HTTPException(RESPONSE_CODES["INVALID_DATA_FORMAT"])
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(RESPONSE_CODES["UNEXPECTED_ERROR"])
