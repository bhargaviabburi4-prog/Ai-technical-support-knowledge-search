from django.db import models

class KnowledgeArticle(models.Model):
    CATEGORY_CHOICES = [
        ('Network & Wi-Fi', 'Network & Wi-Fi'),
        ('Operating System', 'Operating System'),
        ('Software & Hardware', 'Software & Hardware'),
        ('Account & Security', 'Account & Security'),
        ('Programming & Development', 'Programming & Development'),
        ('General IT Support', 'General IT Support'),
    ]

    title = models.CharField(max_length=255, help_text="Title of the technical article or issue")
    category = models.CharField(
        max_length=100, 
        choices=CATEGORY_CHOICES, 
        default='General IT Support',
        db_index=True,
        help_text="Category of the technical problem"
    )
    problem = models.TextField(help_text="Detailed description of the problem or error symptoms")
    solution = models.TextField(help_text="Step-by-step troubleshooting or solution instructions")
    keywords = models.CharField(
        max_length=255, 
        help_text="Comma-separated keywords for search matching (e.g. wifi, internet, connection)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Knowledge Article"
        verbose_name_plural = "Knowledge Articles"

    def __str__(self):
        return f"[{self.category}] {self.title}"
