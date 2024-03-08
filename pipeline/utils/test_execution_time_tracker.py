"""execution_time_tracker.ExecutionTimeTracker tests"""
from conf.config import Configuration
from datetime import datetime
from execution_time_tracker import ExecutionTimeTracker

conf = Configuration()

def test_execution_time_tracker_read_error():
    """Tests read when file does not exist"""
    datetime_format='%Y-%m-%d %H:%M'
    time_tracker = ExecutionTimeTracker(conf.tmp_storage+'/not_there', datetime_format)
    got = time_tracker.get_last_execution_datetime()
    assert got == ''
    got = time_tracker.get_last_execution_datetime(as_string=False)
    assert got is None

def test_execution_time_tracker():
    """Tests that the recorded datetime is same as the readed"""
    datetime_format='%Y-%m-%d %H:%M'
    time_tracker = ExecutionTimeTracker(conf.tmp_storage+'/execution_time_record', datetime_format)
    now = datetime.now()
    time_tracker.record_current_datetime(dt=now)
    got = time_tracker.get_last_execution_datetime()
    assert got == now.strftime(datetime_format)
