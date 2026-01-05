from decimal import Decimal
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import apply_ledger_entry

from . import serializers
from .models import LedgerEntry, Wallet

# @api_view(['GET'])
class WalletView(APIView):
    permission_classes = [IsAuthenticated]
     
    def get(self, request):
        wallet = Wallet.objects.get(user=request.user)
        serializer = serializers.WalletDetailSerializer(wallet)
        
        return Response(serializer.data)
    
class LedgerListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = LedgerEntry.objects.filter(user=request.user)

        purpose = request.query_params.get("purpose")
        txn_type = request.query_params.get("transaction_type")

        if purpose:
            qs = qs.filter(purpose=purpose)
        if txn_type:
            qs = qs.filter(transaction_type=txn_type)

        serializer = serializers.LedgerEntrySerializer(qs, many=True)
        return Response(serializer.data)

class DepositView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        amount = request.data.get("amount")
        
        apply_ledger_entry(
            user=request.user,
            amount=Decimal(amount),
            purpose="DEPOSIT",
            transaction_type="CREDIT",
            description="Manual deposit"
        )
        
        return Response({"status": "ok"})