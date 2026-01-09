#pragma once

enum class Side{
    BUY,
    SELL
};

enum class OrderType{
    LIMIT,
    MARKET
};

enum class OrderStatus{
    OPEN,
    PARTIAL,
    FILLED,
    CANCELLED
};