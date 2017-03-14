#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 00:16:56 2017

@author: Hilder

Modified on Fri Feb 10 17:06:00 2017
@author: rivero
"""

from basicEconomicAgents import Household, Firm
from accounting import GoodOrService
from random import random

    
    
 #definir classes Agent aqui


        
class DumbFirm(Firm):
    """Firm - Goods Producer"""
    goods_market = None
    labor_market = None
    demmanded_labor = None
    estimated_demmand = random()*100.0
    technical_coefficient = .8
    profit_margin = .5
    
    def __init__(self, ag_name, econModel, economy, initial_assets,
                 initial_liabilities, initial_cash):
        
      super().__init__(ag_name, econModel, economy, initial_assets,
           initial_liabilities, initial_cash)

    #colocar as funções que serão ativadas no step
    def estimate_demand(self):
         #my_bid = self.goods_market.get_bid(self)
         #if my_bid != 0.0:
         #   stock = self.estimated_demmand - my_bid.quantity_of_gs 
         #   if stock > 0:
         #       self.estimated_demmand= random()*(self.estimated_demmand - stock)
         #   else:
         #      self.estimated_demmand *= 1.02
         self.estimated_demmand = random()*100.0

    
        
        
    
    def contract_labor(self):
        self.demmanded_labor = self.estimated_demmand/self.technical_coefficient
        #print(["Demmanded_labor:",self.demmanded_labor])
        self.labor_market.take_offers(self,self.demmanded_labor)
        

    def produce(self):
        #labor_available = 10
        production_price = 0.1
        production_value = 0.1
        offer = None
        
        self.labor_available = self.bookkeeper.get_liability("labor")
        #print(["Labor Available:",self.labor_available.quantity_of_gs])
        production = self.labor_available.quantity_of_gs * self.technical_coefficient
        production_price = self.labor_available.unit_value_of_gs * (1+self.profit_margin)
        production_value = production*production_price   
                  
        offer = GoodOrService("corn",1,production,
                               production_price,
                               production_value)
        self.goods_market.add_offer(self, offer)
           
    def get_profits(self):
        pass
        
    def enter_goods_market(self, a_market):   
        self.goods_market = a_market

    def enter_labor_market(self, a_market):        
        self.labor_market = a_market
        
      
    def step(self):
        self.update_available_cash()
        self.estimate_demand()
        self.contract_labor()
        self.produce()
        self.get_profits()
        self.update_available_cash()
        self.update_net_worth()
#        self.labor_market.clean_zero_bids()
  

        
    
    

class DumbHousehold(Household):
    """Household - Offers Labor, consumes final goods"""
    labor_market = None
    goods_market = None
    labor_capacity= 1000.0
    
    def __init__(self, ag_name, econModel, economy, initial_assets,
                 initial_liabilities, initial_cash):
        
        
        super().__init__(ag_name, econModel, economy, initial_assets,
             initial_liabilities, initial_cash)

    #colocar as funções que serão ativadas no step
    def estimate_available_labor(self):
        self.bookkeeper.get_asset("labor").quantity_of_gs = self.labor_capacity
        
    
    def offer_labor(self):   
        food_demmand = None
        food_stock = None
        food_necessities = None
        food_necessities_value = None
        labor_available = None
        labor_necessity = None
     
        # Estimate labor demmand
        
        food_demmand = self.bookkeeper.get_liability("food_demmand")
        food_stock = self.bookkeeper.get_asset("corn")
        food_necessities = food_demmand.quantity_of_gs - food_stock.quantity_of_gs + 100.0
        food_necessities_value = food_necessities*food_stock.unit_value_of_gs
       
        labor_available = self.bookkeeper.get_asset("labor")
        labor_necessity = food_necessities_value/labor_available.unit_value_of_gs
    
    
        # offer labor
        labor_value = labor_available.unit_value_of_gs*labor_necessity                                       
        my_bid = GoodOrService("labor",1,labor_necessity,
                               labor_available.unit_value_of_gs,
                               labor_value)
        self.labor_market.add_offer(self,my_bid)
        
    
    
    def buy_goods(self):
        food_demmand = None
        #food_stock = None
        food_necessities = None
   
     
        # Estimate food demmand
        
        food_demmand = self.bookkeeper.get_liability("food_demmand")
        #food_stock = self.bookkeeper.get_asset("corn")
        #food_necessities = food_demmand.quantity_of_gs - food_stock.quantity_of_gs
        #food_necessities = food_demmand.quantity_of_gs
        food_necessities = random()*food_demmand.quantity_of_gs
        self.goods_market.take_offers(self, food_necessities)
        #self.goods_market.clean_zero_bids()
        
        
    def consume_goods(self):
        #food_demmand = self.bookkeeper.get_liability("food_demmand")
        food_stock = self.bookkeeper.get_asset("corn")
        #new_food_stock_qt = food_demmand.quantity_of_gs - food_stock.quantity_of_gs
        #food_stock._quantity_of_gs = new_food_stock_qt
        food_stock.quantity_of_gs = 0.0
        
        
    def initialize_capacities(self):
         labor_available = self.bookkeeper.get_asset("labor")
         labor_available.quantity_of_gs = self.labor_capacity
         
    
    def enter_goods_market(self, a_market):
        self.goods_market = a_market

    def enter_labor_market(self, a_market):
        self.labor_market = a_market
  
        
    def step(self):
        self.estimate_available_labor()
        self.offer_labor()
        self.buy_goods()
        self.update_available_cash()
        self.consume_goods()
        self.update_net_worth()
        self.initialize_capacities()
        
        
    