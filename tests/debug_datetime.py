from datetime import datetime, timezone
import sys
import os

# Thêm đường dẫn project vào sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from trm_api.adapters.data_adapters import DatetimeAdapter

def debug_datetime_issue():
    now = datetime.now(timezone.utc)
    print(f"Original datetime: {now}")
    
    # Kiểm tra kết quả ISO format
    iso_str = DatetimeAdapter.to_iso_format(now)
    print(f"ISO format: {iso_str}")
    print(f"Ends with Z: {iso_str.endswith('Z')}")
    
    # Kiểm tra trường hợp normalize field
    entity = {'created_at': now}
    result = DatetimeAdapter.normalize_datetime_field(entity, 'created_at')
    print(f"\nAfter normalize_datetime_field:")
    print(f"Result: {result}")
    print(f"Result value: {result['created_at']}")
    print(f"Ends with Z: {result['created_at'].endswith('Z')}")
    
    # Kiểm tra trường hợp normalize dict
    entity = {'created_at': now}
    result = DatetimeAdapter.normalize_dict_datetimes(entity)
    print(f"\nAfter normalize_dict_datetimes:")
    print(f"Result: {result}")
    print(f"Result value: {result['created_at']}")
    print(f"Ends with Z: {result['created_at'].endswith('Z')}")
    
if __name__ == "__main__":
    debug_datetime_issue()
