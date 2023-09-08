# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\jalma\workspace\Tabz\purchase.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_purchaseDialog(object):
    def setupUi(self, purchaseDialog):
        purchaseDialog.setObjectName("purchaseDialog")
        purchaseDialog.resize(400, 280)
        self.addPurchaseLabel = QtWidgets.QLabel(purchaseDialog)
        self.addPurchaseLabel.setGeometry(QtCore.QRect(20, 10, 131, 16))
        self.addPurchaseLabel.setObjectName("addPurchaseLabel")
        self.purchaseAmountLabel = QtWidgets.QLabel(purchaseDialog)
        self.purchaseAmountLabel.setGeometry(QtCore.QRect(20, 180, 47, 13))
        self.purchaseAmountLabel.setObjectName("purchaseAmountLabel")
        self.lineEdit = QtWidgets.QLineEdit(purchaseDialog)
        self.lineEdit.setGeometry(QtCore.QRect(20, 200, 81, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.purchaseMemList = QtWidgets.QListWidget(purchaseDialog)
        self.purchaseMemList.setGeometry(QtCore.QRect(20, 40, 360, 130))
        self.purchaseMemList.setObjectName("purchaseMemList")
        self.horizontalLayoutWidget = QtWidgets.QWidget(purchaseDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 229, 361, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.addButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.addButton.setObjectName("addButton")
        self.horizontalLayout.addWidget(self.addButton)
        self.cancelButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        self.retranslateUi(purchaseDialog)
        self.cancelButton.clicked.connect(purchaseDialog.reject)
        self.addButton.clicked.connect(purchaseDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(purchaseDialog)

    def retranslateUi(self, purchaseDialog):
        _translate = QtCore.QCoreApplication.translate
        purchaseDialog.setWindowTitle(_translate("purchaseDialog", "Add new purchase"))
        self.addPurchaseLabel.setText(_translate("purchaseDialog", "Select a member"))
        self.purchaseAmountLabel.setText(_translate("purchaseDialog", "Amount:"))
        self.addButton.setText(_translate("purchaseDialog", "Add"))
        self.cancelButton.setText(_translate("purchaseDialog", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    purchaseDialog = QtWidgets.QDialog()
    ui = Ui_purchaseDialog()
    ui.setupUi(purchaseDialog)
    purchaseDialog.show()
    sys.exit(app.exec_())

