#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 00:16:56 2017

@author: Hilder

Modified on Fri Feb 10 17:06:00 2017

@author: rivero

"""

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
from basicEconomicAgents import Economy, Market
from dumbEconomicAgents import DumbFirm, DumbHousehold
from random import random
from accounting import GoodOrService


#definir funções de calcular aqui
def compute_net_worth(model):
    agents_worth = [agent.net_worth for agent in model.schedule.agents]
    total_worth = sum(agents_worth)
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
    labor_market = None
    goods_market = None

    def __init__(self, n1, f):
        
        self.num_firms = n1
        self.num_households = f
        self.running = True
        self.grid = MultiGrid(1, 5, True)
        self.result = 0
        #posso criar meu scheduler se for o caso
        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(
                model_reporters={"GoodsVl": goods_vl,
                                 "LaborVl": labor_vl,
                                 "Net_Worth": compute_net_worth,
                                 "Total_Cash":available_cash}
             )
         
        

        self.initial_assets = dict()
        self.initial_liabilities = dict()
        self.initial_cash = 100.0
        
        
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
            quantity_of_food_demmand = random()*150.0
            price_of_food_demmand = 0.1
            value_of_food_demmand = quantity_of_food_demmand*price_of_food_demmand                      
            food_demmand = GoodOrService("food_demmand",1,
                                         quantity_of_food_demmand,
                                         price_of_food_demmand,
                                         value_of_food_demmand)
            self.initial_liabilities = {food_demmand.name_of_gs:food_demmand} 

      
            fm = DumbHousehold("HH"+str(i), self, self.economy, self.initial_assets,
                               self.initial_liabilities, self.initial_cash)
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
            
            f1 = DumbFirm("F"+ str(i), self, self.economy, self.initial_assets,
                          self.initial_liabilities, self.initial_cash)
            self.schedule.add(f1)
            self.grid.place_agent(f1, (0, 4))
            f1.enter_labor_market(self.labor_market)
            f1.enter_goods_market(self.goods_market)
    
            
   
    def step(self):
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
        



   
    
    def run_model(self, n):
        for i in range(n):      
            self.step()
     
            
