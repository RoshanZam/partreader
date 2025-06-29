import pytest
from unittest.mock import mock_open, patch, MagicMock
from csv_to_pg.services import parse_csv
from csv_to_pg.models.vehicle_part import VehiclePart

CSV_CONTENT = """part_number,part_name,manufacturer,price,quantity
PN001,Brake Pad,Brembo,100.50,10
PN002,Air Filter,Bosch,45.00,20
"""

@patch("csv_to_pg.services.parse_csv.open", new_callable=mock_open, read_data=CSV_CONTENT)
@patch("csv_to_pg.services.parse_csv.SessionLocal")
def test_import_csv_to_db(mock_session_local, mock_file):
    mock_session = MagicMock()
    mock_session_local.return_value = mock_session

    parse_csv.import_csv_to_db("dummy.csv")

    assert mock_session.add.call_count == 2
    mock_session.commit.assert_called_once()
    mock_session.close.assert_called_once()
