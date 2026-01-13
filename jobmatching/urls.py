from django.urls import path
from .views import match_jobs

urlpatterns = [
    path("match-jobs/", match_jobs, name="match_jobs"),
]

