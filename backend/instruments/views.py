from tkinter.tix import Tree
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from . import serializers
from .models import Instrument

@api_view(['POST'])
def create_instrument(request):
    serializer = serializers.CreateInstrumentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    instrument = serializer.save()
    return Response(
        {
            "instrument_code" : instrument.instrument_code,
            "message" : "Instrument created"
        },
        status=status.HTTP_201_CREATED
    )

@api_view(['GET'])
def list_instruments(request):
    allowed_filters = {"symbol", "exchange"}
    recieved_params = set(request.query_params.keys())
    invalid_params = recieved_params - allowed_filters
    
    if invalid_params:
        return Response(
                {
                    "error": f"Invalid query parameters: {', '.join(invalid_params)}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
    qs = Instrument.objects.filter(is_listed=True)
    
    symbol = request.query_params.get("symbol")
    exchange = request.query_params.get("exchange")
    
    if symbol:
        qs = qs.filter(symbol=symbol)
    
    if exchange:
        qs = qs.filter(exchange=exchange)
    
    serializer = serializers.InstrumentListSerializer(qs, many=True)
    return Response(serializer.data)

@api_view(["PATCH"])
def update_instrument(request):
    serializer = serializers.UpdateInstrumentSerializer(data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    instrument = serializer.save()
    
    return Response(
        {
            "message" : f"{instrument.instrument_code} Updated"
        },
        status=status.HTTP_200_OK
    )
    
@api_view(['DELETE'])
def delete_instrument(request):
    instrument_code = request.data.get("instrument_code")
    
    try:
        instrument = Instrument.objects.get(
            instrument_code=instrument_code,
            is_listed=True
        )
    except Instrument.DoesNotExist:
        return Response(
            {"error" : "instrument doesn't exists or already unlisted"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    instrument.is_listed = False
    instrument.is_tradable = False
    instrument.save()
    
    return Response(
        {"message" : f"{instrument_code} delisted successfully"},
        status=status.HTTP_200_OK
    )