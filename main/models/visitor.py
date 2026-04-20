from django.db import models
from django.conf import settings


class Visitor(models.Model):
    session_key = models.CharField(max_length=120, blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    product = models.ForeignKey(
        "main.Product",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="visitor_logs"
    )
    is_guest = models.BooleanField(default=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    visited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-visited_at"]

    def __str__(self):
        return f"{self.product} - {'Guest' if self.is_guest else 'User'}"