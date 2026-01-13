# resumes/serializers.py

from rest_framework import serializers

class AnalysisSerializer(serializers.Serializer):
    """
    Serializer for validating resume analysis input data.
    """
    cv = serializers.FileField(
        required=True,
        help_text="Upload your resume in PDF or DOCX format"
    )
    job_description = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=2000,
        help_text="Optional: Paste the job description for better relevance analysis"
    )

    def validate_cv(self, value):
        """
        Validate uploaded CV file type and size.
        """
        # Allowed file extensions
        allowed_extensions = ['.pdf', '.docx']
        file_extension = value.name.lower()[-5:]  # Get last 5 chars to catch .docx
        
        if not any(file_extension.endswith(ext) for ext in allowed_extensions):
            raise serializers.ValidationError(
                "Only PDF (.pdf) and Word (.docx) files are allowed."
            )
        
        # Size limit: 5MB
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError(
                "File size too large. Maximum allowed is 5MB."
            )
        
        return value