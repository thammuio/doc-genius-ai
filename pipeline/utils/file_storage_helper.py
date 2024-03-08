"""File Storage read/write abstraction layer. Supports S3 or local"""
import boto3
from conf.config import Configuration

class FileStorageHelper:
    """File storage helper class"""

    conf = Configuration()
    bucket_name = conf.bucket_name

    def __init__(self, storage_method=conf.default_storage_method):
        self.storage_method = storage_method
        if storage_method == 's3':
            self.s3_client = boto3.client('s3',
                                aws_access_key_id=self.conf.aws_access_key_id,
                                aws_secret_access_key=self.conf.aws_secret_access_key)

    def write(self, file_path, body):
        """Writes body to specified file_path"""
        if self.storage_method == 's3':
            self.s3_client.put_object(
                Bucket=self.bucket_name, Key=file_path, Body=body.encode("utf-8"))
        else:
            with open("./" + file_path, 'w', encoding="utf-8") as file:
                file.write(body)

    def read(self, file_path):
        """Reads from specified file_path"""
        if self.storage_method == 's3':
            response = self.s3_client.get_object(
                Bucket=self.bucket_name, Key=file_path)
            return response['Body'].read().decode('utf-8')
        else:
            with open(file_path, 'r', encoding="utf-8") as file:
                return file.read()
