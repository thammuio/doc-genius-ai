"""file_storage_helper.FileStorageHelper tests"""
import os
from file_storage_helper import FileStorageHelper
from conf.config import Configuration

conf = Configuration()

def test_local_read_write():
    """Tests that writen value is same as readed"""
    file_storage = FileStorageHelper()

    value = "test"
    file_path = conf.tmp_storage + "/test_read_write"
    file_storage.write(file_path, value)
    assert file_storage.read(file_path) == value
