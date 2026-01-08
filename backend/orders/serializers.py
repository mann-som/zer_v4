# from itsdangerous import Serializer
from rest_framework import serializers

from .models import Order
from instruments.models import Instrument

class PlaceOrderSerializer(serializers.Serializer):
    instrument_id = serializers.IntegerField()
    side = serializers.ChoiceField(choices=["BUY", "SELL"])
    order_type = serializers.ChoiceField(choices=["LIMIT", "MARKET"])
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False
    )
    quantity = serializers.IntegerField(min_value=1)
    
    def validate(self, data):
        if data['order_type'] == 'LIMIT' and 'price' not in data:
            raise serializers.ValidationError("Price required for LIMIT order")
        
        if data['order_type'] == 'MARKET' and 'price' in data:
            raise serializers.ValidationError("Price not allowed for MARKET order")
        
        try:
            instrument = Instrument.objects.get(id=data["instrument_id"])
        except Instrument.DoesNotExist:
            raise serializers.ValidationError("Invalid instrument")

        data["instrument"] = instrument
        return data