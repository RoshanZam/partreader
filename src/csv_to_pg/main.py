# src/csv_to_pg/main.py

from fastapi import FastAPI
from csv_to_pg.routes.import_route import router

app = FastAPI()
app.include_router(router)
