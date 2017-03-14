#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 00:16:56 2017

@author: Hilder

Modified on Fri Feb 10 17:06:00 2017

@author: rivero
"""

from mesa import Agent
from accounting import Bookkeeper


class Economy(Agent):
      net_worth = 0.0
      available_cash = 0.0
      
      def __init__(self, ag_name, econModel):
        
          super().__init__(ag_name, econModel)
          self.net_worth = 0.0
          self.available_cash = 0.0
      

      def getResult(self):
          #coletar os resultados
          self.result+=1
        
        
      def step(self):
          pass
        


class Market(Agent):
    
    offers = dict()
    net_worth = 0.0
    available_cash = 0.0
    total_sells_qt = 0.0
    total_sells_vl = 0.0
    
    def __init_(self, market_name, econModel):
        super().__init__(market_name, econModel)
        self.offers = dict()
        self.net_worth = 0.0
        self.available_cash = 0.0
        self.total_sells_qt = 0.0
        self.total_sells_vl = 0.0
        
        
    def add_offer(self, a_seller, a_bid):
            self.offers[a_seller] = a_bid
            
    def take_offers(self, a_buyer, a_quantity):
        for bidder in self.offers:
            bid = self.offers[bidder]
            if bid.quantity_of_gs < a_quantity:
                a_quantity -= bid.quantity_of_gs
                a_buyer.bookkeeper.buy_gs(bidder, bid, bid.unit_value_of_gs)
                self.total_sells_qt += bid.quantity_of_gs
                self.total_sells_vl += bid.quantity_of_gs*bid.unit_value_of_gs
                bid.quantity_of_gs = 0.0
            else:
                a_buyer.bookkeeper.buy_gs(bidder,bid , bid.unit_value_of_gs)
                bid.quantity_of_gs -= a_quantity
                self.total_sells_qt += a_quantity
                self.total_sells_vl += a_quantity*bid.unit_value_of_gs
                a_quantity = 0.0
        
 
    def clean_zero_bids(self):
        self.offers = {bidder:bid 
                       for bidder, bid in self.offers.items() 
                       if bid.quantity_of_gs > 0.0}
                
        
                
    def offers_value(self):
        total_offers = 0.0
        for bidder in self.offers:
            bid = self.offers[bidder]
            total_offers += bid.value_of_gs
        return total_offers

    def offers_quantity(self):
        total_offers = 0.0
        for bidder in self.offers:
            bid = self.offers[bidder]
            total_offers += bid.quantity_of_gs
        return total_offers
    

    def get_bid(self, a_bidder):
        if a_bidder in self.offers:
            return self.offers[a_bidder]
        else:
            return 0.0
        
    
    def step(self):
        pass
                
      


class EconomicAgent (Agent):

    """
    Created on Tue Feb  7 16:24:07 2017

    @author: rivero
    """ 

    contracts = None
    decision_Mechanism = None
    bookkeeper = None
    markets = None
    

  
    def __init__(self, ag_name, econModel, economy, initial_assets,
                 initial_liabilities, initial_cash):
        super().__init__(ag_name, econModel)
        self.economy = economy
        self.markets = dict()
        self.bookkeeper = Bookkeeper(self,initial_assets,initial_liabilities, 
                                     initial_cash)
        self.net_worth = 0.0
        self.available_cash = initial_cash
      
        
    def enter_market(self, a_market):
        self.markets[a_market.unique_id] = a_market
                    
    def buy_gs(self, a_seller, a_good_or_service, price):
        self.bookkeeper.buy_gs(a_seller, a_good_or_service,price)
        self.update_available_cash()


    def update_net_worth(self):
        self.net_worth = self.bookkeeper.net_worth()
    
    def update_available_cash(self):
        self.available_cash = self.bookkeeper.available_cash()
        
        
 
  
    def step(self):
        pass
    
    
    
    
 #definir classes Agent aqui

class Firm (EconomicAgent):
    
    production_function = None
    
    
    def __init__(self, ag_name, econModel, economy, initial_assets,
                 initial_liabilities, initial_cash):
        
         super().__init__(ag_name, econModel, economy, initial_assets,
                          initial_liabilities, initial_cash)
          

    def supply(self, an_agent, a_good_or_service, value):
        pass
        
    def investment(self, an_agent, a_service, value, interest_rate):
        pass
    
    def produce(self,a_good_or_service):
        pass
    
    def step(self):
        pass    




class Household (EconomicAgent):
    
    subsistence_requirements = None
    hh_members = None
    
    def __init__(self, ag_name, econModel, economy, initial_assets,
                 initial_liabilities, initial_cash):
        
         super().__init__(ag_name, econModel, economy, initial_assets,
                          initial_liabilities, initial_cash)

    def consume(self, an_agent, a_good_or_service, value):
        pass   

    def step(self):
        pass            
    
    
    
    
class Bank (EconomicAgent):
    
    def __init__(self, ag_name, econModel, economy, initial_assets,
                 initial_liabilities, initial_cash):
       
         super().__init__(ag_name, econModel, economy, initial_assets,
                          initial_liabilities, initial_cash)

    def interest(self, paying_receivin, an_agent):
        pass    

    def step(self):
        pass    
    
    
    
class Government (EconomicAgent):
    
    def __init__(self, ag_name, econModel, economy, initial_assets,
                 initial_liabilities, initial_cash):
        
         super().__init__(ag_name, econModel, economy, initial_assets,
                          initial_liabilities, initial_cash)

        
    def cash_transfer(self, a_household):
        pass

    def subsidy(self, a_firm):
        pass
    
    def taxes(self):
        pass
    
    def step(self):
        pass    
    
    

class CentralBank (EconomicAgent):
    def __init__(self, ag_name, econModel, economy, initial_assets,
                 initial_liabilities, initial_cash):
       
         super().__init__(ag_name, econModel, economy, initial_assets,
                          initial_liabilities, initial_cash)

    
    def interest(self, a_bank):
        pass    

    def step(self):
        pass    
    
    
    
