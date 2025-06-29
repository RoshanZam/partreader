from unittest.mock import MagicMock, patch
from csv_to_pg.services.s3_client import S3Client

@patch("csv_to_pg.services.s3_client.boto3.client")
def test_download_file(mock_boto_client):
    mock_s3 = MagicMock()
    mock_boto_client.return_value = mock_s3

    client = S3Client("test-bucket")
    client.download_file("test.csv", "local.csv")

    mock_s3.download_file.assert_called_once_with("test-bucket", "test.csv", "local.csv")
