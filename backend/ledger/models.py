import uuid
from django.db import models
from django.conf import settings

class LedgerEntry(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    txn_code = models.CharField(max_length=20, unique=True, db_index=True, blank=True)
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    balance_after = models.DecimalField(max_digits=18, decimal_places=2)
    TRANSACTION_TYPE = [("CREDIT", "CREDIT"), ("DEBIT", "DEBIT")]
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPE)
    
    PURPOSE = [
        ("DEPOSIT", "DEPOSIT"),
        ("WITHDRAWAL", "WITHDRAWAL"),
        ("TRADE", "TRADE"),
        ("REFUND", "REFUND"),
        ("CHARGE", "CHARGE"),
        ("ADJUSTMENT", "ADJUSTMENT"),
    ]
    purpose = models.CharField(max_length=20, choices=PURPOSE)
    
    trade = models.ForeignKey(
        "trades.Trade",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    
    external_reference = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-id"]
    
class Wallet(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    
    balance = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    locked_balance = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    
    updated_at = models.DateTimeField(auto_now=True)