# CSV to PostgreSQL Importer

This project is a **FastAPI-based application** designed to import CSV files into a PostgreSQL database. It integrates with AWS S3 (or LocalStack for local development) to fetch CSV files and provides APIs to trigger the import process. The application also handles duplicate records and logs skipped rows into a separate CSV file for review.

---

## Features

- **FastAPI Framework**: Provides RESTful APIs for importing CSV files.
- **AWS S3 Integration**: Downloads CSV files from S3 buckets (supports LocalStack for local development).
- **PostgreSQL Database**: Imports data into a PostgreSQL database.
- **Duplicate Handling**: Skips duplicate records and logs them into a separate CSV file.
- **LocalStack Support**: Enables local testing of AWS services like S3 and Lambda.
- **AWS Lambda Integration**: Includes a Lambda function to trigger the import API.

---

## Project Structure
