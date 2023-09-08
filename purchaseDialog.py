'''
Created on 29.7.2023

@author: jalma
'''

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

class purchaseDialog (QDialog):
    
    def __init__(self, members):
        super(purchaseDialog, self).__init__()
        uic.loadUi("purchase.ui", self)
        self.show
        for mem in members:
            currentIndex = mem.id
            self.purchaseMemList.insertItem(currentIndex, mem.name)