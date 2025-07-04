from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from csv_to_pg.main import app
from csv_to_pg.routes.import_route import get_vehicle_part_importer

def test_import_vehicle_parts_route():
    # Arrange
    mock_importer = MagicMock()
    mock_importer.run_import.return_value = None

    # Override the dependency
    app.dependency_overrides[get_vehicle_part_importer] = lambda: mock_importer

    client = TestClient(app)

    # Act
    response = client.post("/import-vehicle-parts")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Import completed successfully"}
    mock_importer.run_import.assert_called_once()
    