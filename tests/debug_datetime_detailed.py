from datetime import datetime, timezone
import sys
import os
import json

# Thêm đường dẫn project vào sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from trm_api.adapters.data_adapters import DatetimeAdapter

def debug_normalize_dict_datetimes():
    now = datetime.now(timezone.utc)
    
    # Kiểm tra trường hợp 1: List datetime trực tiếp
    case1 = {
        'date_list': [now, now, now]
    }
    print("\nTrường hợp 1: List datetime trực tiếp")
    print(f"Input: {case1}")
    result1 = DatetimeAdapter.normalize_dict_datetimes(case1)
    print(f"Output: {result1}")
    print(f"Kiểu dữ liệu phần tử đầu tiên: {type(result1['date_list'][0])}")
    
    # Kiểm tra trường hợp 2: List datetime và string hỗn hợp
    case2 = {
        'mixed_list': [now, 'string1', now, 123]
    }
    print("\nTrường hợp 2: List hỗn hợp")
    print(f"Input: {case2}")
    result2 = DatetimeAdapter.normalize_dict_datetimes(case2)
    print(f"Output: {result2}")
    
    # Kiểm tra trường hợp 3: Danh sách trống
    case3 = {
        'empty_list': []
    }
    print("\nTrường hợp 3: Danh sách trống")
    print(f"Input: {case3}")
    result3 = DatetimeAdapter.normalize_dict_datetimes(case3)
    print(f"Output: {result3}")
    
    # Kiểm tra trường hợp 4: Các trường hợp lồng nhau phức tạp
    case4 = {
        'nested': {
            'list_of_lists': [
                [now, now],
                [{'date': now}, {'date': now}]
            ],
            'dict_with_list': {
                'dates': [now, now]
            }
        }
    }
    print("\nTrường hợp 4: Các cấu trúc lồng nhau phức tạp")
    try:
        result4 = DatetimeAdapter.normalize_dict_datetimes(case4)
        print(f"Output (thành công): {result4}")
    except Exception as e:
        print(f"Output (lỗi): {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_normalize_dict_datetimes()
