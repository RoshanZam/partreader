from sqlalchemy import Column, Integer, String, Float
from csv_to_pg.config.db import Base

class VehiclePart(Base):
    __tablename__ = "vehicle_parts"

    id = Column(Integer, primary_key=True, index=True)
    part_name = Column(String, nullable=False)
    part_number = Column(String, unique=True, nullable=False)
    manufacturer = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
