# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 00:42:52 2017

@author: Hilder
"""
from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from dumbEcoModel import DumbEcoModel

chart1 = ChartModule([
                     {"Label":"GoodsQt","Color":"Black"}],
                     data_collector_name='datacollector',
                     )
chart2 = ChartModule([
                     {"Label":"GoodsVl","Color":"Red"}],
                     data_collector_name='datacollector',
                     )
chart3 = ChartModule([
                     {"Label":"LaborQt","Color":"Green"}],
                     data_collector_name='datacollector',
                     )
chart4 = ChartModule([
                     {"Label":"LaborVl","Color":"Blue"}],
                     data_collector_name='datacollector',
                     )
firms = 3
households = 30
server = ModularServer(DumbEcoModel, [chart1, chart2, chart3, chart4], "Dumb Economic Model", firms, households)
server.port = 8891
server.launch()

