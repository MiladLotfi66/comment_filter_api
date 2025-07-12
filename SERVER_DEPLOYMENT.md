# راهنمای نصب API فیلتر کامنت در سرور

این راهنما مراحل نصب و راه‌اندازی API فیلتر کامنت را در یک سرور لینوکس توضیح می‌دهد.

## پیش‌نیازها

- سرور لینوکس (ترجیحاً Ubuntu 20.04 یا بالاتر)
- دسترسی SSH به سرور
- دسترسی root یا دسترسی sudo
- دامنه یا زیردامنه برای API (مثلاً api.nibero.ir)

## مراحل نصب

### 1. کلون کردن مخزن

```bash
# نصب git اگر نصب نیست
sudo apt-get update
sudo apt-get install -y git

# کلون کردن مخزن
git clone https://github.com/MiladLotfi66/comment_filter_api.git
cd comment_filter_api
```

### 2. اجرای اسکریپت راه‌اندازی

```bash
# اعطای دسترسی اجرا به اسکریپت
chmod +x server_setup.sh

# اجرای اسکریپت
./server_setup.sh
```

### 3. ویرایش فایل .env

```bash
# ویرایش فایل .env با تنظیمات مناسب
nano .env
```

### 4. نصب و پیکربندی Nginx

```bash
# نصب Nginx
sudo apt-get install -y nginx

# کپی فایل پیکربندی
sudo cp nginx_config.conf /etc/nginx/sites-available/api.nibero.ir.conf

# ایجاد لینک سمبلیک
sudo ln -s /etc/nginx/sites-available/api.nibero.ir.conf /etc/nginx/sites-enabled/

# بررسی پیکربندی
sudo nginx -t

# راه‌اندازی مجدد Nginx
sudo systemctl restart nginx
```

### 5. نصب و پیکربندی SSL (اختیاری اما توصیه می‌شود)

```bash
# نصب Certbot
sudo apt-get install -y certbot python3-certbot-nginx

# دریافت گواهی SSL
sudo certbot --nginx -d api.nibero.ir

# راه‌اندازی مجدد Nginx
sudo systemctl restart nginx
```

### 6. راه‌اندازی سرویس API

```bash
# کپی فایل سرویس
sudo cp comment_filter.service /etc/systemd/system/

# بارگذاری مجدد systemd
sudo systemctl daemon-reload

# فعال‌سازی سرویس
sudo systemctl enable comment_filter.service

# شروع سرویس
sudo systemctl start comment_filter.service

# بررسی وضعیت سرویس
sudo systemctl status comment_filter.service
```

### 7. تنظیم فایروال

```bash
# باز کردن پورت‌های HTTP و HTTPS
sudo ufw allow 80
sudo ufw allow 443
```

## بررسی نصب

برای بررسی نصب، می‌توانید یک درخواست تست ارسال کنید:

```bash
curl -X POST "https://api.nibero.ir/filter-comment" \
  -H "Content-Type: application/json" \
  -H "Origin: https://nibero.ir" \
  -d '{"text": "این یک کامنت تست است"}'
```

پاسخ مورد انتظار:

```json
{"is_approved": true, "reason": null}
```

## عیب‌یابی

### سرویس API اجرا نمی‌شود

بررسی لاگ‌ها:

```bash
sudo journalctl -u comment_filter.service
```

### مشکلات Nginx

بررسی لاگ‌های Nginx:

```bash
sudo tail -f /var/log/nginx/api.nibero.ir.error.log
```

### مشکلات SSL

بررسی وضعیت گواهی‌ها:

```bash
sudo certbot certificates
```

## به‌روزرسانی API

برای به‌روزرسانی API به آخرین نسخه:

```bash
cd comment_filter_api
git pull
sudo systemctl restart comment_filter.service
```

## پشتیبان‌گیری

برای پشتیبان‌گیری از تنظیمات:

```bash
# پشتیبان‌گیری از فایل .env
cp .env .env.backup

# پشتیبان‌گیری از پیکربندی Nginx
sudo cp /etc/nginx/sites-available/api.nibero.ir.conf ~/api.nibero.ir.conf.backup
```
