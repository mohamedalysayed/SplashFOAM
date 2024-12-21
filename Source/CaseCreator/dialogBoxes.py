from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QDialog
from PySide6.QtGui import QDoubleValidator, QIntValidator
from PySide6 import QtWidgets
from PySide6.QtWidgets import QMessageBox

#from primitives import ampersandPrimitives

import sys
from time import sleep
import os

loader = QUiLoader()
src = None

# set the path of the src folder
def set_src(src_path):
    global src
    src = src_path
#---------------------------------------------------------
main_fluids = {"Air":{"density":1.225,"viscosity":1.7894e-5,"specificHeat":1006.43,"thermalConductivity":0.0257},
               "Water":{"density":1000,"viscosity":1.002e-3,"specificHeat":4186,"thermalConductivity":0.606},
               "Nitrogen":{"density":1.165,"viscosity":1.7894e-5,"specificHeat":1006.43,"thermalConductivity":0.0257},
               "Oxygen":{"density":1.429,"viscosity":1.7894e-5,"specificHeat":1006.43,"thermalConductivity":0.0257},
               "Argon":{"density":1.784,"viscosity":1.7894e-5,"specificHeat":1006.43,"thermalConductivity":0.0257},
               "CarbonDioxide":{"density":1.977,"viscosity":1.7894e-5,"specificHeat":1006.43,"thermalConductivity":0.0257},
               "Steam":{"density":1.977,"viscosity":1.7894e-5,"specificHeat":1006.43,"thermalConductivity":0.0257},
               "R134a":{"density":1.977,"viscosity":1.7894e-5,"specificHeat":1006.43,"thermalConductivity":0.0257},
               "R22":{"density":1.977,"viscosity":1.7894e-5,"specificHeat":1006.43,"thermalConductivity":0.0257},
               "R410a":{"density":1.977,"viscosity":1.7894e-5,"specificHeat":1006.43,"thermalConductivity":0.0257},
               "R404a":{"density":1.977,"viscosity":1.7894e-5,"specificHeat":1006.43,"thermalConductivity":0.0257},
               "R123":{"density":1.977,"viscosity":1.7894e-5,"specificHeat":1006.43,"thermalConductivity":0.0257},
               "R245fa":{"density":1.977,"viscosity":1.7894e-5,"specificHeat":1006.43,"thermalConductivity":0.0257},
               "R32":{"density":1.977,"viscosity":1.7894e-5,"specificHeat":1006.43,"thermalConductivity":0.0257}}

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
        #ui_path = r"C:\Users\Ridwa\Desktop\CFD\01_CFD_Software_Development\ampersandCFD\src\createSphereDialog.ui"
        ui_path = os.path.join(src, "createSphereDialog.ui")
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
        
        self.centerX = float(self.window.lineEditSphereX.text())
        self.centerY = float(self.window.lineEditSphereY.text())
        self.centerZ = float(self.window.lineEditSphereZ.text())
        self.radius = float(self.window.lineEditSphereRadius.text())
        self.created = True
        
        self.window.close()

    def on_pushButtonCancel_clicked(self):
        
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
        #ui_path = r"C:\Users\Ridwa\Desktop\CFD\01_CFD_Software_Development\ampersandCFD\src\inputDialog.ui"
        ui_path = os.path.join(src, "inputDialog.ui")
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
        
        self.input = self.window.input.text()
        self.window.close()

    def on_pushButtonCancel_clicked(self):
        #print("Push Button Cancel Clicked")
        self.window.close()

