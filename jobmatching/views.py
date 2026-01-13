from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
from .models import MatchedJob
@csrf_exempt
def get_saved_jobs(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET method required"}, status=400)

    jobs = MatchedJob.objects.all().order_by("-created_at")[:20]  # latest 20
    jobs_list = [
        {
            "title": job.title,
            "company_name": job.company_name,
            "location": job.location,
            "url": job.url,
            "similarity_score": job.similarity_score,
            "created_at": job.created_at
        }
        for job in jobs
    ]

    return JsonResponse({"saved_jobs": jobs_list})





@csrf_exempt
def match_jobs(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=400)

    try:
        data = json.loads(request.body)
        user_resume_text = data.get("resume_text", "").strip()
    except:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not user_resume_text:
        return JsonResponse({"error": "resume_text is required"}, status=400)

    # Fetch jobs from API
    jobs_api = "https://www.arbeitnow.com/api/job-board-api"
    response = requests.get(jobs_api)
    if response.status_code != 200:
        return JsonResponse({"error": "Failed to fetch jobs from API"}, status=500)

    jobs_data = response.json().get("data", [])

    scored_jobs = []

    for job in jobs_data:
        job_text = f"{job.get('title','')} {job.get('description','')}"
        vectorizer = TfidfVectorizer().fit([user_resume_text, job_text])
        vectors = vectorizer.transform([user_resume_text, job_text])
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

        scored_jobs.append({
            "title": job.get("title"),
            "company_name": job.get("company_name"),
            "location": job.get("location", ""),
            "url": job.get("url", ""),
            "similarity_score": round(float(similarity), 3)
        })

    # Sort by similarity
    scored_jobs.sort(key=lambda x: x["similarity_score"], reverse=True)

    # ✅ NOW create top_jobs
    top_jobs = scored_jobs[:10]

    # ✅ NOW save to database
    for job in top_jobs:
        MatchedJob.objects.create(
            resume_text=user_resume_text,
            title=job["title"],
            company_name=job["company_name"],
            location=job["location"],
            url=job["url"],
            similarity_score=job["similarity_score"]
        )

    return JsonResponse({
        "message": "Jobs matched successfully",
        "count": len(top_jobs),
        "matches": top_jobs
    })
