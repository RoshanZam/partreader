# src/csv_to_pg/services/parse_csv.py

import csv
from csv_to_pg.models.vehicle_part import VehiclePart
from csv_to_pg.config.db import SessionLocal

def import_csv_to_db(csv_path: str):
    session = SessionLocal()
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            part = VehiclePart(
                part_number=row["part_number"],
                part_name=row["part_name"],
                manufacturer=row["manufacturer"],
                price=float(row["price"]),
                quantity=int(row["quantity"])
            )
            session.add(part)
        session.commit()
        session.close()
