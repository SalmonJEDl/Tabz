'''
Created on 14.7.2023

@author: jalma
'''

class Transaction():
    def __init__(self, payer, amount, tId=-1, recipient=-1, time="", exclusion=[]):
        self.id = tId               #transaction id
        self.amount = amount
        self.payer = payer
        self.recipient = recipient  #recipient index, -1 if none
        self.exclusion = exclusion  #list of members (by index) excluded from repayments
        self.timestamp = time
        
    def get_info(self):
        return self.timestamp, self.payer, self.recipient, self.amount
    
    def matches(self, transfer):
        if transfer.payer == self.payer and transfer.recipient == self.recipient:
            return True
        return False
    
    def is_opposite(self, transaction):
        if transaction.payer == self.recipient and transaction.recipient == self.payer:
            return True
        return False
    
    def __str__(self):
        if self.timestamp:
            return self. timestamp + " | " + str(self.payer) + "->" + str(self.recipient) + " | " + str(self.amount)
        return str(self.payer) + "->" + str(self.recipient) + " | " + str(self.amount)


class Operation():
    
    def __init__(self, optype, time, name="", amount=0, exclusions=[]):
        self.timestamp = time
        self.type = optype
        self.info = ""
        if optype == "A" or type == "R":
            self.info = name
        elif optype == "B":
            self.info = str(amount)
        elif optype == "Z":
            pass
        elif optype == "E":
            self.info = exclusions
        
    def __str__(self):
        return "{} {}: {}".format(self.timestamp, self.type, self.info)