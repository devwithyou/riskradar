from django.contrib import admin
from .models import ScanResult, Issue


@admin.register(ScanResult)
class ScanResultAdmin(admin.ModelAdmin):
    list_display = ['url', 'score', 'created_at', 'owner']
    list_filter = ['created_at', 'owner']
    search_fields = ['url']
    readonly_fields = ['created_at']


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['scan_result', 'severity', 'category', 'created_at']
    list_filter = ['severity', 'category', 'created_at']
    search_fields = ['message', 'scan_result__url']


