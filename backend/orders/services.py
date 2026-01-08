from django.db import transaction
from decimal import Decimal

from .models import Order
from ledger.models import Wallet

def place_order(*, user, instrument, side, order_type, quantity, price=None):
    with transaction.atomic():
        
        wallet = Wallet.objects.select_for_update().get(user=user)
        
        if side == 'BUY':
            if order_type == 'LIMIT':
                required_amount = Decimal(price) * quantity
            else:
                raise ValueError("MARKET ORDERS NEEDS TO BE DONE YET")
            
            available = wallet.balance - wallet.locked_balance
            if available < required_amount:
                raise ValueError("Insufficient Balance")
            
            wallet.locked_balance += required_amount
            wallet.save(update_fields=['locked_balance'])
            
        order = Order.objects.create(
            user=user,
            instrument=instrument,
            side=side,
            order_type=order_type,
            price=price,
            quantity=quantity,
        )
        
    return order


def cancel_order(*, user, order_id):
    with transaction.atomic():
        try:
            order = Order.objects.select_for_update().get(
                id=order_id,
                user=user
            )
        except Order.DoesNotExist:
            raise ValueError("Order not found")
        
        if order.status not in ("OPEN", "PARTIAL"):
            raise ValueError("Order can not be placed")
        
        wallet = Wallet.objects.select_for_update().get(user=user)
        
        if order.side == 'BUY':
            remaining_qty = order.quantity - order.filled_quantity
            unlock_amount = Decimal(order.price) * remaining_qty
            
            wallet.locked_balance -= unlock_amount
            if wallet.locked_balance < 0:
                raise("Locked balance in wallet is corrupted please check")
            
            wallet.save(update_fields=["locked_balance"])
        
        order.status = 'CANCELLED'
        order.save(update_fields=['status'])
        
        
    return order