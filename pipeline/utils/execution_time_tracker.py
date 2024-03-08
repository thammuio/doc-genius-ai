"""Last execution time tracker"""
from datetime import datetime

from common.file_storage_helper import FileStorageHelper


class ExecutionTimeTracker:
    """Records and retrieves a datetime from storage"""

    def __init__(self, file_path, datetime_format='%Y-%m-%d %H:%M'):
        self.store = FileStorageHelper()
        self.file_path = file_path
        self.datetime_format = datetime_format

    def record_current_datetime(self, dt=datetime.now()):
        """Records current datetime"""        
        current_time = dt.strftime(self.datetime_format)
        self.store.write(file_path=self.file_path, body=current_time)

    def get_last_execution_datetime(self, as_string=True):
        """Retrieves current datetime"""        
        try:
            last_execution_time = self.store.read(self.file_path)
            if as_string:
                # returns string
                return str(last_execution_time)
            else:
                # returns datetime object
                try:
                    return datetime.strptime(last_execution_time, self.datetime_format)
                except ValueError:
                    return None
        except FileNotFoundError:
            if as_string:
                return ''
            else:
                return None
