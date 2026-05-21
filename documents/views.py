from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .ai_utils import get_answer_from_ai
from .models import QAHistory, Document

# این تابع جدید برای نمایش صفحه چت است
def chat_view(request):
    # خواندن تمام تاریخچه از دیتابیس به ترتیب زمان
    history = QAHistory.objects.all().order_by('created_at')
    
    # تبدیل به یک لیست برای ارسال به فرانت‌اند
    chat_history = []
    for item in history:
        chat_history.append({
            "question": item.question,
            "answer": item.answer
        })
        
    # ارسال لیست تاریخچه به قالب HTML
    return render(request, 'documents/chat.html', {'chat_history': chat_history})

class AskQuestionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        question = request.data.get('question')
        if not question:
            return Response({"error": "Question not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # result الان یک دیکشنری کامل است
            result = get_answer_from_ai(question)
            
            # برای ذخیره در تاریخچه، فقط جواب رو نیاز داریم
            QAHistory.objects.create(question=question, answer=result["answer"])

            # برای نمایش اسم سند، باید از دیتابیس بگیریمش
            source_names = []
            for source_id_str in result.get("sources", []):
                try:
                    # استخراج آیدی عددی از "سند شماره X"
                    doc_id = int(source_id_str.split(" ")[-1])
                    document = Document.objects.get(pk=doc_id)
                    source_names.append(document.title)
                except (ValueError, Document.DoesNotExist):
                    continue

            # دیکشنری نهایی برای ارسال به فرانت‌اند
            final_response = {
                "answer": result["answer"],
                "sources": source_names,
                "prompt": result["prompt"]
            }
            
            return Response(final_response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)