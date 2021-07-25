########################################################
########################################################
####### File To Test Validation On Min X Field #########
########################################################
########################################################

import sys
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QMessageBox
import pytest
from plotter import CheckMinValidation
app = QApplication(sys.argv) 

def test_CheckMinXPositive():
    assert CheckMinValidation("5")==5

def test_CheckMinXNegative():
    assert CheckMinValidation("-5")==-5

def test_CheckMinXEmptyString():
    with pytest.raises(ValueError) as excinfo:   
        CheckMinValidation("") 
    assert '"" is not a number, Please enter a number' in str(excinfo.value)

def test_CheckMinXWords():
    with pytest.raises(ValueError) as excinfo:   
        CheckMinValidation("fad") 
    assert '"fad" is not a number, Please enter a number' in str(excinfo.value)

