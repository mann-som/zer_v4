#pragma once

#include <map>
#include <deque>
#include <unordered_map>
#include <memory>
#include <vector>
#include "../domain/order.h"
#include "../domain/trade.h"

class OrderBook {
public:
    explicit OrderBook(std::string instrument_id);

    std::vector<Trade> add_order(std::shared_ptr<Order> order);

    bool cancel_order(const std::string& order_id);

private:
    std::string instrument_id;

    std::map<double, std::deque<std::shared_ptr<Order>>, std::greater<double>> bids;

    std::map<double, std::deque<std::shared_ptr<Order>>> asks;

    std::unordered_map<std::string, std::shared_ptr<Order>> order_lookup;

    std::vector<Trade> match_buy(std::shared_ptr<Order> buy);
    std::vector<Trade> match_sell(std::shared_ptr<Order> sell);
};
