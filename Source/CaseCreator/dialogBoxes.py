from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QDialog
from PySide6.QtGui import QDoubleValidator, QIntValidator
from PySide6 import QtWidgets
from PySide6.QtWidgets import QMessageBox

import sys
from time import sleep

loader = QUiLoader()

class sphereDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.load_ui()
        self.surfaces = []
        self.centerX = 0.0
        self.centerY = 0.0
        self.centerZ = 0.0
        self.radius = 0.0
        self.created = False
    
    def load_ui(self):
        ui_path = r"C:\Users\Ridwa\Desktop\CFD\01_CFD_Software_Development\ampersandCFD\src\createSphereDialog.ui"
        ui_file = QFile(ui_path)
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file, None)
        ui_file.close()
        #self.window.setWindowTitle("Sphere Dialog")
        self.prepare_events()
        # make text box for number only with floating points OK
        self.window.lineEditSphereX.setValidator(QDoubleValidator())
        self.window.lineEditSphereRadius.setValidator(QDoubleValidator(0.0,1e10,3))
        
    
    def prepare_events(self):
        self.window.pushButtonOK.clicked.connect(self.on_pushButtonOK_clicked)
        self.window.pushButtonCancel.clicked.connect(self.on_pushButtonCancel_clicked)
    
    def on_pushButtonOK_clicked(self):
        #print("Push Button OK Clicked")
        self.centerX = float(self.window.lineEditSphereX.text())
        self.centerY = float(self.window.lineEditSphereY.text())
        self.centerZ = float(self.window.lineEditSphereZ.text())
        self.radius = float(self.window.lineEditSphereRadius.text())
        self.created = True
        #print("Center: ",self.centerX,self.centerY,self.centerZ)
        #print("Radius: ",self.radius)
        self.window.close()

    def on_pushButtonCancel_clicked(self):
        print("Push Button Cancel Clicked")
        self.window.close()
        
    def __del__(self):
        pass

class inputDialog(QDialog):
    def __init__(self, prompt="Enter Input",input_type="string"):
        super().__init__()
        
        self.input = None
        self.created = False
        self.prompt = prompt
        self.input_type = input_type
        self.load_ui()

    def load_ui(self):
        ui_path = r"C:\Users\Ridwa\Desktop\CFD\01_CFD_Software_Development\ampersandCFD\src\inputDialog.ui"
        ui_file = QFile(ui_path)
        #ui_file = QFile("inputDialog.ui")
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file, None)
        ui_file.close()
        self.window.setWindowTitle("Input Dialog")
        self.window.labelPrompt.setText(self.prompt)
        if(self.input_type=="int"):
            self.window.input.setValidator(QIntValidator())
        elif(self.input_type=="float"):
            self.window.input.setValidator(QDoubleValidator())
        else:
            pass
        self.prepare_events()
        

    def prepare_events(self):
        self.window.pushButtonOK.clicked.connect(self.on_pushButtonOK_clicked)
        self.window.pushButtonCancel.clicked.connect(self.on_pushButtonCancel_clicked)
    
    def on_pushButtonOK_clicked(self):
        #print("Push Button OK Clicked")
        self.input = self.window.input.text()
        self.window.close()

    def on_pushButtonCancel_clicked(self):
        #print("Push Button Cancel Clicked")
        self.window.close()

class vectorInputDialog(QDialog):
    def __init__(self, prompt="Enter Input",input_type="float"):
        super().__init__()
        self.xx = 0.0
        self.yy = 0.0
        self.zz = 0.0
        
        self.created = False
        self.prompt = prompt
        self.input_type = input_type
        self.load_ui()

    def load_ui(self):
        ui_path = r"C:\Users\Ridwa\Desktop\CFD\01_CFD_Software_Development\ampersandCFD\src\vectorInputDialog.ui"
        ui_file = QFile(ui_path)
        #ui_file = QFile("inputDialog.ui")
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file, None)
        ui_file.close()
        self.window.setWindowTitle("Vector Input Dialog")
        self.window.labelPrompt.setText(self.prompt)
        if(self.input_type=="int"):
            self.window.lineEditX.setValidator(QIntValidator())
            self.window.lineEditY.setValidator(QIntValidator())
            self.window.lineEditZ.setValidator(QIntValidator())
        elif(self.input_type=="float"):
            self.window.lineEditX.setValidator(QDoubleValidator())
            self.window.lineEditY.setValidator(QDoubleValidator())
            self.window.lineEditZ.setValidator(QDoubleValidator())
        else:
            pass
        self.prepare_events()
        

    def prepare_events(self):
        self.window.pushButtonOK.clicked.connect(self.on_pushButtonOK_clicked)
        self.window.pushButtonCancel.clicked.connect(self.on_pushButtonCancel_clicked)
    
    def on_pushButtonOK_clicked(self):
        self.xx = float(self.window.lineEditX.text())
        self.yy = float(self.window.lineEditY.text())
        self.zz = float(self.window.lineEditZ.text())
        self.window.close()

    def on_pushButtonCancel_clicked(self):
        #print("Push Button Cancel Clicked")
        self.window.close()

class STLDialog(QDialog):
    def __init__(self, prompt="Enter Input"):
        super().__init__()
        self.load_ui()

    def load_ui(self):
        ui_path = r"C:\Users\Ridwa\Desktop\CFD\01_CFD_Software_Development\ampersandCFD\src\vectorInputDialog.ui"
        ui_file = QFile(ui_path)
        #ui_file = QFile("inputDialog.ui")
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file, None)
        ui_file.close()



#---------------------------------------------------------
# Driver function for different dialog boxes
#---------------------------------------------------------

def yesNoDialogDriver(prompt="Save changes to current case files",title="Save Changes"):
    msg = QMessageBox().question(None, title, prompt, QMessageBox.Yes | QMessageBox.No)
    #msg.exec_()
    if(msg==QMessageBox.Yes):
        return True
    else:
        return False
    
def yesNoCancelDialogDriver(prompt="Save changes to current case files",title="Save Changes"):
    msg = QMessageBox().question(None, title, prompt, QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
    #msg.exec_()
    if(msg==QMessageBox.Yes):
        return 1
    elif(msg==QMessageBox.No):
        return -1
    else:
        return 0

def sphereDialogDriver():
    dialog = sphereDialog()
    dialog.window.exec()
    dialog.window.show()
    x,y,z = dialog.centerX,dialog.centerY,dialog.centerZ
    r = dialog.radius
    if(dialog.created==False):
        #print("Sphere Dialog Box Closed")
        return None
    return (x,y,z,r)

def inputDialogDriver(prompt="Enter Input",input_type="string"):
    dialog = inputDialog(prompt=prompt,input_type=input_type)
    dialog.window.exec()
    dialog.window.show()
    input = dialog.input
    if(input==None):
        return None
    return input

def vectorInputDialogDriver(prompt="Enter Input",input_type="float"):
    dialog = vectorInputDialog(prompt=prompt,input_type=input_type)
    dialog.window.exec()
    dialog.window.show()
    xx,yy,zz = dialog.xx,dialog.yy,dialog.zz
    return (xx,yy,zz)
    

def main():
    pass

if __name__ == "__main__":
    main()