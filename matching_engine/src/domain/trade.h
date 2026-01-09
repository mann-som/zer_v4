#pragma once

#include <string>
#include <cstdint>

struct Trade{
    std::string buy_order_id;
    std::string sell_order_id;
    std::string intrument_id;

    double price;
    int64_t quantity;
    int64_t timestamp;
};