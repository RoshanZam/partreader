# src/csv_to_pg/routes/import_route.py

from fastapi import APIRouter
from csv_to_pg.services.import_service import VehiclePartImporter
from csv_to_pg.config import env

router = APIRouter()

@router.post("/import-vehicle-parts")
def import_vehicle_parts():
    importer = VehiclePartImporter(
        bucket_name=env.S3_BUCKET_NAME,
        s3_key="vehicle_parts.csv",
        local_path=env.LOCAL_PATH
    )
    importer.run_import()
    return {"message": "Import completed"}
