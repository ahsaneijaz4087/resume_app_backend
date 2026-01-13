# resume/urls.py
from django.urls import path
from .views import ResumeAnalyzerView

app_name = 'resumes'  # ← optional but recommended

urlpatterns = [
    path('analyze/', ResumeAnalyzerView.as_view(), name='analyze_resume'),
]