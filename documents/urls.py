from django.urls import path
from .views import AskQuestionAPIView

urlpatterns = [
    path('ask/', AskQuestionAPIView.as_view(), name='ask_question'),
]