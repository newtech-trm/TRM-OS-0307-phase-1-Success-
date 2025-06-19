# Hướng dẫn cho phiên làm việc tiếp theo

## Bối cảnh hiện tại
- Đã hoàn thành việc sửa lỗi async mocks trong tất cả các file test relationship
- Tất cả 99 test trong thư mục tests/unit/ đã chạy thành công
- Đã thiết lập pattern chuẩn cho việc mock các phương thức async và async context manager

## Pattern đã thiết lập cho mock async
```python
# Cấu hình mock để hỗ trợ async context manager
mock_session_ctx = MagicMock()
mock_session_ctx.__aenter__ = AsyncMock(return_value=mock_session)
mock_session_ctx.__aexit__ = AsyncMock(return_value=None)
mock_db = MagicMock()
mock_db.session.return_value = mock_session_ctx
# Biến _get_db thành AsyncMock để có thể sử dụng với await
mock_get_db.side_effect = AsyncMock(return_value=mock_db)
```

## Nhiệm vụ tiếp theo
1. **Tiếp tục triển khai ontology-first theo kế hoạch**:
   - Xem lại file `@trmos-sumary-documentation.md` để nắm rõ tổng quan hệ thống
   - Tuân thủ thiết kế trong file `@ONTOLOGY NỘI BỘ TRM - BẢN THIẾT KẾ THỐNG NHẤT HOÀN CHỈNH V3.2.md`
   - Cập nhật `@GAP_ANALYSIS_ONTOLOGY_V3.2.md` sau mỗi phiên làm việc

2. **Cải thiện chất lượng code**:
   - Áp dụng pattern async mock đã thiết lập cho các file test mới
   - Xem xét cập nhật các cảnh báo liên quan đến Pydantic (chuyển từ class-based config sang ConfigDict)
   - Xem xét cập nhật cấu hình pytest-asyncio để tránh cảnh báo về asyncio_default_fixture_loop_scope

3. **Phát triển tính năng mới**:
   - Tiếp tục phát triển các relationship và endpoint theo ontology
   - Đảm bảo mỗi tính năng mới đều có test đầy đủ
   - Tuân thủ nguyên tắc ontology-first trong mọi phát triển

## Lưu ý quan trọng
- Nghiêm cấm mock/demo/fake
- Không được cứ lỗi là đơn giản hóa, mà phải giữ nguyên mục đích là final fully product, accuracy
- Luôn đảm bảo thực sự liên thông giữa các service
- Trong lúc thực hiện, luôn cập nhật `@GAP_ANALYSIS_ONTOLOGY_V3.2.md` GAP analysis mỗi khi xong một đoạn dài các việc
- Cập nhật plan nhằm giúp cho phiên làm việc sau hiểu rõ bối cảnh và tiến độ