class vectorInputDialog(QDialog):
    def __init__(self, prompt="Enter Input",input_type="float",initial_values=[0.0,0.0,0.0]):
        super().__init__()
        if initial_values != None:
            self.xx = initial_values[0]
            self.yy = initial_values[1]
            self.zz = initial_values[2]
        else:
            self.xx = 0
            self.yy = 0
            self.zz = 0
        self.OK_clicked = False
        
        self.created = False
        self.prompt = prompt
        self.input_type = input_type
        self.load_ui()

    def load_ui(self):
        #ui_path = r"C:\Users\Ridwa\Desktop\CFD\01_CFD_Software_Development\ampersandCFD\src\vectorInputDialog.ui"
        ui_path = os.path.join(src, "vectorInputDialog.ui")
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
            # show initial values
            self.window.lineEditX.setText(str(self.xx))
            self.window.lineEditY.setText(str(self.yy))
            self.window.lineEditZ.setText(str(self.zz))
        elif(self.input_type=="float"):
            self.window.lineEditX.setValidator(QDoubleValidator())
            self.window.lineEditY.setValidator(QDoubleValidator())
            self.window.lineEditZ.setValidator(QDoubleValidator())
            # show initial values
            self.window.lineEditX.setText(f"{self.xx:.3f}")
            self.window.lineEditY.setText(f"{self.yy:.3f}")
            self.window.lineEditZ.setText(f"{self.zz:.3f}")
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
        self.OK_clicked = True
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
            usage = purposeUsage[purpose]

            
            if purpose in purposeUsage.keys():
                self.window.comboBoxUsage.setCurrentText(purposeUsage[purpose])
                self.changeUsage()
            else:
                self.window.comboBoxUsage.setCurrentText("Wall")
            if usage=="Inlet" or usage=="Outlet":
                self.window.lineEditRefMin.setText(str(refMin))
                self.window.lineEditRefMax.setText(str(refMax))
                self.window.lineEditRefLevel.setText("0")
                self.window.lineEditNLayers.setText("0")
            elif usage=="Refinement_Surface" or usage=="Refinement_Region":
                #self.window.lineEditRefMin.setText(str(refMin))
                #self.window.lineEditRefMax.setText(str(refMax))
                self.window.lineEditRefLevel.setText(str(property))
                #self.window.lineEditNLayers.setText("0")
            elif usage=="Cell_Zone":
                self.window.lineEditRefLevel.setText(str(property[0]))
                self.window.checkBoxAMI.setChecked(property[1])
            elif usage=="Symmetry":
                self.window.lineEditRefLevel.setText("0")
                self.window.lineEditNLayers.setText("0")
            else: 
                self.window.lineEditRefMin.setText(str(refMin))
                self.window.lineEditRefMax.setText(str(refMax))
                self.window.lineEditRefLevel.setText(str(refMax))
                self.window.lineEditNLayers.setText(str(nLayers))
                self.window.checkBoxEdgeRefine.setChecked(featureEdges)


    def load_ui(self):
        #ui_path = r"C:\Users\Ridwa\Desktop\CFD\01_CFD_Software_Development\ampersandCFD\src\stlDialog.ui"
        ui_path = os.path.join(src, "stlDialog.ui")
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
        # to store initial values
        # these will be used as default values if cancel is clicked
        self.refMin = int(self.window.lineEditRefMin.text())
        self.refMax = int(self.window.lineEditRefMax.text())
        self.refLevel = int(self.window.lineEditRefLevel.text())
        self.nLayers = int(self.window.lineEditNLayers.text())
        self.usage = self.window.comboBoxUsage.currentText()
        self.edgeRefine = self.window.checkBoxEdgeRefine.isChecked()
        self.ami = self.window.checkBoxAMI.isChecked()

    def prepare_events(self):
        self.window.pushButtonOK.clicked.connect(self.on_pushButtonOK_clicked)
        self.window.pushButtonCancel.clicked.connect(self.on_pushButtonCancel_clicked)
        self.window.comboBoxUsage.currentIndexChanged.connect(self.changeUsage)
        # when closed the dialog box
        #self.window.resizeEvent = self.show_closed
        #self.window.closeEvent = self.show_closed

    def show_closed(self):
        
        pass

    def on_pushButtonOK_clicked(self):
        #print("Push Button OK Clicked")
        self.refMin = int(self.window.lineEditRefMin.text())
        self.refMax = int(self.window.lineEditRefMax.text())
        self.refLevel = int(self.window.lineEditRefLevel.text())
        self.nLayers = int(self.window.lineEditNLayers.text())
        self.usage = self.window.comboBoxUsage.currentText()
        self.edgeRefine = self.window.checkBoxEdgeRefine.isChecked()
        self.ami = self.window.checkBoxAMI.isChecked()
        
        self.OK_clicked = True
        self.window.close()

    def on_pushButtonCancel_clicked(self):
        self.OK_clicked = False
        self.window.close()

    def changeUsage(self):
        if(self.window.comboBoxUsage.currentText()=="Wall"):
            self.window.lineEditRefMin.setEnabled(True)
            self.window.lineEditRefMax.setEnabled(True)
            
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
            self.window.lineEditNLayers.setEnabled(False)
            self.window.lineEditNLayers.setText("0")
        elif(self.window.comboBoxUsage.currentText()=="Outlet"):
            self.window.lineEditRefLevel.setEnabled(False)
            self.window.checkBoxAMI.setEnabled(False)
            self.window.checkBoxEdgeRefine.setEnabled(True)
            self.window.lineEditNLayers.setEnabled(False)
            self.window.lineEditNLayers.setText("0")
        elif(self.window.comboBoxUsage.currentText()=="Symmetry"):
            self.window.lineEditRefLevel.setEnabled(False)
            self.window.checkBoxAMI.setEnabled(False)
            self.window.checkBoxEdgeRefine.setEnabled(False)
            self.window.lineEditRefMin.setEnabled(False)
            self.window.lineEditRefMax.setEnabled(False)
            self.window.lineEditNLayers.setEnabled(False)
            self.window.lineEditReflevel.setEnabled(False)
        elif(self.window.comboBoxUsage.currentText()=="Refinement_Surface"):
            self.window.lineEditRefLevel.setEnabled(True)
            self.window.checkBoxAMI.setEnabled(False)
            self.window.checkBoxEdgeRefine.setEnabled(False)
            self.window.lineEditRefMin.setEnabled(False)
            self.window.lineEditRefMax.setEnabled(False)
        elif(self.window.comboBoxUsage.currentText()=="Refinement_Region"):
            self.window.lineEditRefLevel.setEnabled(True)
            self.window.checkBoxAMI.setEnabled(False)
            self.window.checkBoxEdgeRefine.setEnabled(False)
            self.window.lineEditNLayers.setEnabled(False)
            self.window.lineEditNLayers.setText("0")
            self.window.lineEditRefMin.setEnabled(False)
            self.window.lineEditRefMax.setEnabled(False)
        elif(self.window.comboBoxUsage.currentText()=="Cell_Zone"):
            self.window.lineEditRefLevel.setEnabled(True)
            self.window.checkBoxAMI.setEnabled(True)
            self.window.checkBoxEdgeRefine.setEnabled(True)
        else:
            self.window.lineEditRefLevel.setEnabled(False)
            self.window.checkBoxAMI.setEnabled(True)
            self.window.checkBoxEdgeRefine.setEnabled(True)
    
    def __del__(self):
        pass

