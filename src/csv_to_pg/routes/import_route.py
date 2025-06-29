# src/csv_to_pg/routes/import_route.py

from fastapi import APIRouter
from csv_to_pg.services.s3_client import S3Client
from csv_to_pg.services.parse_csv import import_csv_to_db
from csv_to_pg.config import env

router = APIRouter()

@router.post("/import-vehicle-parts")
def import_vehicle_parts():
    bucket_name = env.S3_BUCKET_NAME
    s3_key = "vehicle_parts.csv"
    local_path = env.LOCAL_PATH

    s3 = S3Client(bucket_name)
    s3.download_file(s3_key, local_path)

    import_csv_to_db(local_path)

    return {"message": "Import completed"}
