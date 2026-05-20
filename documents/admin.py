from django.contrib import admin
from .models import Document, QAHistory

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    readonly_fields = ('content',) # متن کامل رو فعلا فقط-خواندنی می‌کنیم چون قراره خودکار استخراج بشه

@admin.register(QAHistory)
class QAHistoryAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at')
    readonly_fields = ('question', 'answer') # تاریخچه نباید دستی ویرایش بشه