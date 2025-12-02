# 📅 PERSONAL SCHEDULE ASSISTANT (DACN)

## Giới thiệu

**Personal Schedule Assistant** là một ứng dụng trợ lý cá nhân giúp người dùng tạo lịch trình một cách nhanh chóng và tự nhiên bằng ngôn ngữ tiếng Việt. Ứng dụng sử dụng kỹ thuật Xử lý Ngôn ngữ Tự nhiên (NLP) kết hợp giữa trích xuất dựa trên luật (Rule-based) và trích xuất thực thể (NER) để phân tích câu lệnh đầu vào của người dùng, tự động xác định Tên sự kiện, Thời gian, Địa điểm và Thời gian nhắc nhở.

Dự án được xây dựng với giao diện người dùng đơn giản bằng Tkinter và hỗ trợ tính năng nhắc nhở (sử dụng thư viện `plyer`).

## ✨ Tính năng chính

* **Xử lý Ngôn ngữ Tự nhiên (NLP):** Phân tích cú pháp tiếng Việt tự nhiên (Ví dụ: "Họp nhóm 10 giờ sáng mai ở phòng 302").
* **Trích xuất thông tin:** Tự động xác định và trích xuất các thành phần:
    * **Sự kiện** (`event`)
    * **Thời gian bắt đầu** (`start_time` - định dạng ISO 8601)
    * **Địa điểm** (`location`)
    * **Thời gian nhắc nhở** (`reminder_minutes`)
* **Đánh giá độ tin cậy (Confidence Score):** Cung cấp điểm tin cậy cho mỗi lịch trình được tạo ra, giúp người dùng đánh giá chất lượng của kết quả phân tích.
* **Giao diện người dùng (GUI):** Giao diện đồ họa đơn giản, trực quan (Tkinter) để thêm, xem, tìm kiếm và xóa lịch trình.
* **Lưu trữ cục bộ:** Lưu trữ lịch trình dưới dạng file JSON (`data/schedules.json`).
* **Hệ thống nhắc nhở:** Hiển thị thông báo (pop-up) trước thời gian diễn ra sự kiện.

## 🛠️ Cài đặt

Yêu cầu Python 3.x.

1.  **Clone repository (Nếu có):**
    ```bash
    git clone <URL_repository_của_bạn>
    cd <tên_thư_mục>
    ```

2.  **Tạo môi trường ảo (Khuyến nghị):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate     # Windows
    ```

3.  **Cài đặt dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Hướng dẫn sử dụng

Chạy ứng dụng bằng cách thực thi file `main.py`:

```bash
python main.py