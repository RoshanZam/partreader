# src/csv_to_pg/main.py

from fastapi import FastAPI
from csv_to_pg.routes.import_route import router
from csv_to_pg.config.logging import setup_logging

setup_logging()
app = FastAPI()
app.include_router(router)
