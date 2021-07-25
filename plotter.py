"""Dialog-Style application."""

import sys
import re
import numpy as np
import matplotlib.pyplot as plt
from PySide2 import QtCore
from PySide2.QtGui import QColor, QPalette, QIcon
from PySide2.QtWidgets import QApplication, QMessageBox, QSizePolicy, QDialog, QLabel, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QErrorMessage
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        #Set Window Style and features
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowSystemMenuHint |QtCore.Qt.WindowMinMaxButtonsHint)
        self.setWindowTitle('Plotter')
        self.setWindowIcon(QIcon('icon.svg'))
        self.setGeometry(700,100,500,700)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(32,178,170))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        #Plotting Figure
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setStyleSheet("background-color:White;")
        
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
        MainLayout.addWidget(self.toolbar)
        MainLayout.addWidget(self.canvas)
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
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Error")
                    msg.setInformativeText('Wrong Function Format !!, Please Use Only (+ - * / x)')
                    msg.setWindowTitle("Error")
                    msg.exec_()
                    raise ValueError(
                        '"{}" is forbidden to use in math expression'.format(char)
                    )        
            
            if string == "":
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('Please enter a valid function first :)')
                msg.setWindowTitle("Error")
                msg.exec_()
                raise ValueError(
                        'No function entered'
                    )   

            #Convert string to python code.   
            def Function(x):
                return eval(string)

            return Function        

        def CheckMinValidation(string):
            #Check if the number is negative
            Negative = False
            if string != "" and string[0] == '-':
                string = string.replace('-','')  
                Negative = True  

            string = string.replace(' ','')         #Remove spaces
            if not string.isdigit():                                                  #Check if it's not integer
                if re.match(r'^-?\d+(?:\.\d+)$', string) is None :                    #Check if it's not float
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Error")
                    msg.setFixedSize(500,500)
                    msg.setInformativeText('Please enter a valid Min number')
                    msg.setWindowTitle("Error")
                    msg.exec_()
                    raise ValueError(
                            '"{}" is not a number, Please enter a number'.format(string)
                        )       
            if (Negative):
                return -1*float(string)             
            return float(string)       

        def CheckMaxValidation(string):
            #Check if the number is negative
            Negative = False
            if string != "" and string[0] == '-':
                string = string.replace('-','')  
                Negative = True  

            string = string.replace(' ','')         #Remove spaces
            if not string.isdigit():                                                  #Check if it's not integer
                if re.match(r'^-?\d+(?:\.\d+)$', string) is None :                    #Check if it's not float
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Error")
                    msg.setInformativeText('Please enter a valid Max number')
                    msg.setWindowTitle("Error")
                    msg.exec_()
                    raise ValueError(
                            '"{}" is not a number, Please enter a number'.format(string)
                        )     
            if (Negative):
                return -1*float(string)             
            return float(string)       

        #The root function
        def Plot():
            Min = CheckMinValidation(self.MinXTextBox.text())
            Max = CheckMaxValidation(self.MaxTextBox.text())
            x = np.linspace(Min, Max, 250)
            Function = ConvertStringtoFunction(self.FunctionTextBox.text())
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(x, Function(x))
            self.canvas.draw()
            # plt.plot(x, Function(x))
            # plt.xlim(Min, Max)
            # plt.show()

    #Listening to Events
        self.PlotBtn.clicked.connect(Plot)  


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = Dialog()
    dlg.show()
    sys.exit(app.exec_())
