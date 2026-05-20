from django.urls import path
from .views import AskQuestionAPIView, chat_view

urlpatterns = [
    # آدرس صفحه چت (فرانت‌اند)
    path('chat/', chat_view, name='chat_view'),
    
    # آدرس API (همون قبلی)
    path('ask/', AskQuestionAPIView.as_view(), name='ask_question'),
]