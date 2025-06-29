# src/csv_to_pg/config/env.py
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env into os.environ

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
LOCAL_PATH = os.getenv("LOCAL_PATH");
