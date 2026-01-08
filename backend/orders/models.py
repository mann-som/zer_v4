import uuid
from django.db import models
from django.conf import settings

class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    instrument = models.ForeignKey(
        "instruments.Instrument",
        on_delete=models.CASCADE
    )

    SIDE = [("BUY", "BUY"), ("SELL", "SELL")]
    side = models.CharField(max_length=4, choices=SIDE)

    ORDER_TYPE = [("LIMIT", "LIMIT"), ("MARKET", "MARKET")]
    order_type = models.CharField(max_length=6, choices=ORDER_TYPE)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    quantity = models.PositiveIntegerField()
    filled_quantity = models.PositiveIntegerField(default=0)

    STATUS = [
        ("OPEN", "OPEN"),
        ("PARTIAL", "PARTIAL"),
        ("FILLED", "FILLED"),
        ("CANCELLED", "CANCELLED"),
    ]
    status = models.CharField(max_length=10, default="OPEN")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["instrument", "side", "price"]),
            models.Index(fields=["user", "status"]),
        ]

    def remaining_quantity(self):
        return self.quantity - self.filled_quantity

    def __str__(self):
        return f"{self.side} {self.quantity} @ {self.price}"
