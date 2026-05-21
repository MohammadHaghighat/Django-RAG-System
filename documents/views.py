from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .ai_utils import get_answer_from_ai
from .models import QAHistory, Document

# ۱. نمایش صفحه چت و تاریخچه
def chat_view(request):
    history = QAHistory.objects.all().order_by('created_at')
    
    chat_history = []
    for item in history:
        chat_history.append({
            "question": item.question,
            "answer": item.answer,
            "sources": item.sources or [], 
            "prompt": item.prompt or ""
        })
        
    return render(request, 'documents/chat.html', {'chat_history': chat_history})

# ۲. API پرسش و پاسخ
class AskQuestionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        question = request.data.get('question')
        if not question:
            return Response({"error": "Question not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # دریافت پاسخ از هوش مصنوعی
            result = get_answer_from_ai(question)
            
            # استخراج اسم اسناد واقعی از روی آیدی‌ها
            source_names = []
            for source_id_str in result.get("sources", []):
                try:
                    doc_id = int(source_id_str.split(" ")[-1])
                    document = Document.objects.get(pk=doc_id)
                    source_names.append(document.title)
                except (ValueError, Document.DoesNotExist):
                    continue
            
            # === فقط و فقط یک بار ذخیره کامل در دیتابیس ===
            QAHistory.objects.create(
                question=question,
                answer=result["answer"],
                sources=source_names,
                prompt=result["prompt"]
            )
            # ============================================

            final_response = {
                "answer": result["answer"],
                "sources": source_names,
                "prompt": result["prompt"]
            }
            
            return Response(final_response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)