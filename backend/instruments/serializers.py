from symtable import Symbol
from tkinter.tix import Tree
from attr import fields
from rest_framework import serializers
from .models import Instrument
from . import utils

class CreateInstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = (
            "symbol",
            "name",
            "exchange",
            "isin",
            "instrument_type",
            "tick_size",
            "lot_size",
        )
    
    def create(self, validated_data):
        validated_data['instrument_code'] = utils.generate_inst_code()
        return super().create(validated_data)
        
class InstrumentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = [
            "symbol",
            "name",
            "exchange",
            "instrument_type",
            "tick_size",
            "lot_size",
            "is_tradable",
        ]
        
class UpdateInstrumentSerializer(serializers.ModelSerializer):
    instrument_code = serializers.CharField()
    
    class Meta:
        model = Instrument
        fields = (
            "instrument_code",
            "tick_size",
            "lot_size",
            "is_tradable",
            "name",
        )
    
    def validate(self, data):
        try:
            self.instrument = Instrument.objects.get(
                instrument_code=data["instrument_code"],
                is_listed=True
            )
        except Instrument.DoesNotExist:
            raise serializers.ValidationError("Instrument doesn't exists or is delisted")
        
        return data
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
    def save(self):
        validated_data = self.validated_data.copy()
        validated_data.pop("instrument_code")
        return self.update(self.instrument, validated_data)
    
class UnlistInstrumentSerializer(serializers.Serializer):
    symbol = serializers.CharField()
    exchange = serializers.CharField()
    
    def validate(self, data):
        try:
            self.instrument = Instrument.objects.get(
                symbol=data['symbol'],
                exchange=data['exchange'],
                is_listed=True
            )
        except Instrument.DoesNotExist:
            raise serializers.ValidationError("Instrument not found or already unlisted")
        
        return data
    
    def save(self):
        self.instrument.is_listed = False
        self.instrument.is_tradable = False
        self.instrument.save(update_fields=["is_listed", "is_tradable"])
        return self.instrument