# -*- coding: utf-8 -*-
"""
EcoSim Agent-Based Modeling Framework
Based on Mesa

Core Objects: EcoModelBasic
              EconomicAgent.

"""
import datetime

from .model import Model
from .agent import Agent


__all__ = ["EcoModelBasic", "EconomicAgent", "Model", "Agent"]

__title__ = 'EcoSim'
__version__ = '0.0.0'
__license__ = 'GNU'
__copyright__ = 'Copyright %s Eco_Sim' % datetime.date.today().year

