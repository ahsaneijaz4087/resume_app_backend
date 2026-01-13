from django.db import models

class MatchedJob(models.Model):
    resume_text = models.TextField()
    title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    url = models.URLField(blank=True)
    similarity_score = models.FloatField()
    is_applied = models.BooleanField(default=False)  # ✅ NEW
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

