#!/bin/bash

# اسکریپت نصب و راه‌اندازی API فیلتر کامنت برای سرور لینوکس
echo "شروع نصب و راه‌اندازی API فیلتر کامنت..."

# بررسی نصب بودن پایتون
if ! command -v python3 &> /dev/null; then
    echo "پایتون نصب نیست. در حال نصب پایتون..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip python3-venv
fi

# ایجاد محیط مجازی
echo "ایجاد محیط مجازی پایتون..."
python3 -m venv venv

# فعال‌سازی محیط مجازی
source venv/bin/activate

# نصب کتابخانه‌های مورد نیاز
echo "نصب کتابخانه‌های مورد نیاز..."
pip install -r requirements.txt

# ایجاد فایل .env از روی نمونه
if [ ! -f .env ]; then
    echo "ایجاد فایل .env..."
    cp .env.example .env
    echo "لطفاً فایل .env را با تنظیمات مناسب ویرایش کنید."
fi

# ایجاد فایل سرویس سیستمی
echo "ایجاد فایل سرویس سیستمی..."
cat > comment_filter.service << EOF
[Unit]
Description=Comment Filter API Service
After=network.target

[Service]
User=$(whoami)
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/venv/bin/python3 simple_filter.py
Restart=always
RestartSec=5
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=comment_filter

[Install]
WantedBy=multi-user.target
EOF

echo "برای نصب سرویس سیستمی، دستورات زیر را اجرا کنید:"
echo "sudo cp comment_filter.service /etc/systemd/system/"
echo "sudo systemctl daemon-reload"
echo "sudo systemctl enable comment_filter.service"
echo "sudo systemctl start comment_filter.service"

echo "نصب و راه‌اندازی به پایان رسید."
echo "برای اجرای دستی API: python3 simple_filter.py"
echo "برای بررسی وضعیت سرویس: sudo systemctl status comment_filter.service"
