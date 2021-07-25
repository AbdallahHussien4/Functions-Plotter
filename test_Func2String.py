################################################################
################################################################
####### File To Test Validation On Function Conversion #########
################################################################
################################################################

import sys
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QMessageBox
import pytest
from plotter import ConvertStringtoFunction
app = QApplication(sys.argv) 

x=5
def test_NormalConversion():
    assert ConvertStringtoFunction("x")(x)==5

def test_XCapital():
    assert ConvertStringtoFunction("X")(x)==5

def test_XCapitalAndSpace():
    assert ConvertStringtoFunction("X + x ")(x)==10  

def test_ComplexFunctionWithNumber():
    assert ConvertStringtoFunction("5*x^3 + 2*x")(x)==635     

def test_EmptyString():
    with pytest.raises(ValueError) as excinfo:   
        assert ConvertStringtoFunction("")(x)
    assert 'No function entered' in str(excinfo.value)

def test_NotAllowedSymbols():
    with pytest.raises(ValueError) as excinfo:   
        ConvertStringtoFunction("BlaBLa") 
    assert '"B" is forbidden to use in math expression' in str(excinfo.value)
