#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 17:59:56 2019

@author: Caleb Powell
"""

from PyQt5.QtWidgets import QDialog
import pandas as pd
from ui.importindexdialogUI import Ui_importIndexDialog


class importDialog(QDialog):
    def __init__(self, parent=None, df=False):
        super().__init__()
        self.init_ui(parent, df)
           
    def init_ui(self, parent, df):
        if isinstance(df, pd.DataFrame):
            self.parent = parent  # this is the master window
            importDialog = Ui_importIndexDialog()
            importDialog.setupUi(self)
            self.df = df
            # populate the qcombo boxes
            for box in [importDialog.value_Existing_Specimen_Numbers,
                        importDialog.value_Existing_Site_Numbers]:
                self.populateQComboBox(box)
            self.importDialog = importDialog
            self.importDialog.pushButton_Assign.clicked.connect(self.accept)
            self.importDialog.pushButton_Assign.setFocus(True)
            self.importDialog.pushButton_Cancel.clicked.connect(self.reject)

    def populateQComboBox(self, obj):
        """ Populates the options in the QComboBox"""
        obj.clear()
        colNames = self.df.columns.tolist()
        obj.addItems(colNames)

    def indexAssignments(self):
        """ harvests the settings, made in the dialog and performs the
        appropriate assignments"""

        useExistingSpecimen = self.importDialog.value_Use_Existing_Specimen_Numbers
        if useExistingSpecimen.isChecked():
            # copy the user defined column over to specimenNumber
            existingCol = self.importDialog.value_Existing_Specimen_Numbers.currentText()
            self.df['specimenNumber'] = self.df[existingCol]
        else:
            # generate sequential specimenNumbers
            numSeq = [str(x+1) for x in range(len(self.df))]
            self.df['specimenNumber'] = numSeq
        useExistingSite = self.importDialog.value_Use_Existing_Site_Numbers
        if useExistingSite.isChecked():
            # generate sequential siteNumbers
            existingCol = self.importDialog.value_Existing_Site_Numbers.currentText()
            self.df['siteNumber'] = self.df[existingCol]
        else:
            # generate sequential siteNumbers
            numSeq = [str(x+1) for x in range(len(self.df))]
            self.df['siteNumber'] = numSeq

        return self.df
