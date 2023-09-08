'''
Created on 29.7.2023

@author: jalma
'''

from PyQt5 import uic
from PyQt5.Qt import QDialog

class transferDialog(QDialog):
    
    def __init__(self, members):
        super(transferDialog, self).__init__()
        uic.loadUi("transfer.ui", self)
        
        for mem in members:
            currentIndex = mem.id
            self.trPayerList.insertItem(currentIndex, mem.name)
            self.trReceiverList.insertItem(currentIndex, mem.name)