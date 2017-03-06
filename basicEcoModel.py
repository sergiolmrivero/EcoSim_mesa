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
from basicEcoSchedule import RandomActivationByBreed
from basicEconomicAgents import Economy, Firm1Agent, Firm2Agent, FamilyAgent

#definir funções de calcular aqui

def computeN1(model):
    N1 = model.num_firms1
    return N1

def getResult(model):
    f1 = len(model.grid.get_cell_list_contents((0, 1)))
    f2 = len(model.grid.get_cell_list_contents((0, 2)))
    fm = len(model.grid.get_cell_list_contents((0, 3)))
    result = f1+f2+fm
    return result
     
#definir classe Model aqui
class MyModel(Model):
    #inicialização
    verbose = False
    economy = None
    initial_assets = None
    initial_liabilities = None
    initial_cash = None 
    initial_inventory = None

    def __init__(self, n1, n2, f):
        
        self.num_firms1 = n1
        self.num_firms2 = n2
        self.num_families = f
        self.running = True
        self.grid = MultiGrid(1, 4, True)
        self.result = 0
        #posso criar meu scheduler se for o caso
        self.schedule = RandomActivationByBreed(self)
        self.datacollector = DataCollector(
            model_reporters={"econ1": computeN1,"econ2": getResult}
            
        )
        self.initial_assets = dict()
        self.initial_liabilities = dict()
        self.initial_cash = 1000.0
        self.initial_inventory = dict()
        
        
        self.economy = Economy(0, self, self.economy, self.initial_assets,self.initial_liabilities, self.initial_cash, self.initial_inventory)
        self.schedule.add(self.economy)
        self.grid.place_agent(self.economy, (0, 0)) 

        
        for i in range(self.num_firms1):
            f1 = Firm1Agent(i, self, self.economy, self.initial_assets,self.initial_liabilities, self.initial_cash, self.initial_inventory)
            self.schedule.add(f1)
            self.grid.place_agent(f1, (0, 1))
        for i in range(self.num_firms1):
            f2 = Firm2Agent(i, self, self.economy, self.initial_assets,self.initial_liabilities, self.initial_cash, self.initial_inventory)
            self.schedule.add(f2)
            self.grid.place_agent(f2, (0, 2))
        for i in range(self.num_firms1):
            fm = FamilyAgent(i, self, self.economy, self.initial_assets,self.initial_liabilities, self.initial_cash, self.initial_inventory)
            self.schedule.add(fm)
            self.grid.place_agent(fm, (0, 3))
        

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        print([self.schedule.time,
                   self.schedule.get_breed_count(Economy),
                   self.schedule.get_breed_count(FamilyAgent)])
    
    def run_model(self, n):
        for i in range(n):
            
            self.step()
            
