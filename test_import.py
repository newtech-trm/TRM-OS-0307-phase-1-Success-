#!/usr/bin/env python
"""
Script kiểm tra import module
"""
import sys
sys.path.append('.')

try:
    print("Thử import trm_api...")
    import trm_api
    print("Import trm_api thành công")
    
    print("\nThử import trm_api.models...")
    import trm_api.models
    print("Import trm_api.models thành công")
    
    print("\nThử import trm_api.models.enums...")
    import trm_api.models.enums
    print("Import trm_api.models.enums thành công")
    print("Các enum có trong module:", dir(trm_api.models.enums))
    
    print("\nThử import trm_api.models.enums.TaskStatus...")
    from trm_api.models.enums import TaskStatus
    print("Import TaskStatus thành công")
    print("Các giá trị TaskStatus:", [status.value for status in TaskStatus])
    
except ImportError as e:
    print(f"Lỗi import: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"Lỗi khác: {e}")
    import traceback
    traceback.print_exc()