class physicalPropertiesDialog(QDialog):
    def __init__(self,initialProperties=None):
        super().__init__()
        
        self.fluids = main_fluids
        self.fluid = "Air"
        self.rho = 1.225
        self.mu = 1.7894e-5
        self.cp = 1006.43
        self.nu = self.mu/self.rho
        self.turbulenceOn = True
        self.turbulence_model = "kOmegaSST"
        self.initialProperties = None
        if initialProperties!=None:
            self.initialProperties = initialProperties
            self.fluid,self.rho,self.nu,self.cp,self.turbulence_model = initialProperties
            self.mu = self.rho*self.nu
        self.load_ui()
        self.disable_advanced_physics()
        self.fill_fluid_types()
        self.fill_turbulence_models()
        self.prepare_events()
        self.OK_clicked = False
    

    def load_ui(self):
        ##ui_path = r"C:\Users\Ridwa\Desktop\CFD\01_CFD_Software_Development\ampersandCFD\src\physicalPropertiesDialog.ui"
        ui_path = os.path.join(src, "physicalPropertiesDialog.ui")
        ui_file = QFile(ui_path)
        #ui_file = QFile("inputDialog.ui")
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file, None)
        ui_file.close()
    
    def disable_advanced_physics(self):
        self.window.checkBoxDynamicMesh.setEnabled(False)
        self.window.checkBoxMultiphase.setEnabled(False)
        self.window.checkBoxCompressibleFluid.setEnabled(False)

    def fill_fluid_types(self):
        fluid_names = list(self.fluids.keys())
        for fluid in fluid_names:
            self.window.comboBoxFluids.addItem(fluid)
        if self.initialProperties!=None:
            self.window.comboBoxFluids.addItem(self.fluid)
            self.window.comboBoxFluids.setCurrentText(self.fluid)
            self.window.lineEditRho.setText(str(self.rho))
            self.window.lineEditMu.setText(str(self.mu))
            self.window.lineEditCp.setText(str(self.cp))
        else:  
            self.window.comboBoxFluids.setCurrentText("Air")
            self.window.lineEditRho.setText(str(1.225))
            self.window.lineEditMu.setText(str(1.7894e-5))
            self.window.lineEditCp.setText(str(1006.43))
        

    def fill_turbulence_models(self):
        turbulence_models = ["laminar","k-epsilon","kOmegaSST","SpalartAllmaras","RNG_kEpsilon"
                             ,"realizableKE",]
        for model in turbulence_models:
            self.window.comboBoxTurbulenceModels.addItem(model)
        if self.initialProperties!=None:
            self.window.comboBoxTurbulenceModels.setCurrentText(self.turbulence_model)
        else:
            self.window.comboBoxTurbulenceModels.setCurrentText("kOmegaSST")

    def changeTurbulenceModel(self):
        self.turbulence_model = self.window.comboBoxTurbulenceModels.currentText()

    

    def changeFluidProperties(self):
        fluid = self.window.comboBoxFluids.currentText()
        if fluid not in self.fluids.keys():
            # set default values for Air
            self.window.lineEditRho.setText(str(1.225))
            self.window.lineEditMu.setText(str(1.7894e-5))
            self.window.lineEditCp.setText(str(1006.43))
        self.window.lineEditRho.setText(str(self.fluids[fluid]["density"]))
        self.window.lineEditMu.setText(str(self.fluids[fluid]["viscosity"]))
        self.window.lineEditCp.setText(str(self.fluids[fluid]["specificHeat"]))
        
    def prepare_events(self):
        self.window.pushButtonOK.clicked.connect(self.on_pushButtonOK_clicked)
        self.window.pushButtonCancel.clicked.connect(self.on_pushButtonCancel_clicked)
        self.window.pushButtonApply.clicked.connect(self.on_pushButtonApply_clicked) 
        self.window.comboBoxFluids.currentIndexChanged.connect(self.changeFluidProperties)
        self.window.comboBoxTurbulenceModels.currentIndexChanged.connect(self.changeTurbulenceModel)
        #self.window.checkBoxTurbulenceOn.stateChanged.connect(self.turbulenceOnOff)


    def on_pushButtonOK_clicked(self):
        #print("Push Button OK Clicked")
        self.on_pushButtonApply_clicked()
        self.OK_clicked = True
        self.window.close()

    def on_pushButtonCancel_clicked(self):
        self.window.close()

    def on_pushButtonApply_clicked(self):
        
        self.rho = float(self.window.lineEditRho.text())
        self.mu = float(self.window.lineEditMu.text())
        self.cp = float(self.window.lineEditCp.text())
        self.nu = self.mu/self.rho
        #self.turbulenceOn = self.window.checkBoxTurbulenceOn.isChecked()
        #if self.turbulenceOn:
        self.turbulence_model = self.window.comboBoxTurbulenceModels.currentText()
        #else:
        #    self.turbulence_model = "laminar"
        self.OK_clicked = True
        #self.window.close()

    def __del__(self):
        pass

