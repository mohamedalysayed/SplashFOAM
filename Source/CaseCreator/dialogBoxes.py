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
    def __init__(self, stl_name="stl_file.stl",stlProperties=None):
        super().__init__()
        self.load_ui()
        self.stl_name = stl_name
        self.OK_clicked = False
        self.stl_properties = stlProperties
        self.set_initial_values()
        self.show_stl_properties()
        self.prepare_events()

    def show_stl_properties(self):
        purposeUsage = {"wall":"Wall","inlet":"Inlet","outlet":"Outlet","symmetry":"Symmetry",
                        "refinementSurface":"Refinement_Surface","refinementRegion":"Refinement_Region",
                        "cellZone":"Cell_Zone","baffles":"Baffle","interface":"Interface"}
        if self.stl_properties != None:
            purpose,refMin,refMax,featureEdges,featureLevel,nLayers,property,bounds = self.stl_properties
            self.window.lineEditRefMin.setText(str(refMin))
            self.window.lineEditRefMax.setText(str(refMax))
            self.window.lineEditRefLevel.setText(str(refMax))
            self.window.lineEditNLayers.setText(str(nLayers))
            if purpose in purposeUsage.keys():
                self.window.comboBoxUsage.setCurrentText(purposeUsage[purpose])
            else:
                self.window.comboBoxUsage.setCurrentText("Wall")


    def load_ui(self):
        ui_path = r"C:\Users\Ridwa\Desktop\CFD\01_CFD_Software_Development\ampersandCFD\src\stlDialog.ui"
        ui_file = QFile(ui_path)
        #ui_file = QFile("inputDialog.ui")
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file, None)
        ui_file.close()

    def set_initial_values(self):
        # change window title
        self.window.setWindowTitle(f"STL Properties: {self.stl_name}")
        self.window.comboBoxUsage.addItem("Wall")
        self.window.comboBoxUsage.addItem("Inlet")
        self.window.comboBoxUsage.addItem("Outlet")
        self.window.comboBoxUsage.addItem("Symmetry")
        self.window.comboBoxUsage.addItem("Refinement_Surface")
        self.window.comboBoxUsage.addItem("Refinement_Region")
        self.window.comboBoxUsage.addItem("Cell_Zone")
        self.window.comboBoxUsage.addItem("Baffle")
        self.window.comboBoxUsage.addItem("Interface")
        self.window.lineEditRefMin.setText("1")
        self.window.lineEditRefMax.setText("1")
        self.window.lineEditRefMin.setValidator(QIntValidator())
        self.window.lineEditRefMax.setValidator(QIntValidator())
        self.window.lineEditRefLevel.setText("1")
        self.window.lineEditRefLevel.setValidator(QIntValidator())
        self.window.lineEditRefLevel.setEnabled(False)
        self.window.lineEditNLayers.setText("0")
        self.window.checkBoxAMI.setChecked(False)
        self.window.checkBoxAMI.setEnabled(False)

    def prepare_events(self):
        self.window.pushButtonOK.clicked.connect(self.on_pushButtonOK_clicked)
        self.window.pushButtonCancel.clicked.connect(self.on_pushButtonCancel_clicked)
        self.window.comboBoxUsage.currentIndexChanged.connect(self.changeUsage)
        # when closed the dialog box
        self.window.closeEvent = self.on_pushButtonCancel_clicked

    def on_pushButtonOK_clicked(self):
        print("Push Button OK Clicked")
        self.refMin = int(self.window.lineEditRefMin.text())
        self.refMax = int(self.window.lineEditRefMax.text())
        self.refLevel = int(self.window.lineEditRefLevel.text())
        self.nLayers = int(self.window.lineEditNLayers.text())
        self.usage = self.window.comboBoxUsage.currentText()
        self.edgeRefine = self.window.checkBoxEdgeRefine.isChecked()
        self.ami = self.window.checkBoxAMI.isChecked()

        #print("Refinement Min: ",self.refMin)
        #print("Refinement Max: ",self.refMax)
        #print("Refinement Level: ",self.refLevel)
        #print("Number of Layers: ",self.nLayers)
        #print("Usage: ",self.usage)
        #print("Edge Refine: ",self.edgeRefine)
        #print("AMI: ",self.ami)
        if(self.usage=="Inlet"):
            xx,yy,zz = vectorInputDialogDriver(prompt="Enter Inlet Velocity Vector",input_type="float")
            print("Inlet Velocity: ",xx,yy,zz)
            self.xx = xx
            self.yy = yy
            self.zz = zz
        self.OK_clicked = True
        self.window.close()

    def on_pushButtonCancel_clicked(self):
        #print("Push Button Cancel Clicked")
        self.OK_clicked = False
        self.window.close()

    def changeUsage(self):
        if(self.window.comboBoxUsage.currentText()=="Wall"):
            self.window.lineEditRefLevel.setEnabled(False)
            self.window.checkBoxAMI.setEnabled(False)
            self.window.checkBoxEdgeRefine.setEnabled(True)
        elif(self.window.comboBoxUsage.currentText()=="Baffle"):
            self.window.lineEditRefLevel.setEnabled(False)
            self.window.checkBoxAMI.setEnabled(False)
            self.window.checkBoxEdgeRefine.setEnabled(True)
        elif(self.window.comboBoxUsage.currentText()=="Inlet"):
            self.window.lineEditRefLevel.setEnabled(False)
            self.window.checkBoxAMI.setEnabled(False)
            self.window.checkBoxEdgeRefine.setEnabled(True)
        elif(self.window.comboBoxUsage.currentText()=="Outlet"):
            self.window.lineEditRefLevel.setEnabled(False)
            self.window.checkBoxAMI.setEnabled(False)
            self.window.checkBoxEdgeRefine.setEnabled(True)
        elif(self.window.comboBoxUsage.currentText()=="Symmetry"):
            self.window.lineEditRefLevel.setEnabled(False)
            self.window.checkBoxAMI.setEnabled(False)
            self.window.checkBoxEdgeRefine.setEnabled(True)
        elif(self.window.comboBoxUsage.currentText()=="Refinement_Surface"):
            self.window.lineEditRefLevel.setEnabled(True)
            self.window.checkBoxAMI.setEnabled(False)
            self.window.checkBoxEdgeRefine.setEnabled(False)
        elif(self.window.comboBoxUsage.currentText()=="Refinement_Region"):
            self.window.lineEditRefLevel.setEnabled(True)
            self.window.checkBoxAMI.setEnabled(False)
            self.window.checkBoxEdgeRefine.setEnabled(False)
        elif(self.window.comboBoxUsage.currentText()=="Cell_Zone"):
            self.window.lineEditRefLevel.setEnabled(True)
            self.window.checkBoxAMI.setEnabled(True)
            self.window.checkBoxEdgeRefine.setEnabled(True)
        else:
            self.window.lineEditRefLevel.setEnabled(False)
            self.window.checkBoxAMI.setEnabled(True)
            self.window.checkBoxEdgeRefine.setEnabled(True)
        
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
    

def STLDialogDriver(stl_name="stl_file.stl",stlProperties=None):
    dialog = STLDialog(stl_name=stl_name,stlProperties=stlProperties)
    dialog.window.exec()
    dialog.window.show()
    if(dialog.OK_clicked==False):
        return None
    refMin = dialog.refMin
    refMax = dialog.refMax
    refLevel = dialog.refLevel
    nLayers = dialog.nLayers
    usage = dialog.usage
    edgeRefine = dialog.edgeRefine
    ami = dialog.ami
    if(dialog.usage=="Inlet"):
        xx = dialog.xx
        yy = dialog.yy
        zz = dialog.zz
        U = (xx,yy,zz)
        return (refMin,refMax,refLevel,nLayers,usage,edgeRefine,ami,U)
    return (refMin,refMax,refLevel,nLayers,usage,edgeRefine,ami,None)

def main():
    pass

if __name__ == "__main__":
    main()