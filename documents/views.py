from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .ai_utils import get_answer_from_ai
from .models import QAHistory

class AskQuestionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        question = request.data.get('question')
        if not question:
            return Response({"error": "Question not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            answer = get_answer_from_ai(question)
            # ذخیره تاریخچه
            QAHistory.objects.create(question=question, answer=answer)
            return Response({"answer": answer}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)