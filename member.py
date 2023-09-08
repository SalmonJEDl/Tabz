'''
Created on 14.7.2023

@author: jalma
'''

class Member():
    def __init__(self, name, member_id):
        self.name = name
        self.id = member_id
        self.spending = 0.0
        
    def add_spending(self, amount):
        self.spending += amount
        
    def zero_spending(self):
        self.spending = 0
        
    def set_spending(self, amount):
        self.spending = amount
        
    def get_info(self):
        return self.id, self.name, self.spending
        
    def __str__(self):
        return "id: {}, name: {}, spending: {}".format(self.id, self.name. self.spending)