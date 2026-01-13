
from django.contrib import admin
from django.contrib import messages
from .models import MatchedJob

@admin.action(description="Apply Job")
def apply_job(modeladmin, request, queryset):
    applied_count = 0

    for job in queryset:
        if not job.is_applied:
            job.is_applied = True
            job.save()
            applied_count += 1

    messages.success(
        request,
        f"{applied_count} job(s) applied successfully ✅"
    )


@admin.register(MatchedJob)
class MatchedJobAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "company_name",
        "similarity_score",
        "is_applied",
        "created_at"
    )

    list_filter = ("is_applied", "created_at")
    search_fields = ("title", "company_name")
    actions = [apply_job]   # ✅ ACTION ADDED
