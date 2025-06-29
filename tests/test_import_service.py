import pytest
from unittest.mock import patch
from csv_to_pg.services.import_service import VehiclePartImporter


@patch("csv_to_pg.services.import_service.import_csv_to_db")
@patch("csv_to_pg.services.import_service.S3Client")
def test_run_import(mock_s3_client_class, mock_import_csv_to_db):
    # Arrange
    bucket_name = "test-bucket"
    s3_key = "test.csv"
    local_path = "test.csv"

    mock_s3_client_instance = mock_s3_client_class.return_value

    importer = VehiclePartImporter(bucket_name, s3_key, local_path)

    # Act
    importer.run_import()

    # Assert
    mock_s3_client_class.assert_called_once_with(bucket_name)
    mock_s3_client_instance.download_file.assert_called_once_with(s3_key, local_path)
    mock_import_csv_to_db.assert_called_once_with(local_path)
