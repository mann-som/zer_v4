from django.db import transaction
from decimal import Decimal
from .models import LedgerEntry, Wallet
import uuid

def apply_ledger_entry(*, user, amount, purpose, transaction_type, reference=None, description=""):
    if amount <= 0:
        raise ValueError("Amount must be positive")
    
    with transaction.atomic():
        wallet = Wallet.objects.select_for_update().get(user=user)
        
        if transaction_type == 'DEBIT':
            new_balance = wallet.balance - Decimal(amount)
            signed_amount = -amount
        else:
            new_balance = wallet.balance + Decimal(amount)
            signed_amount = amount
            
        wallet.balance = new_balance
        wallet.save(update_fields=["balance"])
        
        entry = LedgerEntry.objects.create(
            user=user,
            amount=signed_amount,
            balance_after=new_balance,
            transaction_type=transaction_type,
            purpose=purpose,
            trade=reference,
            description=description,
        ) 
    
    return entry