class boundaryConditionDialog(QDialog):
    def __init__(self,boundary=None):
        super().__init__()
        self.boundary = boundary
        self.purpose = boundary["purpose"]
        self.pressureType = "Gauge"
        self.velocityBC = None
        self.pressureBC = None
        self.turbulenceBC = None
        self.load_ui()
        self.setNameAndType()
        self.window.setWindowTitle(f"Boundary Condition: {self.boundary['name']} ({self.boundary['purpose']})")
        self.disable_unnecessary_fields()
        self.fill_input_types()
        self.OK_clicked = False
        self.window.lineEditU.setValidator(QDoubleValidator())
        self.window.lineEditV.setValidator(QDoubleValidator())
        self.window.lineEditW.setValidator(QDoubleValidator())
        self.window.lineEditPressure.setValidator(QDoubleValidator())
        self.window.lineEditK.setValidator(QDoubleValidator())
        self.window.lineEditEpsilon.setValidator(QDoubleValidator())
        self.window.lineEditOmega.setValidator(QDoubleValidator())
        self.prepare_events()

    def disable_unnecessary_fields(self):
        if(self.purpose=="wall"):
            self.window.lineEditU.setEnabled(False)
            self.window.lineEditV.setEnabled(False)
            self.window.lineEditW.setEnabled(False)
            self.window.lineEditVelMag.setEnabled(False)
            self.window.lineEditPressure.setEnabled(False)
            self.window.lineEditIntensity.setEnabled(False)
            self.window.lineEditLengthScale.setEnabled(False)
            self.window.lineEditViscosityRatio.setEnabled(False)
            self.window.lineEditHydraulicDia.setEnabled(False)
            self.window.lineEditK.setEnabled(False)
            self.window.lineEditEpsilon.setEnabled(False)
            self.window.lineEditOmega.setEnabled(False)
        elif(self.purpose=="symmetry" or self.purpose=="refinementRegion" or self.purpose=="refinementSurface"):
            self.window.lineEditU.setEnabled(False)
            self.window.lineEditV.setEnabled(False)
            self.window.lineEditW.setEnabled(False)
            self.window.lineEditVelMag.setEnabled(False)
            self.window.lineEditPressure.setEnabled(False)
            self.window.lineEditIntensity.setEnabled(False)
            self.window.lineEditLengthScale.setEnabled(False)
            self.window.lineEditViscosityRatio.setEnabled(False)
            self.window.lineEditHydraulicDia.setEnabled(False)
            self.window.lineEditK.setEnabled(False)
            self.window.lineEditEpsilon.setEnabled(False)
            self.window.lineEditOmega.setEnabled(False)
        elif(self.purpose=="outlet"):
            self.window.lineEditK.setEnabled(False)
            self.window.lineEditEpsilon.setEnabled(False)
            self.window.lineEditOmega.setEnabled(False)
        else:
            pass


    # to set the default values of the input fields based on the boundary type
    def fill_input_types(self):
        if(self.purpose=="wall"):
            self.fill_wall_bcs()
        elif(self.purpose=="inlet"):
            self.fill_inlet_bcs()
        elif(self.purpose=="outlet"):
            self.fill_outlet_bcs()
        else:
            pass

    def setNameAndType(self):
        self.window.labelBC.setText(f"{self.boundary['name']} ({self.boundary['purpose']})")

    def prepare_events(self):
        self.window.pushButtonOK.clicked.connect(self.on_pushButtonOK_clicked)
        self.window.pushButtonCancel.clicked.connect(self.on_pushButtonCancel_clicked)
        self.window.pushButtonApply.clicked.connect(self.on_pushButtonApply_clicked)
        self.window.comboBoxVelocityStyle.currentIndexChanged.connect(self.changeVelocityStyle)
        self.window.comboBoxPressure.currentIndexChanged.connect(self.changePressureType)

        
    def changeVelocityStyle(self):
        if(self.window.comboBoxVelocityStyle.currentText()=="Components"):
            self.window.lineEditVelMag.setEnabled(False)
            self.window.lineEditU.setEnabled(True)
            self.window.lineEditV.setEnabled(True)
            self.window.lineEditW.setEnabled(True)
        else:
            self.window.lineEditVelMag.setEnabled(True)  
            self.window.lineEditU.setEnabled(False)
            self.window.lineEditV.setEnabled(False)
            self.window.lineEditW.setEnabled(False) 

    def changePressureType(self):
        if(self.window.comboBoxPressure.currentText()=="Gauge Pressure"):
            self.pressureType = "Gauge"
        else:
            self.pressureType = "Total"

    def fill_wall_bcs(self):
        # clear all items
        self.window.comboBoxVelocityStyle.clear()
        self.window.comboBoxVelocityStyle.addItem("Non-slip")
        self.window.comboBoxVelocityStyle.addItem("Slip")
        self.window.comboBoxVelocityStyle.addItem("Moving Wall")
        self.window.comboBoxPressure.clear()
        self.window.comboBoxPressure.addItem("Zero Gradient")
        #self.window.comboBoxPressure.addItem("Fixed Flux Pressure")
        self.window.comboBoxTurbulence.clear()
        self.window.comboBoxTurbulence.addItem("Wall Functions")
        #self.window.comboBoxTurbulence.addItem("Resolve Wall (y+<1)")
        # disable unnecessary fields
        self.window.lineEditU.setEnabled(False)
        self.window.lineEditV.setEnabled(False)
        self.window.lineEditW.setEnabled(False)
        self.window.lineEditVelMag.setEnabled(False)
        self.window.lineEditPressure.setEnabled(False)
        self.window.lineEditIntensity.setEnabled(False)
        self.window.lineEditLengthScale.setEnabled(False)
        self.window.lineEditViscosityRatio.setEnabled(False)
        self.window.lineEditHydraulicDia.setEnabled(False)
        self.window.lineEditK.setEnabled(False)
        self.window.lineEditEpsilon.setEnabled(False)
        self.window.lineEditOmega.setEnabled(False)

    def fill_inlet_bcs(self):
        self.window.comboBoxVelocityStyle.clear()
        self.window.comboBoxVelocityStyle.addItem("Components")
        self.window.comboBoxVelocityStyle.addItem("Normal to boundary")
        #self.window.comboBoxVelocityStyle.addItem("Parabolic Profile")
        self.window.comboBoxPressure.clear()
        self.window.comboBoxPressure.addItem("Zero Gradient")
        self.window.comboBoxPressure.addItem("Fixed Flux Pressure")
        
        self.window.comboBoxTurbulence.clear()
        self.fill_turbulence_types()

        # disable unnecessary fields
        self.window.lineEditVelMag.setEnabled(False)
        u,v,w = self.boundary["property"][0],self.boundary["property"][1],self.boundary["property"][2]
        self.window.lineEditU.setText(str(u))
        self.window.lineEditV.setText(str(v))
        self.window.lineEditW.setText(str(w))
        self.window.lineEditPressure.setEnabled(False)


    def fill_outlet_bcs(self):
        self.window.comboBoxVelocityStyle.clear()
        self.window.comboBoxVelocityStyle.addItem("Zero Gradient")
        self.window.comboBoxVelocityStyle.addItem("Inlet Outlet")
        
        self.window.comboBoxPressure.clear()
        self.window.comboBoxPressure.addItem("Fixed Value")
        self.window.comboBoxPressure.addItem("Fixed Flux Pressure")
        self.window.comboBoxTurbulence.clear()
        self.window.comboBoxTurbulence.addItem("Zero Gradient")
        self.window.comboBoxTurbulence.addItem("Inlet Outlet")
        # disable unnecessary fields
        self.window.lineEditU.setEnabled(False)
        self.window.lineEditV.setEnabled(False)
        self.window.lineEditW.setEnabled(False)
        self.window.lineEditVelMag.setEnabled(False)
        self.window.lineEditK.setEnabled(False)
        self.window.lineEditEpsilon.setEnabled(False)
        self.window.lineEditOmega.setEnabled(False)

        # set default value for pressure
        self.window.lineEditPressure.setText("0")


    def fill_turbulence_types(self):
        self.window.comboBoxTurbulence.addItem("Intensity and Length Scale")
        self.window.comboBoxTurbulence.addItem("Intensity and Viscosity Ratio")
        self.window.comboBoxTurbulence.addItem("Intensity and Hydraulic Diameter")
        self.window.comboBoxTurbulence.addItem("Turbulent Kinetic Energy (k) and Specific Dissipation Rate (omega)")
        self.window.comboBoxTurbulence.addItem("Turbulent Kinetic Energy (k) and Dissipation Rate (epsilon)")
        # default values
        self.window.comboBoxTurbulence.setCurrentText("Intensity and Length Scale")
        self.window.lineEditIntensity.setEnabled(True)
        self.window.lineEditLengthScale.setEnabled(True)
        self.window.lineEditViscosityRatio.setEnabled(False)
        self.window.lineEditHydraulicDia.setEnabled(False)
        self.window.lineEditK.setEnabled(False)
        self.window.lineEditEpsilon.setEnabled(False)
        self.window.lineEditOmega.setEnabled(False)

    def load_ui(self):
        #ui_path = r"C:\Users\Ridwa\Desktop\CFD\01_CFD_Software_Development\ampersandCFD\src\boundaryConditionDialog.ui"
        ui_path = os.path.join(src, "boundaryConditionDialog.ui")
        ui_file = QFile(ui_path)
        #ui_file = QFile("inputDialog.ui")
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file, None)
        ui_file.close()

    def on_pushButtonApply_clicked(self):
        #print("Push Button OK Clicked")
        self.OK_clicked = True
        velocity_style = self.window.comboBoxVelocityStyle.currentText()
        pressure_type = self.window.comboBoxPressure.currentText()
        if(velocity_style=="Components"):
            U = float(self.window.lineEditU.text())
            V = float(self.window.lineEditV.text())
            W = float(self.window.lineEditW.text())
            self.velocityBC = (U,V,W)
        if self.purpose=="inlet":
            if(velocity_style=="Components"):
                U = float(self.window.lineEditU.text())
                V = float(self.window.lineEditV.text())
                W = float(self.window.lineEditW.text())
                self.velocityBC = (U,V,W)
            else:
                self.velocityBC = (0,0,0)
            if(pressure_type=="Fixed Flux Pressure"):
                self.pressureBC = "fixedFluxPressure"
            else:
                self.pressureBC = "zeroGradientPressure"
        elif self.purpose=="outlet":
            if(velocity_style=="Zero Gradient"):
                self.velocityBC = "zeroGradient"
            else:
                self.velocityBC = "inletOutlet"
            self.pressureBC = self.window.lineEditPressure.text()
        elif self.purpose=="wall":
            if(velocity_style=="Non-slip"):
                self.velocityBC = "nonSlip"
            elif(velocity_style=="Slip"):
                self.velocityBC = "slip"
            else:
                self.velocityBC = "movingWall"
            self.pressureBC = "zeroGradient"
            self.turbulenceBC = "wallFunctions"
        #self.window.close()

    def on_pushButtonOK_clicked(self):
        self.on_pushButtonApply_clicked()
        self.window.close()

    def on_pushButtonCancel_clicked(self):
        self.window.close()


    def __del__(self):
        pass

class numericalSettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.load_ui()
        self.initialize_values()
        self.OK_clicked = False
    
    def load_ui(self):
        #ui_path = r"C:\Users\Ridwa\Desktop\CFD\01_CFD_Software_Development\ampersandCFD\src\numericDialog.ui"
        ui_path = os.path.join(src, "numericDialog.ui")
        ui_file = QFile(ui_path)
        #ui_file = QFile("inputDialog.ui")
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file, None)
        ui_file.close()

    def initialize_values(self):
        self.window.comboBoxBasicMode.addItem("Balanced (Blended 2nd Order schemes)")
        self.window.comboBoxBasicMode.addItem("Stablity Mode (1st Order schemes)")
        self.window.comboBoxBasicMode.addItem("Accuracy Mode (2nd Order schemes)")
        self.window.comboBoxBasicMode.addItem("Advanced Mode")
        
        self.window.comboBoxGradScheme.addItem("Gauss Linear")
        self.window.comboBoxGradScheme.addItem("cellLimited Gauss Linear")
        self.window.comboBoxGradScheme.addItem("faceLimited Gauss Linear")
        self.window.comboBoxGradScheme.addItem("Least Squares")

        self.window.comboBoxDivScheme.addItem("Gauss Linear")
        self.window.comboBoxDivScheme.addItem("Gauss Linear Upwind")
        self.window.comboBoxDivScheme.addItem("Gauss Upwind")  
        self.window.comboBoxDivScheme.addItem("Gauss LUST")      
        self.window.comboBoxDivScheme.addItem("Gauss Linear Limited")

        self.window.comboBoxLaplacian.addItem("Corrected")
        self.window.comboBoxLaplacian.addItem("Limited 0.333")
        self.window.comboBoxLaplacian.addItem("Limited 0.666")
        self.window.comboBoxLaplacian.addItem("Limited 1.0")

        self.window.comboBoxTemporal.addItem("Steady State")
        self.window.comboBoxTemporal.addItem("Euler (1st Order)")
        self.window.comboBoxTemporal.addItem("Backward Euler (2nd Order)")
        self.window.comboBoxTemporal.addItem("Crank-Nicolson (Blended 2nd Order)")
        self.window.comboBoxTemporal.addItem("Crank-Nicolson (2nd Order)")

        self.window.frame.setVisible(False)

    def prepare_events(self):
        self.window.pushButtonOK.clicked.connect(self.on_pushButtonOK_clicked)
        self.window.pushButtonCancel.clicked.connect(self.on_pushButtonCancel_clicked)
        self.window.pushButtonApply.clicked.connect(self.on_pushButtonApply_clicked)

    def on_pushButtonOK_clicked(self):
        #print("Push Button OK Clicked")
        self.OK_clicked = True
        self.window.close()

    def on_pushButtonCancel_clicked(self):
        self.window.close()

    def on_pushButtonApply_clicked(self):
        self.OK_clicked = True
        #self.window.close()


    def __del__(self):
        pass


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

