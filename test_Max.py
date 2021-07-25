########################################################
########################################################
####### File To Test Validation On Max X Field #########
########################################################
########################################################

import sys
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QMessageBox
import pytest
from plotter import CheckMaxValidation
app = QApplication(sys.argv) 

def test_CheckMaxXPositive():
    assert CheckMaxValidation("5")==5

def test_CheckMaxXNegative():
    assert CheckMaxValidation("-5")==-5

def test_CheckMaxXEmptyString():
    with pytest.raises(ValueError) as excinfo:   
        CheckMaxValidation("") 
    assert '"" is not a number, Please enter a number' in str(excinfo.value)

def test_CheckMaxXWords():
    with pytest.raises(ValueError) as excinfo:   
        CheckMaxValidation("fad") 
    assert '"fad" is not a number, Please enter a number' in str(excinfo.value)

