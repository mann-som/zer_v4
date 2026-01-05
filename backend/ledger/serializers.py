from rest_framework import serializers
from .models import LedgerEntry, Wallet

class WalletDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Wallet
        fields = (
            "user",
            "balance",
            "locked_balance",
            "updated_at"
        )
        
class LedgerEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LedgerEntry
        fields = "__all__"