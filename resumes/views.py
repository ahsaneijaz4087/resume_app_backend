from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AnalysisSerializer
from .utils import perform_analysis
from .models import ResumeAnalysis  # Optional

class ResumeAnalyzerView(APIView):
    def post(self, request):
        serializer = AnalysisSerializer(data=request.data)
        if serializer.is_valid():
            cv_file = serializer.validated_data['cv']
            job_desc = serializer.validated_data.get('job_description', "")
            
            try:
                result = perform_analysis(cv_file, job_desc)
                
                # Optional: Save to PostgreSQL
                ResumeAnalysis.objects.create(
                    cv_filename=cv_file.name,
                    job_description=job_desc,
                    analysis_result=result,
                    overall_score=result['overall_score']
                )
                
                return Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)