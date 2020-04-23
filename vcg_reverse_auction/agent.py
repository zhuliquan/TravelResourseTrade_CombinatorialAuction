#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author : zlq16
# date   : 2018/10/25
from auction_base.agent import BasePlatform,BaseBidder

class Platform(BasePlatform):

    def __init__(self,quantity, predict_price_mui, predict_price_sigma):
        super(Platform, self).__init__(0,quantity)
        self.predict_price_mui = predict_price_mui
        self.predict_price_sigma = predict_price_sigma

class Bidder(BaseBidder):

    def __init__(self, id, D, unit_server_cost, capacity, v_f):
        super(Bidder, self).__init__(id, D, unit_server_cost, capacity, v_f)

class VirtualBidder(BaseBidder):

    def __init__(self, reverse_price, capacity):
        super(VirtualBidder, self).__init__(0, 1, reverse_price, capacity, lambda x:0)

    # def __str__(self):
    #     return "虚拟投标者,保留价格为{0},运载量:".format(self.unit_server_cost,self.capacity)
