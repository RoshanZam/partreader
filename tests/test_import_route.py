from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from csv_to_pg.main import app
from csv_to_pg.routes.import_route import get_vehicle_part_importer
from csv_to_pg.utils.response_codes import RESPONSE_CODES

client = TestClient(app)

def test_import_vehicle_parts_success():
    # Arrange
    mock_importer = MagicMock()
    mock_importer.run_import.return_value = {"rows_added": 100, "rows_skipped": 20}

    # Override the dependency
    app.dependency_overrides[get_vehicle_part_importer] = lambda: mock_importer

    # Act
    response = client.post("/import-vehicle-parts")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": RESPONSE_CODES["IMPORT_SUCCESS"]["detail"],
        "rows_added": 100,
        "rows_skipped": 20
    }
    mock_importer.run_import.assert_called_once()

def test_import_vehicle_parts_file_not_found():
    # Arrange
    mock_importer = MagicMock()
    mock_importer.run_import.side_effect = FileNotFoundError("File not found")

    # Override the dependency
    app.dependency_overrides[get_vehicle_part_importer] = lambda: mock_importer

    # Act
    response = client.post("/import-vehicle-parts")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": RESPONSE_CODES["FILE_NOT_FOUND"]["detail"]}
    mock_importer.run_import.assert_called_once()

def test_import_vehicle_parts_invalid_data_format():
    # Arrange
    mock_importer = MagicMock()
    mock_importer.run_import.side_effect = ValueError("Invalid data format")

    # Override the dependency
    app.dependency_overrides[get_vehicle_part_importer] = lambda: mock_importer

    # Act
    response = client.post("/import-vehicle-parts")

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": RESPONSE_CODES["INVALID_DATA_FORMAT"]["detail"]}
    mock_importer.run_import.assert_called_once()

def test_import_vehicle_parts_unexpected_error():
    # Arrange
    mock_importer = MagicMock()
    mock_importer.run_import.side_effect = Exception("Unexpected error")

    # Override the dependency
    app.dependency_overrides[get_vehicle_part_importer] = lambda: mock_importer

    # Act
    response = client.post("/import-vehicle-parts")

    # Assert
    assert response.status_code == 500
    assert response.json() == {"detail": RESPONSE_CODES["UNEXPECTED_ERROR"]["detail"]}
    mock_importer.run_import.assert_called_once()
