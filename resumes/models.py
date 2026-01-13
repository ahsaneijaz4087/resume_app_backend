from django.db import models

class ResumeAnalysis(models.Model):
    cv_filename = models.CharField(max_length=255)
    job_description = models.TextField(blank=True)
    analysis_result = models.JSONField()
    overall_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis for {self.cv_filename}"