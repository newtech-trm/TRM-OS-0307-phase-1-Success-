import sys
import os
import unittest

def setup_env():
    # Đảm bảo thư mục hiện tại nằm trong Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

def run_tests():
    # Import test modules
    from tests.unit.test_task_resolves_tension_relationship import TestTaskResolvesTensionRelationship
    from tests.unit.test_tension_leads_to_win_relationship import TestTensionLeadsToWinRelationship
    
    # Tạo test suite
    test_suite = unittest.TestSuite()
    
    # Thêm tất cả test cases từ TestTaskResolvesTensionRelationship
    task_tension_tests = unittest.TestLoader().loadTestsFromTestCase(TestTaskResolvesTensionRelationship)
    test_suite.addTest(task_tension_tests)
    
    # Thêm tất cả test cases từ TestTensionLeadsToWinRelationship
    tension_win_tests = unittest.TestLoader().loadTestsFromTestCase(TestTensionLeadsToWinRelationship)
    test_suite.addTest(tension_win_tests)
    
    # Chạy tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # In kết quả
    print(f"\nTest Results:")
    print(f"Ran {result.testsRun} tests")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    # Hiển thị chi tiết failure (nếu có)
    if result.failures:
        print("\nFailure details:")
        for failure in result.failures:
            print(f"\nTest: {failure[0]}")
            print(f"Error: {failure[1]}")
    
    # Hiển thị chi tiết errors (nếu có)
    if result.errors:
        print("\nError details:")
        for error in result.errors:
            print(f"\nTest: {error[0]}")
            print(f"Error: {error[1]}")
    
    # Trả về mã trạng thái đúng dựa trên kết quả test
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    setup_env()
    sys.exit(run_tests())