def vectorInputDialogDriver(prompt="Enter Input",input_type="float",initial_values=[0.0,0.0,0.0]):
    dialog = vectorInputDialog(prompt=prompt,input_type=input_type,initial_values=initial_values)
    dialog.window.exec()
    dialog.window.show()
    xx,yy,zz = dialog.xx,dialog.yy,dialog.zz
    if dialog.OK_clicked==False:
        return None
    return (xx,yy,zz)
    

def STLDialogDriver(stl_name="stl_file.stl",stlProperties=None):
    dialog = STLDialog(stl_name=stl_name,stlProperties=stlProperties)
    dialog.window.exec()
    dialog.window.show()
    OK_clicked = dialog.OK_clicked
    if(OK_clicked==False):
        return None

    refMin = dialog.refMin
    refMax = dialog.refMax
    refLevel = dialog.refLevel
    nLayers = dialog.nLayers
    usage = dialog.usage
    edgeRefine = dialog.edgeRefine
    ami = dialog.ami
    if(dialog.usage=="Inlet"):
        # just give a temporary value. 
        # The actual value will be changed in Boundary Condition Dialog
        U = (1,0,0)
        return (refMin,refMax,refLevel,nLayers,usage,edgeRefine,ami,U)
    return (refMin,refMax,refLevel,nLayers,usage,edgeRefine,ami,None)

