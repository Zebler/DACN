📅 PERSONAL SCHEDULE ASSISTANT (DACN)

Giới thiệu

Personal Schedule Assistant là một ứng dụng trợ lý cá nhân giúp người dùng tạo lịch trình một cách nhanh chóng và tự nhiên bằng ngôn ngữ tiếng Việt. Ứng dụng sử dụng kỹ thuật Xử lý Ngôn ngữ Tự nhiên (NLP) kết hợp giữa trích xuất dựa trên luật (Rule-based) và trích xuất thực thể (NER) để phân tích câu lệnh đầu vào của người dùng, tự động xác định Tên sự kiện, Thời gian, Địa điểm và Thời gian nhắc nhở.

Dự án được xây dựng với giao diện người dùng đơn giản bằng Tkinter và hỗ trợ tính năng nhắc nhở (sử dụng thư viện plyer).

✨ Tính năng chính

Xử lý Ngôn ngữ Tự nhiên (NLP): Phân tích cú pháp tiếng Việt tự nhiên (Ví dụ: "Họp nhóm 10 giờ sáng mai ở phòng 302").
Trích xuất thông tin: Tự động xác định và trích xuất các thành phần:

Sự kiện (event)
Thời gian bắt đầu (start_time - định dạng ISO 8601)
Địa điểm (location)
Thời gian nhắc nhở (reminder_minutes)
Đánh giá độ tin cậy (Confidence Score): Cung cấp điểm tin cậy cho mỗi lịch trình được tạo ra, giúp người dùng đánh giá chất lượng của kết quả phân tích.
Giao diện người dùng (GUI): Giao diện đồ họa đơn giản, trực quan (Tkinter) để thêm, xem, tìm kiếm và xóa lịch trình.
Lưu trữ cục bộ: Lưu trữ lịch trình dưới dạng file JSON (data/schedules.json).
Hệ thống nhắc nhở: Hiển thị thông báo (pop-up) trước thời gian diễn ra sự kiện.

🛠️ Cài đặt và Khởi chạy

Yêu cầu Python 3.x.

Clone repository (Nếu có):

git clone <URL_repository_của_bạn>
cd <tên_thư_mục>


Tạo môi trường ảo (Khuyến nghị):

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows


Cài đặt dependencies:

pip install -r requirements.txt


🚀 Hướng dẫn sử dụng

Cách 1: Chạy trực tiếp từ mã nguồn

Chạy ứng dụng bằng cách thực thi file main.py:

python main.py

Cách 2: Đóng gói lại thành 1 file thực thi duy nhất
2.1: tạo file build.spec và đsao chép đoạn code dưới vào

import os
import underthesea
underthesea_path = os.path.dirname(underthesea.__file__)

underthesea_all_data = [(underthesea_path, 'underthesea')]

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src', 'src'),
        ('gui', 'gui'),
        # File dữ liệu của dự án
        ('data/schedules.json', 'data'),
        ('icon.ico', '.'),
    ] + underthesea_all_data,
    hiddenimports=[
        # Khai báo thủ công các imports ẩn cần thiết
        'src.core.scheduler',
        'src.nlp.preprocessor',
        'src.nlp.ner_extractor',
        'src.nlp.rule_extractor',
        'src.nlp.patterns',
        'src.core.parser',
        'src.core.validator',
        'src.storage.json_storage',
        'src.utils.time_utils',
        'pytz',
        'underthesea', 
        'underthesea.models', 
        'underthesea.pos',
        'underthesea.ner',
        'underthesea.train'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ScheduleAssistant',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False, # Ẩn cửa sổ console (vì là ứng dụng GUI)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' 
)
```

#### 2.2 Chạy lệnh đóng gói

Sử dụng file `build.spec` đã tạo để đóng gói ứng dụng:

```bash
pyinstaller build.spec
```

#### 2.3. Kết quả

File EXE (`ScheduleAssistant.exe`) sẽ được tạo trong thư mục **`dist/`**. Bạn có thể chạy file này trực tiếp.
