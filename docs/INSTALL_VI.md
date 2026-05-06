# Hướng dẫn cài đặt — TCS-COMMUNITY (gói pip: `tcs-macro-pulse`)

> Tài liệu tiếng Việt cho người dùng VN. English version: see [`README.md`](../README.md).
>
> _Repo đổi tên 07/05/2026: `tcs-macro-pulse` → `TCS-COMMUNITY`. Tên gói pip vẫn là `tcs-macro-pulse` để không phá vỡ user đã cài._

## 1. Yêu cầu hệ thống

- Python **3.11** hoặc mới hơn
- Hệ điều hành: Windows / macOS / Linux
- Kết nối Internet (để gọi API FRED, GDACS, ACLED…)
- (Tuỳ chọn) Tài khoản FRED API miễn phí — đăng ký tại https://fred.stlouisfed.org/docs/api/api_key.html

## 2. Cài đặt nhanh

### Cách A — qua pip (khuyến nghị)

```bash
pip install tcs-macro-pulse
```

### Cách B — từ source

```bash
git clone https://github.com/TCS-PLATFORM-OFFICIAL/TCS-COMMUNITY.git
cd tcs-macro-pulse
pip install -e .
```

### Cách C — môi trường ảo (sạch nhất)

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -U pip
pip install tcs-macro-pulse
```

## 3. Chạy thử

### 3.1 Lấy dữ liệu vĩ mô FRED

```bash
python -m tcs_macro_pulse.fetchers.fred --output macro.json
```

Kết quả mẫu:

```json
{
  "fed_funds_rate": 5.33,
  "cpi_yoy": 3.4,
  "unemployment": 3.9,
  "gdp_growth": 2.8
}
```

### 3.2 Lấy thiên tai GDACS 30 ngày qua

```bash
python -m tcs_macro_pulse.fetchers.gdacs --days 30 --output disasters.json
```

### 3.3 Pipeline đầy đủ (kết hợp 3 nguồn)

```bash
python examples/full_pipeline.py
```

## 4. Cấu hình API key (nếu cần)

Tạo file `.env` ở thư mục dự án:

```env
FRED_API_KEY=abc123...
ACLED_USERNAME=your_email@example.com
ACLED_PASSWORD=your_password
```

> ⚠️ **Tuyệt đối không commit file `.env`** lên Git. Đã có sẵn trong `.gitignore`.

## 5. Sự cố thường gặp

| Lỗi | Nguyên nhân | Cách xử lý |
|---|---|---|
| `ModuleNotFoundError: No module named 'tcs_macro_pulse'` | Chưa `pip install` | Chạy lại `pip install tcs-macro-pulse` |
| `requests.exceptions.Timeout` | Mạng chậm hoặc API down | Tăng timeout: thêm `--timeout 60` |
| `403 Forbidden` từ ACLED | Sai username/password | Kiểm tra `.env`; đăng ký lại ở acleddata.com |
| `429 Too Many Requests` | Vượt rate limit | Chờ 60 giây rồi thử lại |

## 6. Bước kế tiếp

- 📖 Đọc [`README.md`](../README.md) để xem ví dụ Python API.
- 💬 Tham gia [Discussions](https://github.com/TCS-PLATFORM-OFFICIAL/TCS-COMMUNITY/discussions) hỏi đáp.
- 🎁 Star repo + mở [Trial Request issue](https://github.com/TCS-PLATFORM-OFFICIAL/TCS-COMMUNITY/issues/new?template=trial-request.md) để nhận **30 ngày Pro** miễn phí.
- 🌐 Trải nghiệm full TCS-PLATFORM tại https://tcs-platform-rust.vercel.app
