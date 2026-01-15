# Ứng dụng Quản lý Doanh thu Doanh nghiệp

Ứng dụng Streamlit để quản lý và phân bổ doanh thu doanh nghiệp theo tháng.

## Tính năng

- ✅ Nhập thông tin doanh nghiệp (tên, mã số thuế, doanh thu năm trước)
- ✅ Nhập doanh thu thuần năm 2026
- ✅ Tự động chia doanh thu năm 2026 ra 12 tháng
- ✅ Chỉnh sửa doanh thu từng tháng thủ công
- ✅ Nhập yếu tố ảnh hưởng và ghi chú cho từng tháng
- ✅ Xuất dữ liệu ra file CSV và Excel

## Cài đặt

1. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

## Chạy ứng dụng

```bash
streamlit run app.py
```

Ứng dụng sẽ mở trong trình duyệt tại địa chỉ `http://localhost:8501`

## Sử dụng

1. Nhập thông tin doanh nghiệp ở sidebar bên trái:
   - Tên doanh nghiệp
   - Mã số thuế
   - Doanh thu thuần năm trước

2. Nhập doanh thu thuần năm 2026

3. Chọn cách phân bổ:
   - Chia đều 12 tháng: Tự động chia đều doanh thu
   - Nhập thủ công từng tháng: Điều chỉnh doanh thu cho từng tháng

4. Nhập yếu tố ảnh hưởng và ghi chú cho từng tháng

5. Nhấn "Lưu dữ liệu" để lưu thay đổi

6. Tải xuống dữ liệu dưới dạng CSV hoặc Excel

