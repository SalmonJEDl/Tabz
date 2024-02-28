'''
Created on 19.7.2023

@author: jalma
'''

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QInputDialog, QMessageBox, QApplication, QAbstractItemView
#from PyQt5.uic.Compiler.qtproxies import QtWidgets
from tab import Tab, TAB_PATH
from actions import Transaction
import os
from webbrowser import open
from purchaseDialog import purchaseDialog
from transferDialog import transferDialog

class TabzGUI(QMainWindow):
    
    def __init__(self):
        super(TabzGUI, self).__init__()
        uic.loadUi("tabz.ui", self)
        self.autosave = True
        self.autoupdate = True
        self.tabPath = os.path.join(os.getcwd(), TAB_PATH)
        self.required_tr = []
        self.setFixedSize(800, 600)
        
        self.actionQuit.triggered.connect(exit)
        self.actionOpen_Tab.triggered.connect(self.open_tab)
        self.actionNew_Tab.triggered.connect(self.new_tab)
        self.actionSave_Tab.triggered.connect(self.save)
        self.actionAdd_member.triggered.connect(self.add_member)
        self.actionRemove_member.triggered.connect(self.remove_member)
        self.actionReplicate_Tab.triggered.connect(self.replicate)
        self.actionDirectory.triggered.connect(self.open_tab_dir)
        
        self.memList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        
        self.purchaseButton.clicked.connect(self.add_purchase)
        self.transferButton.clicked.connect(self.add_transfer)
        self.balanceButton.clicked.connect(self.balace_tab)
        self.updateButton.clicked.connect(self.print_actions)
        self.renameButton.clicked.connect(self.rename_tab)
        self.addMemButton.clicked.connect(self.add_member)
        self.exButton.clicked.connect(self.exclude)
        self.removeMemButton.clicked.connect(self.remove_member)
        self.openChildButton.clicked.connect(self.open_child)
        self.payButton.clicked.connect(self.repay)
        self.payAllButton.clicked.connect(self.repay_all)
        self.returnButton.clicked.connect(self.return_to_main)
        self.saveButton.clicked.connect(self.save)
        self.childCheckBox.toggled.connect(self.set_required_transfers)
        self.autoCheckBox.toggled.connect(self.update_toggle)
        self.trCheckBox.toggled.connect(self.action_toggle)
        self.opCheckBox.toggled.connect(self.action_toggle)
        
        self.returnButton.hide()
        
        
    def open_tab(self):
        path, ok = QFileDialog.getOpenFileName(self, "Open Tab", self.tabPath, "Text Files (*.txt)")
        if path:
            self.tab = Tab(read=True, path=path)
            self.tabName.setText(self.tab.name)
            self.refresh_info()
            self.enable_ui()
    
    
    def new_tab(self):
        tabName, ok = QInputDialog.getText(self, "Create Tab", "Tab name:")
        if ok and tabName != None:
            if tabName + ".txt" in self.find_tabs():
                self.show_error("Tabname already exists")
                return
            
            self.tab = Tab(name=tabName)
            self.clear_fields()
            self.tabName.setText(tabName)
            self.enable_ui()
    
    
    def save(self):
        self.tab.write_to_file()
    
    def add_member(self):
        #
        name, success = QInputDialog.getText(self, "Add Member", "Name:")
        if success and name != None:
            self.tab.add_member(name)
            self.refresh_info()
            #self.memList.addItem(name.replace(" ", "_"))
            
            
    def remove_member(self):
        index = self.memList.currentIndex().row()
        if index == -1:
            return
        reply = self.reconfirm_dialog("Remove member", "Do you want to remove member: {}?".format(self.tab.members[index].name))
        if reply == QMessageBox.Yes:
            self.tab.remove_member(index)
            
                
    def exclude(self):
        exclusions = self.memList.selectedItems()
        if not exclusions:
            return
        m_ids = []
        for mem in exclusions:
            m_ids.append(self.tab.find_member_id(mem.text()))
            
        reply = self.reconfirm_dialog("Exclude member(s)", "Do you want to exclude selected member(s)?")
        if reply == QMessageBox.Yes:
            name, success = QInputDialog.getText(self, "Add SubTab", "Tab name:")
            if success:
                self.tab = self.tab.exclude_members(m_ids, name = name)
                self.tabName.setText("{} ({})".format(self.tab.parent.name, self.tab.name))
                self.refresh_info()
                self.returnButton.show()
            
            
    def open_child(self):
        index = self.childList.currentIndex().row()
        if index == -1:
            return
        self.tab = self.tab.children[index]
        self.tabName.setText("{} ({})".format(self.tab.parent.name, self.tab.name))
        self.refresh_info()
        self.childCheckBox.setChecked(False)
        self.childCheckBox.setEnabled(False)
        self.returnButton.show()
            
            
    def return_to_main(self):
        if self.tab.parent:
            self.tab = self.tab.parent
            self.tabName.setText(self.tab.name)
            self.refresh_info()
            self.childCheckBox.setChecked(True)
            self.childCheckBox.setEnabled(True)
            self.returnButton.hide()
        
    
    def replicate(self):
        tabName, ok = QInputDialog.getText(self, "Create New Tab", "Tab name:")
        if ok and tabName != None:
            self.tab.change_name(tabName)
            self.tabName.setText(tabName)
            self.save()
            
    
    def rename_tab(self):
        #self.replicate()
        old_file = os.path.join(self.tabPath, "{}.txt".format(self.tab.name))
        tabName, ok = QInputDialog.getText(self, "Rename Tab", "Tab name:")
        if ok and tabName != None:
            self.tab.change_name(tabName)
            new_file = os.path.join(self.tabPath, "{}.txt".format(tabName))
            os.rename(old_file, new_file)
            self.tabName.setText(tabName)
            self.save()
        
    
    def find_tabs(self):
        #Finds existing .txt files from tab directory
        files = [file for file in os.listdir(self.tabPath) if file.endswith(".txt")]
        return files
        
        
    def add_purchase(self):
        Dialog = purchaseDialog(self.tab.members)
        Dialog.show()
        if Dialog.exec_():
            payer = Dialog.purchaseMemList.currentIndex().row()
            if payer == -1:
                self.show_error("Payer not selected.")
                return
            amount = Dialog.purchaseAmount.text()
            try:
                famount = int(float(amount.replace(",","."))*100)
            except ValueError:
                self.show_error("Invalid amount")
                return
            self.tab.add_purchase(self.tab.members[payer].id, famount)
            self.refresh_info()
        
    
    def add_transfer(self):
        Dialog = transferDialog(self.tab.members)
        Dialog.show()
        if Dialog.exec_():
            payer = Dialog.trPayerList.currentIndex().row()
            receiver = Dialog.trReceiverList.currentIndex().row()
            if payer == -1 or receiver == -1:
                self.show_error("Payer or receiver not chosen.")
                return
            if payer == receiver:
                self.show_error("Selected payer and receiver are the same.")
                return
            amount = Dialog.transferAmount.text()
            try:
                famount = int(float(amount.replace(",","."))*100)
            except ValueError:
                self.show_error("Invalid amount")
                return
            
            payment = Transaction(self.tab.members[payer].id, famount, recipient = self.tab.members[receiver].id)
            if Dialog.prioCheckBox.isChecked():
                self.pay_to_children(payment)
                if payment.amount == 0:
                    self.refresh_info()
                    return
            self.tab.add_transfer(payment.payer, payment.recipient, payment.amount)
            self.refresh_info()
            
    
    def repay(self):
        index = self.reqList.currentIndex().row()
        if index == -1:
            return
        else:
            payment = self.required_tr[index]
            if self.childCheckBox.isChecked():
                self.pay_to_children(payment)
                if payment.amount == 0:
                    self.refresh_info()
                    return
            self.tab.add_transfer(payment.payer, payment.recipient, payment.amount)
            self.refresh_info()
                
                
                
    def pay_to_children(self, payment):
        for child in self.tab.children:
            for tr in child.get_required_transfers(False):
                if payment.matches(tr):
                    if tr.amount >= payment.amount:
                        child.add_transfer(payment.payer, payment.recipient, payment.amount)
                        payment.amount = 0
                        return
                    child.add_transfer(payment.payer, payment.recipient, tr.amount)
                    payment.amount -= tr.amount
                    break
                   
    
    def repay_all(self):
        reply = self.reconfirm_dialog("Pay due transactions", "Do you want to pay all due transactions?")
        if reply == QMessageBox.Yes:
            for tr in self.tab.get_required_transfers(False):
                self.tab.add_transfer(tr.payer, tr.recipient, tr.amount)
            for child in self.tab.children:
                for tr in child.get_required_transfers(False):
                    child.add_transfer(tr.payer, tr.recipient, tr.amount)
            self.refresh_info()
        
        
    def balace_tab(self):
        self.tab.balance()
        self.refresh_info()
    
    
    def print_members(self):
        self.memList.clear()
        for index, mem in enumerate(self.tab.members):
            self.memList.insertItem(index, mem.name)
            
            
    def print_children(self):
        self.childList.clear()
        if self.tab.parent:
            return
        for index, child in enumerate(self.tab.children):
            self.childList.insertItem(index, child.name)
                
    
    def print_operations(self):
        self.transactionBrowser.clear()
        self.transactionBrowser.setText(self.tab.operations_to_string())
            
        
    def print_transactions(self):
        self.transactionBrowser.clear()
        self.transactionBrowser.setText(self.tab.transactions_to_string())
    
    
    def print_actions(self):
        if self.trCheckBox.isChecked():
            if self.opCheckBox.isChecked():
                self.transactionBrowser.clear()
                self.transactionBrowser.setText(self.tab.actions_to_string())
                return
            self.print_transactions()
            return
        if self.opCheckBox.isChecked():
            self.print_operations()
            return
        self.transactionBrowser.setText("")
    
    
    def set_required_transfers(self):
        self.reqList.clear()
        self.required_tr = self.tab.get_required_transfers(self.childCheckBox.isChecked())
        for count, tr in enumerate(self.required_tr):
            time, payer_id, recipient_id, amount = tr.get_info()
            payer = self.tab.find_member(payer_id)
            recipient = self.tab.find_member(recipient_id)
            string = "{} -> {} | {}".format(payer.name, recipient.name, str(amount/100))
            self.reqList.insertItem(count, string)

    
    
    def enable_ui(self):
        self.disableFrame.setEnabled(True)
        self.actionSave_Tab.setEnabled(True)
        self.actionReplicate_Tab.setEnabled(True)
        self.actionAdd_member.setEnabled(True)
        #self.actionRemove_member.setEnabled(True)
        self.actionAutosave.setEnabled(True)
        self.renameButton.setEnabled(True)
        self.addMemButton.setEnabled(True)
        self.exButton.setEnabled(True)
        #self.removeMemButton.setEnabled(True)
        self.openChildButton.setEnabled(True)
        self.payButton.setEnabled(True)
        self.payAllButton.setEnabled(True)
        self.childCheckBox.setEnabled(True)
        self.autoCheckBox.setEnabled(True)
        self.trCheckBox.setEnabled(True)
        self.opCheckBox.setEnabled(True)
        
        
    def clear_fields(self):
        self.memList.clear()
        self.reqList.clear()
        self.childList.clear()
        self.transactionBrowser.clear()
        #self.tabName.clear()
        
        
    def refresh_info(self):
        self.print_members()
        self.print_actions()
        self.print_children()
        self.set_required_transfers()
        
        
    def update_toggle(self):
        if self.autoCheckBox.isChecked():
            self.updateButton.setEnabled(False)
            self.print_actions()
        else:
            self.updateButton.setEnabled(True)
            
            
    def action_toggle(self):
        if self.autoCheckBox.isChecked():
            self.print_actions()
            
    
    def open_tab_dir(self):
        open(self.tabPath)
        
        
    def reconfirm_dialog(self, title, msg):
        conf = QMessageBox()
        conf.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        conf.setWindowTitle(title)
        conf.setText(msg)
        conf.setIcon(QMessageBox.Warning)
        return conf.exec_()
        
        
    def show_error(self, message, title="Error"):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Critical)
        x = msg.exec_()


def main():
    app = QApplication([])
    window = TabzGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()