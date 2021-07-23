"""Dialog-Style application."""

import sys
import re
import numpy as np
import matplotlib.pyplot as plt
from PySide2 import QtCore
from PySide2.QtGui import QColor, QPalette
from PySide2.QtWidgets import QApplication, QSizePolicy, QDialog, QLabel, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton

class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        #Set Window Style
        self.setWindowTitle('Plotter')
        self.setGeometry(500,300,700,700)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(32,178,170))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        
        #Welcome Label
        WelcomeLabel = QLabel('Welcome to Plotter',self)
        WelcomeLabel.setMaximumHeight(50)
        WelcomeLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        WelcomeLabel.setAlignment(QtCore.Qt.AlignCenter)
        WelcomeLabel.setStyleSheet('QLabel { color: black; font-size : 40px; }')

        #Function Field
        FunctionLayout = QHBoxLayout()
        self.FunctionTextBox = QLineEdit()
        self.FunctionTextBox.setMaximumHeight(50)
        font = self.FunctionTextBox.font()
        font.setPointSize(16) # sets the size to 16
        self.FunctionTextBox.setFont(font)
        FunctionLabel = QLabel("Function")
        FunctionLabel.setStyleSheet('QLabel { color: black; font-size : 25px;}')
        FunctionLayout.addWidget(FunctionLabel)
        FunctionLayout.addWidget(self.FunctionTextBox)

        #Min Value of X field
        MinXLayout = QHBoxLayout()
        self.MinXTextBox = QLineEdit()
        self.MinXTextBox.setMaximumHeight(50)
        self.MinXTextBox.setFont(font)
        MinXLabel = QLabel("Min X")
        MinXLabel.setStyleSheet('QLabel { color: black; font-size : 25px; margin : 0 20 0 0}')
        MinXLayout.addWidget(MinXLabel)
        MinXLayout.addWidget(self.MinXTextBox)

        #Max Value of X field
        MaxLayout = QHBoxLayout()
        self.MaxTextBox = QLineEdit()
        self.MaxTextBox.setMaximumHeight(50)
        self.MaxTextBox.setFont(font)
        MaxLabel = QLabel("Max X")
        MaxLabel.setStyleSheet('QLabel { color: black; font-size : 25px; margin : 0 13 0 0}')
        MaxLayout.addWidget(MaxLabel)
        MaxLayout.addWidget(self.MaxTextBox)
        
        #Plot Button Field
        self.PlotBtn = QPushButton()
        self.PlotBtn.setFixedHeight(50)
        self.PlotBtn.setStyleSheet('QPushButton {background-color: #A3C1DA; color: black; font-size : 20px}')
        self.PlotBtn.setText("Plot")

        #Main Layout Field
        MainLayout = QVBoxLayout()
        MainLayout.addWidget(WelcomeLabel)
        MainLayout.addLayout(FunctionLayout)
        MainLayout.addLayout(MinXLayout)
        MainLayout.addLayout(MaxLayout)
        MainLayout.addWidget(self.PlotBtn)
        self.setLayout(MainLayout)

#############################################################
#############################################################
##################  Functions To Plot  ######################
#############################################################
#############################################################

        def ConvertStringtoFunction(string):
            #Prepare the string to conversion   
            string = string.replace('X','x')        #Convert to lowercase
            string = string.replace(' ','')         #Remove spaces
            string = string.replace('^','**')       #Handle power function

            # find all words and check if all are allowed:
            for char in string:
                if char != 'x' and char != '+' and char != '-' and char != '/' and char != '*' and not char.isdigit():
                    raise ValueError(
                        '"{}" is forbidden to use in math expression'.format(char)
                    )        
            
            #Convert string topython code.           
            return eval(string) 

        def CheckMinValidation(string):
            if not string.isdigit() and not string.find('.'):
                raise ValueError(
                        '"{}" is not a number, Please enter a number'.format(string)
                    )  
            return float(string)       

        def CheckMaxValidation(string):
            if not string.isdigit() and not string.find('.'):
                raise ValueError(
                        '"{}" is not a number, Please enter a number'.format(string)
                    )  
            return float(string)       

        #The root function
        def Plot():
            Min = CheckMinValidation(self.MinXTextBox.text())
            Max = CheckMaxValidation(self.MaxTextBox.text())
            x = np.linspace(Min, Max, 250)
            Function = ConvertStringtoFunction(self.FunctionTextBox.text())
            plt.plot(x, Function)
            plt.xlim(Min, Max)
            plt.show()

    #Listening to Events
        self.PlotBtn.clicked.connect(Plot)  


if __name__ == '__main__':
    x = np.linspace(-2, 2, 250)
    app = QApplication(sys.argv)
    dlg = Dialog()
    dlg.show()
    dlg.resize(640,480)
    sys.exit(app.exec_())
