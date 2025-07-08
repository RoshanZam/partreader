# src/csv_to_pg/services/parse_csv.py

import csv
from csv_to_pg.models.vehicle_part import VehiclePart
from csv_to_pg.config.db import SessionLocal
import logging
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger(__name__)

def import_csv_to_db(csv_path: str):
    session = SessionLocal()
    rows_added = 0
    skipped_rows = 0

    try:
        logger.info(f"Importing CSV from path: {csv_path}")
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Check if the record already exists
                existing_part = session.query(VehiclePart).filter_by(part_number=row["part_number"]).first()
                if existing_part:
                    skipped_rows += 1
                    continue

                # Add the new record
                part = VehiclePart(
                    part_number=row["part_number"],
                    part_name=row["part_name"],
                    manufacturer=row["manufacturer"],
                    price=float(row["price"]),
                    quantity=int(row["quantity"])
                )
                session.add(part)
                rows_added += 1
            logger.info(f"Rows processed: {rows_added}, Rows skipped: {skipped_rows}")
            # Commit the transaction after processing all rows
            session.commit()
            logger.info(f"CSV import completed. Rows added: {rows_added}, Rows skipped: {skipped_rows}")
    except Exception as e:
        logger.exception("Failed to import CSV data to the database")
        session.rollback()
        raise
    finally:
        session.close()
        logger.info("CSV import process finished.")

    return rows_added, skipped_rows
