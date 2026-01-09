#pragma once

#include <string>
#include <cstdint>
#include "enums.h"

struct Order {
    std::string order_id;        
    std::string instrument_id;   
    Side side;
    OrderType type;

    double price;               
    int64_t quantity;
    int64_t filled_quantity;

    int64_t timestamp;          

    Order(
        std::string oid,
        std::string iid,
        Side s,
        OrderType t,
        double p,
        int64_t q,
        int64_t ts
    ) : order_id(std::move(oid)),
        instrument_id(std::move(iid)),
        side(s),
        type(t),
        price(p),
        quantity(q),
        filled_quantity(0),
        timestamp(ts) {}

    int64_t remaining() const {
        return quantity - filled_quantity;
    }
};
