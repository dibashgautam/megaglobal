from django.db import models
from django.utils import timezone
import re


class Lead(models.Model):
    lead_id = models.CharField(max_length=120, unique=True, blank=True)
    phone = models.CharField(max_length=20, db_index=True)
    machine_requirement = models.CharField(max_length=255)
    raw_material_requirement = models.CharField(max_length=255)
    is_popup_submitted = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.lead_id:
            clean_phone = re.sub(r"\D", "", self.phone)  # number मात्र राख्ने
            timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
            self.lead_id = f"MSG-{clean_phone}-{timestamp}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.lead_id} - {self.phone}"