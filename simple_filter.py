"""
ساده‌ترین نسخه از API فیلتر کامنت برای وبسایت nibero.ir
این نسخه فقط از کتابخانه‌های استاندارد پایتون استفاده می‌کند
"""

import re
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import socket

# لیست کلمات ممنوعه (این فقط یک مثال است و باید با لیست واقعی جایگزین شود)
INAPPROPRIATE_WORDS = [
    "فحش",
    "توهین",
    "کلمه_نامناسب",
    # کلمات رکیک
    "لعنتی",
    "احمق",
    # کلمات سیاسی حساس
    "انقلاب",
    "اعتراض",
    "تحریم",
    # کلمات توهین‌آمیز
    "بی‌شعور",
    "نادان",
    "ابله",
    # اینجا کلمات بیشتری اضافه کنید
]

def contains_inappropriate_content(text):
    """
    بررسی می‌کند که آیا متن شامل محتوای نامناسب است یا خیر
    """
    # تبدیل به حروف کوچک برای مطابقت بدون توجه به حالت حروف
    text_lower = text.lower()
    
    # بررسی کلمات نامناسب
    for word in INAPPROPRIATE_WORDS:
        if word in text_lower:
            return True, f"شامل زبان نامناسب است"
    
    # بررسی طول متن
    if len(text) < 2:
        return True, "کامنت خیلی کوتاه است"
        
    return False, None

class CommentFilterHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """پاسخ به درخواست‌های OPTIONS برای CORS"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "https://nibero.ir")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Max-Age", "86400")  # 24 ساعت
        self.end_headers()
    
    def do_POST(self):
        """پاسخ به درخواست‌های POST"""
        # بررسی آدرس درخواست
        if self.path != "/filter-comment":
            self.send_error(404, "مسیر مورد نظر یافت نشد")
            return
        
        # بررسی منشا درخواست (Origin)
        origin = self.headers.get("Origin", "")
        if not origin.endswith("nibero.ir"):
            self.send_error(403, "دسترسی ممنوع: منشا نامعتبر")
            return
        
        # خواندن داده‌های درخواست
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")
        
        try:
            # تبدیل داده‌های JSON به دیکشنری پایتون
            data = json.loads(post_data)
            
            # بررسی وجود فیلد متن
            if "text" not in data:
                self.send_error(400, "فیلد text در درخواست یافت نشد")
                return
            
            # بررسی محتوای نامناسب
            is_inappropriate, reason = contains_inappropriate_content(data["text"])
            
            # ایجاد پاسخ
            response = {
                "is_approved": not is_inappropriate,
                "reason": reason
            }
            
            # ارسال پاسخ
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "https://nibero.ir")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
            
        except json.JSONDecodeError:
            self.send_error(400, "داده‌های JSON نامعتبر")
        except Exception as e:
            self.send_error(500, f"خطای سرور: {str(e)}")

def run_server(host="0.0.0.0", port=8000):
    """راه‌اندازی سرور HTTP"""
    server_address = (host, port)
    httpd = HTTPServer(server_address, CommentFilterHandler)
    print(f"سرور در آدرس http://{host}:{port} در حال اجراست...")
    httpd.serve_forever()

if __name__ == "__main__":
    # بررسی پورت در دسترس
    port = 8000
    max_port = 8010  # حداکثر پورت برای امتحان
    
    while port <= max_port:
        try:
            run_server(port=port)
            break
        except socket.error:
            print(f"پورت {port} در دسترس نیست. امتحان پورت بعدی...")
            port += 1
    
    if port > max_port:
        print("هیچ پورت در دسترسی یافت نشد.")
