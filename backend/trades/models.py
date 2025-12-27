from django.db import models
import uuid
from django.conf import settings


class Trade(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    SIDE = [("BUY", "BUY"), ("SELL", "SELL")]
    
    side = models.CharField(max_length=10, choices=SIDE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Trade {self.id}"