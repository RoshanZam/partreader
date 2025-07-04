from unittest.mock import MagicMock, patch
from csv_to_pg.services.s3_client import S3Client

@patch("csv_to_pg.services.s3_client.boto3.client")
def test_s3_client_initialization(mock_boto_client):
    # Arrange
    mock_boto_instance = MagicMock()
    mock_boto_client.return_value = mock_boto_instance

    # Act
    client = S3Client(bucket_name="test-bucket")

    # Assert
    mock_boto_client.assert_called_once_with(
        "s3",
        endpoint_url="http://localhost:4566",  # Assuming LOCALSTACK_ENDPOINT is set
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1"
    )
    assert client.bucket == "test-bucket"

@patch("csv_to_pg.services.s3_client.boto3.client")
def test_s3_client_download_file(mock_boto_client):
    # Arrange
    mock_boto_instance = MagicMock()
    mock_boto_client.return_value = mock_boto_instance
    client = S3Client(bucket_name="test-bucket")

    # Act
    client.download_file("test-key", "/tmp/test-file")

    # Assert
    mock_boto_instance.download_file.assert_called_once_with("test-bucket", "test-key", "/tmp/test-file")
