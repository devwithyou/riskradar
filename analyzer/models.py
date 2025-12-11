from django.db import models
from django.contrib.auth.models import User


class ScanResult(models.Model):
    url = models.URLField(max_length=500)
    final_url = models.URLField(max_length=500)
    status_code = models.IntegerField()
    score = models.IntegerField(default=100)
    raw_headers = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.url} - Score: {self.score}"


class Issue(models.Model):
    SEVERITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    scan_result = models.ForeignKey(ScanResult, on_delete=models.CASCADE, related_name='issues')
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    category = models.CharField(max_length=100)
    message = models.TextField()
    recommendation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['severity', '-created_at']

    def __str__(self):
        return f"{self.severity.upper()}: {self.category}"


