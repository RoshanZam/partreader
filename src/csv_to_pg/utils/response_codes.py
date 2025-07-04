# src/csv_to_pg/utils/response_codes.py

RESPONSE_CODES = {
    "FILE_NOT_FOUND": {"status_code": 404, "detail": "File not found"},
    "INVALID_DATA_FORMAT": {"status_code": 400, "detail": "Invalid data format"},
    "UNEXPECTED_ERROR": {"status_code": 500, "detail": "An unexpected error occurred"},
    "IMPORT_SUCCESS": {"status_code": 200, "detail": "Import completed successfully"},
}