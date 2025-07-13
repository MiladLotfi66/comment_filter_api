"""
فایل تست برای بررسی کامنت‌های نامناسب
"""

import re
import json

# لیست کلمات ممنوعه (گسترش یافته)
INAPPROPRIATE_WORDS = [
    "فحش",
    "توهین",
    "کلمه_نامناسب",
    # کلمات رکیک
    "لعنتی",
    "احمق",
    "کیر",
    "کس",
    "کون",
    "جنده",
    "گاییدن",
    "کیری",
    "کصکش",
    # کلمات سیاسی حساس
    "انقلاب",
    "اعتراض",
    "تحریم",
    "خامنه ای",
    "رهبر",
    "رئیسی",
    "روحانی",
    "احمدی نژاد",
    "نظام",
    "جمهوری اسلامی",
    "براندازی",
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
            return True, f"شامل زبان نامناسب است (کلمه: {word})"
    
    # بررسی طول متن
    if len(text) < 2:
        return True, "کامنت خیلی کوتاه است"
        
    return False, None

def test_comment(comment_text):
    """
    تست یک کامنت و نمایش نتیجه
    """
    print(f"کامنت: {comment_text}")
    is_inappropriate, reason = contains_inappropriate_content(comment_text)
    
    if is_inappropriate:
        print(f"نتیجه: رد شد - {reason}")
    else:
        print("نتیجه: تایید شد")
    print("-" * 50)

# تست کامنت‌ها
if __name__ == "__main__":
    test_comment("این یک کامنت مناسب است")
    test_comment("کیرم تو کیفیت جنساتون")
    test_comment("این محصول خیلی بی‌کیفیت است")
    test_comment("لعنتی چقدر گرون شده")
    test_comment("احمق خودتی")
    test_comment("خامنه ای مرد خوبی نیست") 