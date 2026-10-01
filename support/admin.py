from django.contrib import admin
from .models import KnowledgeArticle

@admin.register(KnowledgeArticle)
class KnowledgeArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'keywords', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'problem', 'solution', 'keywords', 'category')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('General Information', {
            'fields': ('title', 'category', 'keywords')
        }),
        ('Problem Description & Solution', {
            'fields': ('problem', 'solution')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
