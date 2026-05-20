from django.db import models
from django.core.validators import FileExtensionValidator

class Document(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان سند")
    file = models.FileField(
        upload_to='docs/', 
        verbose_name="فایل سند",
        validators=[FileExtensionValidator(allowed_extensions=['docx', 'pdf', 'txt'])]
    )
    content = models.TextField(blank=True, null=True, verbose_name="متن کامل استخراج شده")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ آپلود")

    class Meta:
        verbose_name = "سند"
        verbose_name_plural = "اسناد"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        is_new = self.pk is None 
        file_changed = False

        if not is_new:
            old_document = Document.objects.get(pk=self.pk)
            if old_document.file != self.file:
                file_changed = True

        super().save(*args, **kwargs)

        from .ai_utils import process_and_store_document, delete_document_from_chroma

        # اگر فایل در حال ویرایش تغییر کرده بود، اول دیتای قبلی رو پاک کن
        if file_changed:
            delete_document_from_chroma(self.pk)
            if old_document.file:
                old_document.file.delete(save=False) # پاک کردن فایل قدیمی از هارد

        if (is_new or file_changed) and self.file:
            # اینجا آیدی سند رو هم به تابع پاس میدیم
            extracted_text = process_and_store_document(self.file.path, self.pk)
            self.content = extracted_text
            super().save(update_fields=['content'])

    # تغییر مهم: تابع حذف کامل (دیتابیس + فایل + ChromaDB)
    def delete(self, *args, **kwargs):
        from .ai_utils import delete_document_from_chroma
        
        # ۱. حذف بردارها از هوش مصنوعی
        delete_document_from_chroma(self.pk)
        
        # ۲. حذف فایل فیزیکی از روی هارد دیسک
        if self.file:
            self.file.delete(save=False)
            
        # ۳. حذف از دیتابیس جنگو
        super().delete(*args, **kwargs)

class QAHistory(models.Model):
    # (کدهای این بخش دست نخورده باقی ماند)
    question = models.TextField(verbose_name="پرسش کاربر")
    answer = models.TextField(verbose_name="پاسخ هوش مصنوعی")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")

    class Meta:
        verbose_name = "تاریخچه پرسش"
        verbose_name_plural = "تاریخچه پرسش‌ها"

    def __str__(self):
        return self.question[:50]