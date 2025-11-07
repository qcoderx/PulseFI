from django.db import models
from django.conf import settings

class BusinessProfile(models.Model):
    """
    Stores the "Stated Truth"
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    business_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    founded_date = models.DateField(null=True, blank=True)
    # Other fields from the "Stated Truth" form

    def __str__(self):
        return self.business_name

class CACDocument(models.Model):
    """
    Stores the "Document Truth"
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cac_document')
    cac_file = models.FileField(upload_to='cac_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    extracted_name = models.CharField(max_length=255, blank=True, null=True) # To be filled by AI

    def __str__(self):
        return f"CAC for {self.user.email}"

class BusinessVideo(models.Model):
    """
    Stores the "Visual Truth"
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='business_video')
    video_file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    video_summary = models.TextField(blank=True, null=True) # To be filled by AI

    def __str__(self):
        return f"Video for {self.user.email}"

class Score(models.Model):
    """
    Stores the Pulse and Profit Scores
    """
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        VERIFIED = 'verified', 'Verified'
        FAILED = 'failed', 'Failed'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='score')
    pulse_score = models.IntegerField(default=0)
    profit_score = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    pulse_fail_reason = models.TextField(blank=True, null=True) # To explain failure
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Scores for {self.user.email}: Pulse({self.pulse_score}), Profit({self.profit_score})"