def physicalPropertiesDialogDriver(initialProperties=None):
    dialog = physicalPropertiesDialog(initialProperties)
    dialog.window.exec()
    dialog.window.show()
    turbulence_models = {"laminar":"laminar","k-epsilon":"kEpsilon","kOmegaSST":"kOmegaSST","SpalartAllmaras":"SpalartAllmaras",
                         "RNG_kEpsilon":"RNGkEpsilon","realizableKE":"realizableKE"}
    OK_clicked = dialog.OK_clicked
    if(OK_clicked==False):
        return None
    rho = dialog.rho
    mu = dialog.mu
    cp = dialog.cp
    nu = dialog.nu
    fluid = dialog.window.comboBoxFluids.currentText()
    turbulenceOn = dialog.turbulenceOn
    turbulence_model = turbulence_models[dialog.turbulence_model]
    #print(rho,nu,cp,turbulence_model)
    return (fluid,rho,nu,cp,turbulence_model)

def boundaryConditionDialogDriver(boundary=None):
    #print(boundary)
    dialog = boundaryConditionDialog(boundary)
    dialog.window.exec()
    dialog.window.show()
    OK_clicked = dialog.OK_clicked
    if(OK_clicked==False):
        return None
    velocityBC = dialog.velocityBC
    pressureBC = dialog.pressureBC
    turbulenceBC = dialog.turbulenceBC
    return (velocityBC,pressureBC,turbulenceBC)

def numericsDialogDriver():
    dialog = numericalSettingsDialog()
    dialog.window.exec()
    dialog.window.show()

def controlsDialogDriver():
    pass

def meshPointDialogDriver(locationInMesh=None):
    meshPoint = vectorInputDialogDriver(prompt="Enter mesh point",input_type="float",initial_values=locationInMesh)
    if(meshPoint==None):
        return None
    x,y,z = meshPoint
    return [x,y,z]

def main():
    pass

if __name__ == "__main__":
    main()