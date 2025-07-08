import pytest
from unittest.mock import MagicMock, mock_open, patch
from csv_to_pg.services.parse_csv import import_csv_to_db

CSV_CONTENT = """part_number,part_name,manufacturer,price,quantity
PN001,Part1,Manufacturer1,10.5,5
PN002,Part2,Manufacturer2,20.0,10
"""

@patch("csv_to_pg.services.parse_csv.open", new_callable=mock_open, read_data=CSV_CONTENT)
@patch("csv_to_pg.services.parse_csv.SessionLocal")
def test_import_csv_success(mock_session_local, mock_file):
    mock_session = MagicMock()
    mock_session.query().filter_by().first.return_value = None  # Simulate no duplicates
    mock_session_local.return_value = mock_session

    rows_added, skipped_rows = import_csv_to_db("dummy.csv")

    assert rows_added == 2
    assert skipped_rows == 0
    assert mock_session.add.call_count == 2
    mock_session.commit.assert_called_once()
    mock_session.close.assert_called_once()


@patch("csv_to_pg.services.parse_csv.open", new_callable=mock_open, read_data=CSV_CONTENT)
@patch("csv_to_pg.services.parse_csv.SessionLocal")
def test_import_csv_skips_duplicates(mock_session_local, mock_file):
    mock_session = MagicMock()
    # First row is new, second is duplicate
    mock_session.query().filter_by().first.side_effect = [None, True]
    mock_session_local.return_value = mock_session

    rows_added, skipped_rows = import_csv_to_db("dummy.csv")

    assert rows_added == 1
    assert skipped_rows == 1
    assert mock_session.add.call_count == 1
    mock_session.commit.assert_called_once()
    mock_session.close.assert_called_once()


@patch("csv_to_pg.services.parse_csv.open", side_effect=Exception("CSV Read Error"))
@patch("csv_to_pg.services.parse_csv.SessionLocal")
def test_import_csv_raises_and_rolls_back(mock_session_local, mock_open):
    mock_session = MagicMock()
    mock_session_local.return_value = mock_session

    with pytest.raises(Exception, match="CSV Read Error"):
        import_csv_to_db("dummy.csv")

    mock_session.rollback.assert_called_once()
    mock_session.close.assert_called_once()
