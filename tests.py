'''
Created on 15.7.2023

@author: jalma
'''
from tab import Tab
from actions import Transaction, Operation
import os

def test1():
    tab = Tab(name="Test")
    tab.add_member("Pekka")
    tab.add_member("Kalle")
    tab.add_member("Keijo")
    tab.add_member("Maija")
    tab.add_purchase(0, 60.0)
    tab.add_purchase(2, 90.0)
    tab.add_transfer(1, 2, 20.0)
    tab.add_purchase(3, 150)
    print(tab)
    '''for i in tab.get_required_transfers():
        print(i)'''
    #tab.write_to_file()
    print(tab.transactions_to_string())
    
def test2():
    tab = Tab(read=True, file="Test.txt")
    tab.change_name("Test2")
    tab.add_purchase(tab.find_member_id("Keijo"), 15.0)
    print(tab)
    #tab.write_to_file()
    
    
def test3():
    tran = Transaction(1, 50.0, time="")
    print(tran)
    
    
def test4():
    tab = Tab(read=True, file="Test.txt")
    #for i in tab.get_required_transfers():
    #    print(i)
    print(tab)
    #print(tab.operations_to_string())
    
    
def test5():
    tab = Tab(read=True, file="Test5.txt")
    subtab = tab.exclude_members([1,2])
    print(tab.members_to_string())
    print(subtab.members_to_string())
    
    subtab.add_purchase(3, 15.5)
    subtab.add_transfer(0, 3, 5.0)
    print(tab)
    tab.change_name("Test6")
    tab.write_to_file()
    
    
def test6():
    tab = Tab(read=True, file="Test6.txt")
    print(tab)
    
test6()
