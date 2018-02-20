#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 00:16:56 2017

@author: Hilder

Modified on Fri Feb 10 17:06:00 2017

@author: rivero

"""

from random import random

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.time import RandomActivation

from accounting import GoodOrService
from basicEconomicAgents import Economy, Market
from dumbEconomicAgents import DumbFirm, DumbHousehold


#definir funções de calcular aqui
def compute_net_worth(model):
    agents_worth = [agent.net_worth for agent in model.schedule.agents]
    total_worth = sum(agents_worth)
    print(total_worth)
    return total_worth
   
def available_cash(model):
    agents_cash = [agent.available_cash for agent in model.schedule.agents]
    total_cash = sum(agents_cash)
    return total_cash
   
def goods_qt(model):
    gs_mkt_qt = model.goods_market.total_sells_qt
    return gs_mkt_qt

def goods_vl(model):
    gs_mkt_vl = model.goods_market.total_sells_vl
    return gs_mkt_vl
  
def labor_qt(model):
    l_mkt_qt = model.labor_market.total_sells_qt
    return l_mkt_qt

def labor_vl(model):
    l_mkt_vl = model.labor_market.total_sells_vl
    return l_mkt_vl    


def computeN1(model):
    N1 = model.num_firms
    return N1

def getResult(model):
    # Checar o tratamento do gid aqui
    f1 = len(model.grid.get_cell_list_contents((0, 2)))
    fm = len(model.grid.get_cell_list_contents((0, 3)))
    result = f1+fm
    return result
     
#definir classe Model aqui
class DumbEcoModel(Model):
    #inicialização
    verbose = True
    economy = None
    initial_assets = None
    initial_liabilities = None
    initial_cash = None 
    initial_inventory = None
    labor_market = None
    goods_market = None

    def __init__(self):
        
        self.num_firms = 3
    #    self.num_firms2 = n2
        self.num_households = 30
        self.running = True
        self.grid = MultiGrid(1, 5, True)
        self.result = 0
        #posso criar meu scheduler se for o caso
        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(
                model_reporters={"GoodsQt": goods_qt,
                                 "GoodsVl": goods_vl,
                                 "LaborQt": labor_qt,
                                 "LaborVl": labor_vl}
             )
         
        
#        )
  
#        self.datacollector = DataCollector(
#           model_reporters={"Labor": computeN1,"Goods": getResult}
            
#       )
        self.initial_assets = dict()
        self.initial_liabilities = dict()
        self.initial_cash = 100.0
        self.initial_inventory = dict()
        
        
        self.economy = Economy("DumbEconomy", self)
        self.schedule.add(self.economy)
        self.grid.place_agent(self.economy, (0, 0)) 
        
        self.labor_market = Market("LaborMarket", self)
        self.schedule.add(self.labor_market)
        self.grid.place_agent(self.labor_market, (0, 1)) 

        self.goods_market = Market("GoodsMarket", self)
        self.schedule.add(self.goods_market)
        self.grid.place_agent(self.goods_market, (0, 2)) 
        
        
        #### Define goods and services of the economy

        self.initial_assets = dict()
        self.initial_liabilities = dict()
 
        self.initial_inventory = dict()
   
        # initialize households    
        for i in range(self.num_households):
            self.initial_cash = 10.0 
            # Intialize Household assets
            quantity_of_labor = 1000.0
            price_of_labor = .5
            value_of_labor = quantity_of_labor*price_of_labor                       
            quantity_of_food = 0.0
            price_of_food = .1
            value_of_food = quantity_of_food*price_of_food  
            available_labor = GoodOrService("labor",1,quantity_of_labor,
                                            price_of_labor,value_of_labor)
            food = GoodOrService("corn",1,quantity_of_food,price_of_food,
                                 value_of_food)
            self.initial_assets = {available_labor.name_of_gs:available_labor, 
                                   food.name_of_gs:food} 
 
            # Intialize Household liabilities                    
            quantity_of_food_demmand = random()*130.0
            price_of_food_demmand = 0.1
            value_of_food_demmand = quantity_of_food_demmand*price_of_food_demmand                      
            food_demmand = GoodOrService("food_demmand",1,
                                         quantity_of_food_demmand,
                                         price_of_food_demmand,
                                         value_of_food_demmand)
            self.initial_liabilities = {food_demmand.name_of_gs:food_demmand} 

            # Initialize Household inventory
            self.initial_inventory_hh = {food.name_of_gs:food,
                                         available_labor.name_of_gs:available_labor} 
        
            fm = DumbHousehold(i, self, self.economy, self.initial_assets,
                               self.initial_liabilities, self.initial_cash, 
                               self.initial_inventory_hh)
            self.schedule.add(fm)
            self.grid.place_agent(fm, (0, 3))
            fm.enter_labor_market(self.labor_market)
            fm.enter_goods_market(self.goods_market)
            
          

        # initialize firms        
        for i in range(self.num_firms):
            # initialize firm assets    
            self.initial_cash = 1000.0 
            quantity_of_food = 10.0
            price_of_food = .1
            value_of_food = quantity_of_food*price_of_food  
            produced_food = GoodOrService("corn",1,quantity_of_food,price_of_food,value_of_food)
            self.initial_assets = {produced_food.name_of_gs:produced_food} 
            # initialize firm liabilities
            quantity_of_labor = 0.0
            price_of_labor = 0.5
            value_of_labor = quantity_of_labor*price_of_labor
            demmanded_labor = GoodOrService("labor",1,quantity_of_labor,price_of_labor,value_of_labor)
            self.initial_liabilities = {demmanded_labor.name_of_gs:demmanded_labor}
            # initialize firm inventory
            self.initial_inventory_firm = {produced_food.name_of_gs:produced_food} 
            
            f1 = DumbFirm(i, self, self.economy, self.initial_assets,
                          self.initial_liabilities, self.initial_cash, 
                          self.initial_inventory_firm)
            self.schedule.add(f1)
            self.grid.place_agent(f1, (0, 4))
            f1.enter_labor_market(self.labor_market)
            f1.enter_goods_market(self.goods_market)
    
            
   
    def step(self):
        print([self.schedule.time," my_step"])
        self.schedule.step()
        # restart market variables
        self.datacollector.collect(self)
        print(["Labor Market:",self.labor_market.unique_id, 
               "Quantity: ", self.labor_market.total_sells_qt, 
               "  Value: ", self.labor_market.total_sells_vl])
        print(["Goods Market:",self.goods_market.unique_id, 
               "Quantity: ", self.goods_market.total_sells_qt, 
               "  Value: ", self.goods_market.total_sells_vl])        

        self.goods_market.total_sells_qt = 0.0
        self.labor_market.total_sells_qt = 0.0
        self.goods_market.total_sells_vl = 0.0
        self.labor_market.total_sells_vl = 0.0


        print([self.schedule.time,"passei"])
   
    
    def run_model(self, n):
        for i in range(n):      
            self.step()
     
            
