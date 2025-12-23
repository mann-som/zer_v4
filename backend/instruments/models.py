from django.db import models

class Instrument(models.Model):
    EXCHANGE_CHOICES = (
        ('NSE', 'NSE'),
        ('BSE', 'BSE')
    )
    
    INSTRUMENT_TYPE_CHOICES = (
        ("EQ", "Equity"),
    )
    
    instrument_code = models.CharField(max_length=15, null=False, db_index=True, unique=True)
    symbol = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    exchange = models.CharField(max_length=10, choices=EXCHANGE_CHOICES)
    isin = models.CharField(max_length=20, unique=True)

    instrument_type = models.CharField(
        max_length=10,
        choices=INSTRUMENT_TYPE_CHOICES,
        default="EQ"
    )

    tick_size = models.DecimalField(max_digits=10, decimal_places=2)
    lot_size = models.IntegerField(default=1)

    is_tradable = models.BooleanField(default=True)
    is_listed = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ("symbol" , "exchange")
        indexes = [
            models.Index(fields=["symbol", "exchange"]),
        ]
        
    def __str__(self):
        return f"{self.symbol} ({self.exchange})"