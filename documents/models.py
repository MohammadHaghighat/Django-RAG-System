from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان سند")
    file = models.FileField(upload_to='docs/', verbose_name="فایل سند (docx)")
    content = models.TextField(blank=True, null=True, verbose_name="متن کامل استخراج شده")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ آپلود")

    class Meta:
        verbose_name = "سند"
        verbose_name_plural = "اسناد"

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # بررسی میکنیم که آیا این یک فایل جدید است؟
        is_new = self.pk is None 
        super().save(*args, **kwargs) # اول فایل رو ذخیره میکنیم تا روی هارد قرار بگیره

        # اگر فایل جدید بود و هنوز متنش استخراج نشده بود
        if is_new and self.file:
            from .ai_utils import process_and_store_document # ایمپورت فایل هوش مصنوعی
            
            # ارسال مسیر فایل برای پردازش
            extracted_text = process_and_store_document(self.file.path)
            
            # ذخیره متن استخراج شده در دیتابیس
            self.content = extracted_text
            self.save(update_fields=['content'])


class QAHistory(models.Model):
    question = models.TextField(verbose_name="پرسش کاربر")
    answer = models.TextField(verbose_name="پاسخ هوش مصنوعی")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")

    class Meta:
        verbose_name = "تاریخچه پرسش"
        verbose_name_plural = "تاریخچه پرسش‌ها"

    def __str__(self):
        return self.question[:50]