#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 17:18:59 2017

@author: rivero
"""

class Bookkeeper(object):
    """
    This class controls the cash_flow, balance_sheet and inventory of an_agent
    It is responsible to maintain the consistence of the financial values of the 
    economy. All the events that update the cash, assets, liabilities or 
    inventory of the agent are responsibility of this class
    """
    
    cash_flow = None
    balance_sheet = None
    agent = None
    
    
    def __init__(self,agent,initial_assets,initial_liabilities, 
                 initial_cash):
        self.agent = agent
        self.cash_flow = CashFlow(self, agent, initial_cash)
        self.balance_sheet = BalanceSheet(self, agent,initial_assets, 
                                          initial_liabilities, initial_cash)
        
    
    def buy_gs(self,agent_seller, a_good_or_service, price):
        """
        Basic method to buy goods or services. This method:
            - Checks the agent cash
            - Starts the sell method of the seller
            - Updates the cash_flow of the agent
            - Updates the balance_sheet of the agent
        """
        date = self.agent.model.schedule.time
        if self.have_cash(price):
            if agent_seller.bookkeeper.sell_gs(self.agent,a_good_or_service,price):
                self.cash_flow.outflux(date,agent_seller.unique_id, price)
                self.balance_sheet.update_cash(self.cash_flow.available_cash)
                self.balance_sheet.add_asset(a_good_or_service)
                #print(["Agent: ", self.agent.unique_id, " buying: ", 
                #       a_good_or_service.name_of_gs,
                #       "from: ", agent_seller.unique_id])
                return True
            else:
                #print(["buy_gs - Agent: ", agent_seller.unique_id, " not selling ", 
                #       a_good_or_service.name_of_gs,
                #       "for: ", self.agent.unique_id, "***"])
                return False
        else:
            #print(["buy_gs - Agent: ", self.agent.unique_id, " doesn't have cash"])
            return False
    
    
    def sell_gs(self, agent_buyer, a_good_or_service, price):
        """
        Basic method to sell goods or services. This method is activated
        only by the buy_gs method and:
            - Checks the agent availibility of the goods to sell
            - Starts the sell method of the seller
            - Updates the cash_flow of the agent
            - Updates the balance_sheet of the agent
        """
        date = self.agent.model.schedule.time
        if self.balance_sheet.have_asset(a_good_or_service):
            self.cash_flow.influx(date,agent_buyer.unique_id, price)
            self.balance_sheet.update_cash(self.cash_flow.available_cash)
            self.balance_sheet.subtract_asset(a_good_or_service)
            return True
        else:
            #print(["sell_gs - Agent: ", self.agent.unique_id, " not selling:", 
            #       a_good_or_service.name_of_gs, "to: ",agent_buyer.unique_id,
            #       "doesn't have gs"])
            return False
        
    def have_cash(self,value):
        if self.cash_flow.available_cash > value:
            return True
        else:
            return False
        
        
    
    def payment(self,an_agent, date, value):
        """ 
        Basic method to make a payment. Just cash operation.
        considers;
        cash_flow Ag1 -> Ag2
        Agent doesn't pay if available cash is less than payment value
        """
        if self.have_cash(value):
            self.cash_flow.outflux(date,an_agent,value)
            an_agent.bookkeper.receive_payment(self.agent, date, value)
            return True
        else:
            return False
        
    def receive_payment(self, an_agent, date, value):
         """
         Basic method to receive a payment.
         Executed only by the payment method.
         """
         self.cash_flow.influx(date, an_agent,value)     
        
    
    def get_asset(self, an_asset_name):
        return self.balance_sheet.get_asset(an_asset_name)
    
    def get_liability(self, a_liability_name):
        return self.balance_sheet.get_liability(a_liability_name)

    def net_worth(self):
        worth = self.balance_sheet.net_worth()
        return worth
    
    def available_cash(self):
        cash = self.cash_flow.available_cash
        return cash
    
    


class BalanceSheet(object):
    """
    Class responsible for the balance sheet of the agent.
    Includes:
        Assets:
          10  Short term assets
              11  Cash
              12  Inventory Goods      
          20  Long term assets
        Liabilities:
          30   Short term liabilties
          40  Long term liabilities
     
    This class controls all financial records for the agent accounting
    Is updated only by the bookkeeper    
    """
    # Check the necessity to change the balance items codes
    
    assets = dict()
    liabilities = dict()  

    def __init__(self, bookkeeper, owner, assets,liabilities, initial_cash):
        self.owner = owner
        self.bookkeeper = bookkeeper
        self.assets = assets
        self.liabilities = liabilities
        self.initialize_cash(initial_cash)
    
    def initialize_cash(self, initial_cash):
        """
        Intialize the cash of the agent in the balance_sheet.
        The value of cash is updated by the bookkeper every time that some
        transaction updates the total available cash value.
        Cash here is considered "GoodOrService" object.
        """
        if not 'cash' in self.assets:
            my_cash = GoodOrService('cash',1,1.0,initial_cash,initial_cash)
            self.assets['cash'] = my_cash
                       
    def update_cash(self, value):
        """ Update agent cash in a balance_sheet object"""
        self.assets['cash'].value_of_gs = value
            

    def add_asset(self, a_good_or_service):
        """ 
        Add the quantity and value of one existing asset of the agent
        If the asset is not in the assets dict, it is included.
        """
        if a_good_or_service.name_of_gs in self.assets:
            my_gs = self.assets[a_good_or_service.name_of_gs]
            my_gs.quantity_of_gs += a_good_or_service.quantity_of_gs
            my_gs.value_of_gs += a_good_or_service.value_of_gs
            my_gs.unit_value_of_gs = a_good_or_service.unit_value_of_gs
            my_gs.avg_value_of_gs = (a_good_or_service.unit_value_of_gs + my_gs.unit_value_of_gs)/2
        else:
            self.assets[a_good_or_service.name_of_gs] = a_good_or_service
        return True
    
    def subtract_asset(self, a_good_or_service):
        """ 
        Subtract the quantity and value of one existing asset of the agent
        If the asset is not in the assets dict returns False.
        """
        if a_good_or_service.name_of_gs in self.assets:
            my_gs = self.assets[a_good_or_service.name_of_gs]
            my_gs.quantity_of_gs -= a_good_or_service.quantity_of_gs
            my_gs.value_of_gs -= a_good_or_service.value_of_gs
            my_gs.unit_value_of_gs = a_good_or_service.unit_value_of_gs
            my_gs.avg_value_of_gs = (a_good_or_service.unit_value_of_gs + my_gs.unit_value_of_gs)/2
            return True
        else:
            #print(["subtract_asset - asset no in assets"])
            return False
        
    def have_asset(self, a_gs):
           if a_gs.name_of_gs in self.assets:
              if self.assets[a_gs.name_of_gs].quantity_of_gs >= a_gs.quantity_of_gs:
                 return True
              else: 
                 #print(["have_asset - Insuficient quantity"])
                 return False
           else:
               #print(["have_asset - does not have gs"])
               return False
        


        
    def show_assets(self):
        
        print([self.owner.unique_id])           

        for an_asset_name in self.assets:
            an_asset = self.assets[an_asset_name]
            aa_name = an_asset.name_of_gs
            aa_quantity = an_asset.quantity_of_gs
            aa_price = an_asset.unit_value_of_gs
            aa_value = an_asset.value_of_gs
            print([aa_name, aa_quantity, aa_price, aa_value])
            
            return True

    def show_liabilities(self):
        print([self.owner.unique_id])           

        for a_liability_name in self.liabilities:
            a_liability = self.liabilities[a_liability_name]
            aa_name = a_liability.name_of_gs
            aa_quantity = a_liability.quantity_of_gs
            aa_price = a_liability.unit_value_of_gs
            aa_value = a_liability.value_of_gs
            print([aa_name, aa_quantity, aa_price, aa_value])
            
            return True


                          
    def add_liability(self, a_good_or_service):
        """ 
        Add the quantity and value of one existing liability of the agent
        If the liability is not in the liabilities dict, it is included.
        """
        if a_good_or_service in self.liabilities:
            my_gs = self.liabilities[a_good_or_service.name_of_gs]
            my_gs.quantity_of_gs += a_good_or_service.quantity_of_gs
            my_gs.value_of_gs += a_good_or_service.value_of_gs
            my_gs.unit_value_of_gs = a_good_or_service.unit_value_of_gs
        else:
            self.liabilities[a_good_or_service.name_of_gs] = a_good_or_service
        return True
    
    def subtract_liability(self, a_good_or_service):
        """ 
        Subtract the quantity and value of one existing liability of the agent
        If the liability is not in the liabilities dict returns False.
        """
        if a_good_or_service in self.liabilities:
            my_gs = self.liabilities[a_good_or_service.name_of_gs]
            my_gs.quantity_of_gs -= a_good_or_service.quantity_of_gs
            my_gs.value_of_gs -= a_good_or_service.value_of_gs
            my_gs.unit_value_of_gs = a_good_or_service.unit_value_of_gs
            return True
        else:
            return False

    def net_worth(self):
        """
        Answers The Net Worth of the agent
        """
        assets_values = 0.0
        liabilities_values = 0.0
        for asset_name,a_gs in self.assets.items():
            assets_values += a_gs.value_of_gs
        for liability_name, a_gs in self.liabilities.items():
            liabilities_values += a_gs.value_of_gs
        nw = assets_values - liabilities_values
        return nw

    def assets_value(self):
        """
        Answers the total monetary value of the assets
        """
        total_assets = sum(self.assets.values().value_of_gs)
        return total_assets

    def total_liabilities(self):
        """
        Answers the total liabilties of the agent
        Monetary value of the agent liabilities
        total_liabilities = sum(liabilities)
        """
        total_liabilities = sum(self.liabilities.values().value_of_gs)
        return total_liabilities
    
    def get_liability(self, a_liability_name):
        if a_liability_name in self.liabilities:
            return self.liabilities[a_liability_name]
        else:
            return False
    
    def get_asset(self, an_asset_name):
        if an_asset_name in self.assets:
            return self.assets[an_asset_name]
        else:
            return False


class CashFlow(object):
    """
    Basic cash flow class of the agent.
    It controls the initial cash value, the total available cash
    Records the cash transactions in a dict with the date and the 
    agent responsible for the transaction as the key
    """
    
    available_cash = 0.0
    initial_cash = 0.0
    transactions = dict()
    
    
    def __init__(self, bookkeeper, owner, initial_cash):
        self.initial_cash = initial_cash
        self.available_cash = initial_cash
        self.trasactions = dict()
        self.owner = owner
        self.bookkeeper = bookkeeper
        
    def influx(self, date,agent, value):
        """ Add Values to available_cash and update cash transactions """
        self.available_cash += value
        self.transactions[(date,agent)] = value
    
    def outflux(self, date, agent, value):
        """
        Check the available_cash of the agent. 
        If enough subtract values from availble_cash and update cash transactions
        """
        if self.available_cash >= value:
            self.available_cash -= value
            self.transactions[(date,agent)] = value
            value = 0.0
        else:
            value -= self.available_cash
            self.transactions[(date,agent)] = self.available_cash
            self.available_cash = 0.0

        return value
    
    
    
class Contract(object):
    """
    Basic class for contracts in the framework
    """

#==============================================================================
# Necessary to develop the semantic for this part
# Look the possibility to use (or include in the class) a network framework
#==============================================================================


    contract_type = None
    market = None
    contractor = None
    supplier = None
    total_periods = 0
    actual_period = 0
    total_value = 0.0
    asset_or_liability = None
    payment = 0.0
    
    def __init__(self,contract_type, market, contractor, supplier, total_periods,total_value, asset_or_liability, payment):
        contract_type = contract_type
        market = market
        contractor = contractor
        supplier = supplier
        total_periods = total_periods
        total_value = total_value
        self.actual_period = 0
        asset_or_liability = asset_or_liability
        payment = payment
        
    def make_payment(self, a_transaction):  
        if a_transaction.transaction_value < self.total_value:
            a_transaction.payment(self.contractor, self.supplier)            
            self.total_value -= a_transaction.transaction_value
        else:
            self.total_value = 0.0
            
            

class GoodOrService(object):
    """
    A Basic Class representing a good or service. 
    This class includes all types of goods or services of an economy
    Types of Goods:
        1 - Household - Short Term Good or Service (Consumer_Good)
        2 - Household - Long Term Good or Service (Consumer_Property)
        3 - Firm - Short Term Good or Service (Production Input_Good)
        4 - Firm - Long Term Good or Service (Capital)
    
    """
    
#==============================================================================
# It probably will be necessary to especialize this class to include the 
# specificities of the diferent goods or services.
# Type of especific goods that will probably need more detail:
#   - Capital
#   - Labour (Available_labour???) - Howto treat it as a service?
#   - Financial Assets and Liabilities (see how to include interests) 
#      
#==============================================================================
    
    name_of_gs = ''
    type_of_gs = 0
    value_of_gs = 0.0
    quantity_of_gs = 0.0
    unit_value_of_gs = 0.0
    avg_value_of_gs = 0.0

    
    def __init__(self,name_of_gs, type_of_gs, quantity_of_gs,unit_value_of_gs, value_of_gs):
        self.name_of_gs = name_of_gs
        self.type_of_gs = type_of_gs
        self.value_of_gs = value_of_gs
        self.quantity_of_gs = quantity_of_gs
        self.unit_value_of_gs = unit_value_of_gs
        self.avg_value_of_gs = unit_value_of_gs
        
        
    def name_of_gs(self):
        """ Returns the name of the good or service"""
        return self.name_of_gs
    
    
    def estimated_value_of_gs(self, a_quantity_of_gs):
        return self.unit_value_of_gs*a_quantity_of_gs
    
    def estimated_cost_of_gs(self):
        return self.unit_value_of_gs*self.quantity_of_gs
    
    
    
    

