from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import PlaceOrderSerializer
from .services import cancel_order, place_order
from .models import Order

class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PlaceOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        try:
            order = place_order(
                user=request.user,
                instrument=data["instrument"],
                side=data["side"],
                order_type=data["order_type"],
                quantity=data["quantity"],
                price=data.get("price"),
            )
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "order_id": order.id,
                "status": order.status,
                "locked_balance": request.user.wallet.locked_balance,
            },
            status=status.HTTP_201_CREATED
        )


class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Order.objects.filter(user=request.user)

        status_filter = request.query_params.get("status")
        if status_filter:
            qs = qs.filter(status=status_filter)

        data = [
            {
                "id": o.id,
                "instrument_id" : o.instrument.id,
                "instrment_sym" : o.instrument.symbol,
                "instrument_name" : o.instrument.name,
                "side": o.side,
                "price": o.price,
                "quantity": o.quantity,
                "filled": o.filled_quantity,
                "status": o.status,
                "created_at": o.created_at,
            }
            for o in qs
        ]

        return Response(data)


class CancelOrder(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, order_id):
        try:
            order = cancel_order(
                user=request.user,
                order_id=order_id
            )
        except ValueError as e:
            return Response(
                {"error" : str(e)},
                status = status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            {
                "order_id" : order.id,
                "status" : order.status
            },
            status = status.HTTP_200_OK
        )