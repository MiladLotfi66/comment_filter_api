# راهنمای استفاده از API فیلتر کامنت

این راهنما نحوه استفاده از API فیلتر کامنت را برای توسعه‌دهندگان وبسایت nibero.ir توضیح می‌دهد.

## مقدمه

API فیلتر کامنت یک سرویس برای بررسی خودکار کامنت‌های کاربران و فیلتر کردن محتوای نامناسب است. این API فقط به درخواست‌های ارسال شده از دامنه `nibero.ir` پاسخ می‌دهد.

## نقطه پایانی (Endpoint)

- **آدرس**: `https://api.nibero.ir/filter-comment`
- **متد**: `POST`
- **هدرها**:
  - `Content-Type: application/json`
  - `Origin: https://nibero.ir` (الزامی)

## ساختار درخواست

```json
{
  "text": "متن کامنت",
  "user_id": "شناسه کاربر (اختیاری)",
  "post_id": "شناسه پست (اختیاری)"
}
```

### پارامترها

- `text` (الزامی): متن کامنت برای بررسی
- `user_id` (اختیاری): شناسه کاربر ارسال‌کننده کامنت
- `post_id` (اختیاری): شناسه پست یا محتوایی که کامنت برای آن ارسال شده است

## ساختار پاسخ

```json
{
  "is_approved": true/false,
  "reason": "دلیل رد کامنت (در صورت رد شدن)"
}
```

### پارامترها

- `is_approved`: وضعیت تأیید کامنت (true = تأیید شده، false = رد شده)
- `reason`: دلیل رد کامنت (در صورت تأیید بودن، مقدار null خواهد بود)

## مثال‌ها

### مثال با JavaScript (Fetch API)

```javascript
async function checkComment(commentText) {
  try {
    const response = await fetch('https://api.nibero.ir/filter-comment', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Origin': 'https://nibero.ir'
      },
      body: JSON.stringify({
        text: commentText
      })
    });
    
    const result = await response.json();
    return result;
  } catch (error) {
    console.error('خطا در بررسی کامنت:', error);
    return { is_approved: false, reason: 'خطای سیستمی' };
  }
}

// نحوه استفاده
document.getElementById('comment-form').addEventListener('submit', async function(e) {
  e.preventDefault();
  
  const commentText = document.getElementById('comment-text').value;
  const result = await checkComment(commentText);
  
  if (result.is_approved) {
    // ذخیره کامنت در سیستم
    saveComment(commentText);
  } else {
    // نمایش پیام خطا به کاربر
    showError(`کامنت شما تأیید نشد: ${result.reason}`);
  }
});
```

### مثال با PHP

```php
function checkComment($commentText) {
  $url = 'https://api.nibero.ir/filter-comment';
  $data = array(
    'text' => $commentText
  );
  
  $options = array(
    'http' => array(
      'header'  => "Content-type: application/json\r\nOrigin: https://nibero.ir\r\n",
      'method'  => 'POST',
      'content' => json_encode($data)
    )
  );
  
  $context  = stream_context_create($options);
  $result = file_get_contents($url, false, $context);
  
  if ($result === FALSE) {
    return array('is_approved' => false, 'reason' => 'خطای سیستمی');
  }
  
  return json_decode($result, true);
}

// نحوه استفاده
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  $commentText = $_POST['comment_text'];
  $result = checkComment($commentText);
  
  if ($result['is_approved']) {
    // ذخیره کامنت در سیستم
    saveComment($commentText);
    echo "کامنت با موفقیت ثبت شد.";
  } else {
    // نمایش پیام خطا به کاربر
    echo "کامنت شما تأیید نشد: " . $result['reason'];
  }
}
```

## کدهای خطا

- **400**: درخواست نامعتبر (مثلاً فیلد `text` وجود ندارد)
- **403**: دسترسی ممنوع (Origin نامعتبر)
- **500**: خطای سرور

## محدودیت‌ها

- حداکثر طول متن کامنت: نامحدود
- حداکثر تعداد درخواست در دقیقه: نامحدود (ممکن است در آینده محدود شود)

## نکات امنیتی

1. همیشه هدر `Origin` را به درستی تنظیم کنید.
2. هرگز اطلاعات حساس را در متن کامنت ارسال نکنید.
3. همیشه از HTTPS برای ارتباط با API استفاده کنید.

## پشتیبانی

در صورت بروز مشکل یا نیاز به پشتیبانی، با آدرس ایمیل support@nibero.ir تماس بگیرید.
