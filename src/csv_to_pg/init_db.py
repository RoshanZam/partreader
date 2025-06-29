from csv_to_pg.config.db import Base, engine
from csv_to_pg.models.vehicle_part import VehiclePart

print("Creating vehicle_parts table...")
Base.metadata.create_all(bind=engine)
print("Done.")
