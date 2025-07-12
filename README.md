# API فیلتر کامنت برای وبسایت Nibero.ir

این API برای فیلتر کردن کامنت‌های نامناسب طراحی شده است. این سرویس فقط به درخواست‌های ارسال شده از دامنه `nibero.ir` پاسخ می‌دهد و کامنت‌های حاوی کلمات ممنوعه، رکیک، سیاسی، توهین‌آمیز و غیره را رد می‌کند.

## نسخه‌های موجود

دو نسخه از این API وجود دارد:

1. **نسخه کامل (main.py)**: این نسخه از کتابخانه‌های FastAPI و Transformers استفاده می‌کند و امکان استفاده از مدل‌های هوش مصنوعی برای تشخیص محتوای نامناسب را فراهم می‌کند.

2. **نسخه ساده (simple_filter.py)**: این نسخه فقط از کتابخانه‌های استاندارد پایتون استفاده می‌کند و برای محیط‌هایی که امکان نصب کتابخانه‌های خارجی وجود ندارد مناسب است.

## نصب و راه‌اندازی

### پیش‌نیازها

- پایتون 3.6 یا بالاتر

### نصب کتابخانه‌ها (برای نسخه کامل)

```bash
# ایجاد محیط مجازی
python3 -m venv venv

# فعال‌سازی محیط مجازی
source venv/bin/activate  # در لینوکس/مک
# یا
venv\\Scripts\\activate  # در ویندوز

# نصب کتابخانه‌ها
pip install -r requirements.txt
```

### اجرای API

#### نسخه کامل

```bash
python main.py
```

#### نسخه ساده

```bash
python simple_filter.py
```

## استفاده از API

### نقطه پایانی (Endpoint)

- **آدرس**: `/filter-comment`
- **متد**: `POST`
- **هدرها**:
  - `Content-Type: application/json`
  - `Origin: https://nibero.ir` (الزامی)

### ساختار درخواست

```json
{
  "text": "متن کامنت",
  "user_id": "شناسه کاربر (اختیاری)",
  "post_id": "شناسه پست (اختیاری)"
}
```

### ساختار پاسخ

```json
{
  "is_approved": true/false,
  "reason": "دلیل رد کامنت (در صورت رد شدن)"
}
```

## مثال‌ها

### کامنت مناسب

درخواست:
```bash
curl -X POST "http://localhost:8000/filter-comment" \
  -H "Content-Type: application/json" \
  -H "Origin: https://nibero.ir" \
  -d '{"text": "این یک کامنت مناسب است"}'
```

پاسخ:
```json
{
  "is_approved": true,
  "reason": null
}
```

### کامنت نامناسب

درخواست:
```bash
curl -X POST "http://localhost:8000/filter-comment" \
  -H "Content-Type: application/json" \
  -H "Origin: https://nibero.ir" \
  -d '{"text": "این کامنت حاوی کلمه فحش است"}'
```

پاسخ:
```json
{
  "is_approved": false,
  "reason": "شامل زبان نامناسب است"
}
```

## شخصی‌سازی

برای اضافه کردن کلمات ممنوعه بیشتر، لیست `INAPPROPRIATE_WORDS` را در فایل `simple_filter.py` یا `main.py` ویرایش کنید.

## ارتقاء سیستم

برای استفاده از مدل‌های پیشرفته‌تر تشخیص محتوای نامناسب، می‌توانید از مدل‌های آماده در Hugging Face استفاده کنید. برای این کار، بخش مربوط به `contains_inappropriate_content` در فایل `main.py` را از حالت کامنت خارج کنید و یک مدل مناسب برای زبان فارسی انتخاب کنید. 