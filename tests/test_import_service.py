from unittest.mock import MagicMock
from csv_to_pg.services.import_service import VehiclePartImporter

def test_vehicle_part_importer_run_import():
    # Arrange
    mock_s3_client = MagicMock()
    mock_csv_importer = MagicMock(return_value=(100, 20))  # Mock returns rows_added and skipped_rows

    importer = VehiclePartImporter(
        bucket_name="test-bucket",
        s3_key="test-key",
        local_path="/tmp/test-file",
        s3_client=mock_s3_client,
        csv_importer=mock_csv_importer
    )

    # Act
    result = importer.run_import()

    # Assert
    assert result == {"rows_added": 100, "rows_skipped": 20}
    mock_s3_client.download_file.assert_called_once_with("test-key", "/tmp/test-file")
    mock_csv_importer.assert_called_once_with("/tmp/test-file")
