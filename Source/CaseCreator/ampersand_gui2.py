from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QMainWindow
from PySide6 import QtWidgets
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from dialogBoxes import sphereDialogDriver, yesNoDialogDriver, yesNoCancelDialogDriver
from dialogBoxes import vectorInputDialogDriver, STLDialogDriver, physicalPropertiesDialogDriver
from dialogBoxes import boundaryConditionDialogDriver, numericsDialogDriver, controlsDialogDriver
# ----------------- VTK Libraries ----------------- #
import vtk
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkInteractionWidgets import vtkOrientationMarkerWidget
from vtkmodules.vtkRenderingAnnotation import vtkAxesActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)
# ------------------------------------------------- #
import sys
import os
from time import sleep

# Connection to the Ampersand Backend
from project import ampersandProject
from primitives import ampersandPrimitives, ampersandIO

os.chdir(r"C:\Users\Ridwa\Desktop\CFD\01_CFD_Software_Development\ampersandCFD\src")
loader = QUiLoader()

# This function reads STL file and extracts the surface patch names.
def readSTL(stlFileName="cylinder.stl"):
    surfaces = [] # to store the surfaces in the STL file
    try:
        f = open(stlFileName, "r")
        for x in f:
            
            items = x.split(" ")
            if(items[0]=='solid'):
                surfaces.append(items[1][:-1])
                #print(items[1][:-1])
        f.close()
    except:
        print("Error while opening file: ",stlFileName)
    return surfaces


# This is the main window class
class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_ui()
        self.surfaces = []
        self.project_opened = False
        self.project = None #ampersandProject(GUIMode=True,window=self)
        self.minx,self.miny,self.minz = 0.0,0.0,0.0
        self.maxx,self.maxy,self.maxz = 0.0,0.0,0.0
        self.nx,self.ny,self.nz = 0,0,0
        self.current_stl_file = None
        self.colorCounter = 0
        # disable all the buttons and input fields
        #self.disableButtons()

    def disableButtons(self):
        self.pushButtonSTLImport.setEnabled(False)
        self.pushButtonSphere.setEnabled(False)
        self.pushButtonBox.setEnabled(False)
        self.pushButtonCylinder.setEnabled(False)
        self.radioButtonInternal.setEnabled(False)
        self.radioButtonExternal.setEnabled(False)
        self.checkBoxOnGround.setEnabled(False)
        self.pushButtonSTLProperties.setEnabled(False)
        self.pushButtonPhysicalProperties.setEnabled(False)
        self.pushButtonBoundaryCondition.setEnabled(False)
        self.pushButtonNumerics.setEnabled(False)
        self.pushButtonControls.setEnabled(False)
        self.pushButtonDomainAuto.setEnabled(False)
        self.pushButtonDomainManual.setEnabled(False)
        #self.pushButtonCreate.setEnabled(False)
        #self.pushButtonOpen.setEnabled(False)
        self.pushButtonGenerate.setEnabled(False)
        self.pushButtonSave.setEnabled(False)
        self.lineEditMinX.setEnabled(False)
        self.lineEditMinY.setEnabled(False)
        self.lineEditMinZ.setEnabled(False)
        self.lineEditMaxX.setEnabled(False)
        self.lineEditMaxY.setEnabled(False)
        self.lineEditMaxZ.setEnabled(False)
        self.lineEdit_nX.setEnabled(False)
        self.lineEdit_nY.setEnabled(False)
        self.lineEdit_nZ.setEnabled(False)
        # change color of widget 
        self.widget.setStyleSheet('''background-color: lightgrey;''')
        self.plainTextTerminal.appendPlainText("Welcome to SplashFOAM Case Creator")
       
    def enableButtons(self):
        self.pushButtonSTLImport.setEnabled(True)
        self.pushButtonSphere.setEnabled(True)
        self.pushButtonBox.setEnabled(True)
        self.pushButtonCylinder.setEnabled(True)
        self.radioButtonInternal.setEnabled(True)
        self.radioButtonExternal.setEnabled(True)
        self.checkBoxOnGround.setEnabled(True)
        self.pushButtonSTLProperties.setEnabled(True)
        self.pushButtonPhysicalProperties.setEnabled(True)
        self.pushButtonBoundaryCondition.setEnabled(True)
        self.pushButtonNumerics.setEnabled(True)
        self.pushButtonControls.setEnabled(True)
        self.pushButtonCreate.setEnabled(True)
        self.pushButtonOpen.setEnabled(True)
        self.pushButtonGenerate.setEnabled(True)
        self.pushButtonSave.setEnabled(True)
        self.pushButtonDomainAuto.setEnabled(True)
        self.pushButtonDomainManual.setEnabled(True)
        self.lineEditMinX.setEnabled(True)
        self.lineEditMinY.setEnabled(True)
        self.lineEditMinZ.setEnabled(True)
        self.lineEditMaxX.setEnabled(True)
        self.lineEditMaxY.setEnabled(True)
        self.lineEditMaxZ.setEnabled(True)
        self.lineEdit_nX.setEnabled(True)
        self.lineEdit_nY.setEnabled(True)
        self.lineEdit_nZ.setEnabled(True)

    def load_ui(self):
        ui_file = QFile("ampersandInputForm.ui")
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()
        self.setWindowTitle("Ampersand Input Form")
        #self.prepare_vtk()
        #self.prepare_subWindows()
        #self.prepare_events()

    def __del__(self):
        pass

    def openCADDialog(self):
        fname,ftype = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 
        'c:\\',"CAD files (*.brep *.igs *.iges)")
        if(fname==""):
            return -1 # CAD file not loaded
        else:
            #print("Current CAD File: ",fname)
            return fname
                       
    # manage sub windows
    def prepare_subWindows(self):
        self.createCaseWindow = None

    def prepare_vtk(self):
        # Prepare the VTK widget to show the STL
        self.vl = QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.widget)
        self.vl.addWidget(self.vtkWidget)
        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.vtkWidget.resize(891,471)
        # change the background color to black
        colors = vtk.vtkNamedColors()
        whiteColor = colors.GetColor3d("White")
        blackColor = colors.GetColor3d("Black")
        self.ren.GradientBackgroundOn()
        self.ren.SetBackground(whiteColor)
        self.ren.SetBackground2(blackColor)
        #self.ren.SetBackground(0, 0, 0)
        #self.ren.SetBackground(0.1, 0.2, 0.4)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        #self.reader = vtk.vtkSTLReader()
        #self.render3D()
        self.initializeVTK()
        #self.iren.Initialize()
        #self.iren.Start()

    # this function will read STL file and show it in the VTK renderer
    def showSTL(self,stlFile=r"C:\Users\mrtha\Desktop\GitHub\foamAutoGUI\src\pipe.stl"):
        # Read stl
        try:
            self.reader = vtk.vtkSTLReader()
            self.reader.SetFileName(stlFile)
            self.render3D()
        except:
            print("Reading STL not successful. Try again")

    def initializeVTK(self):
        # Create a mapper
        #mapper = vtk.vtkPolyDataMapper()
        #mapper.SetInputConnection(self.reader.GetOutputPort())
        # Create an actor
        actor = vtk.vtkActor()
        #actor.SetMapper(mapper)
        actor.GetProperty().EdgeVisibilityOn()
        colors = vtk.vtkNamedColors()
        whiteColor = colors.GetColor3d("Grey")
        blackColor = colors.GetColor3d("Black")
        #deepBlue = colors.GetColor3d("DeepBlue")
        #self.ren.SetBackground(colors.GetColor3d("SlateGray"))
        # set background color as gradient
        self.ren.GradientBackgroundOn()
        self.ren.SetBackground(whiteColor)
        self.ren.SetBackground2(blackColor)
        self.ren.AddActor(actor)
        style = vtk.vtkInteractorStyleTrackballCamera()
        self.iren.SetInteractorStyle(style)
        camera = vtk.vtkCamera()
        camera.SetPosition(-1, 1, 1)
        camera.SetFocalPoint(0, 0, 0)
        camera.SetViewUp(0, 0, 1)
        self.ren.SetActiveCamera(camera)
        self.iren.Initialize()
        # add coordinate axes
        axes = vtk.vtkAxesActor()
        self.ren.AddActor(axes)
        self.iren.Start()
        """
        widget = vtkOrientationMarkerWidget()
        #renderWindowInteractor = vtkRenderWindowInteractor()
        rgba = [0] * 4
        colors.GetColor('Carrot', rgba)
        widget.SetOutlineColor(rgba[0], rgba[1], rgba[2])
        widget.SetOrientationMarker(axes)
        widget.SetInteractor(self.iren)
        widget.SetViewport(0.0, 0.0, 0.4, 0.4)
        widget.SetEnabled(1)
        widget.InteractiveOn()
        """
        

    def render3D(self):  # self.ren and self.iren must be used. other variables are local variables
        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(self.reader.GetOutputPort())
        # Create an actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        #actor.GetProperty().EdgeVisibilityOn()
        # set random colors to the actor
        colors = vtk.vtkNamedColors()
        listOfColors = ["Pink","Red","Green","Blue","Yellow","Orange","Purple","Cyan","Magenta","Brown",]
        if(self.colorCounter>9):
            self.colorCounter = 0
        actor.GetProperty().SetColor(colors.GetColor3d(listOfColors[self.colorCounter]))
        self.ren.AddActor(actor)
        axes = vtk.vtkAxesActor()
        self.ren.AddActor(axes)
        self.colorCounter += 1
        
        #self.iren.Start()

    def add_object_to_VTK(self,object,objectName="sphere",opacity=0.5,removePrevious=False):
        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(object.GetOutputPort())
        # Create an actor
        actor = vtk.vtkActor()
        actor.GetProperty().SetOpacity(opacity)
        actor.GetProperty().SetColor(0.5,0.5,0.5)
        actor.GetProperty().SetObjectName(objectName)
        actor.GetProperty().EdgeVisibilityOn()
        actor.SetMapper(mapper)
        # remove the previous object
        if(removePrevious):
            currentActors = self.ren.GetActors()
            for act in currentActors:
                if(act.GetProperty().GetObjectName()==objectName):
                    self.ren.RemoveActor(act)
        self.ren.AddActor(actor)
        self.iren.Start()

    def add_sphere_to_VTK(self):
        # Create a sphere
        sphere = vtk.vtkSphereSource()
        sphere.SetCenter(0.0, 0.0, 0.0)
        sphere.SetRadius(1.0)
        self.add_object_to_VTK(sphere,objectName="sphere",removePrevious=True)
       

    def add_box_to_VTK(self,minX=0.0,minY=0.0,minZ=0.0,maxX=1.0,maxY=1.0,maxZ=1.0,boxName="box"):
        # Create a cube
        cube = vtk.vtkCubeSource()
        cube.SetXLength(maxX-minX)
        cube.SetYLength(maxY-minY)
        cube.SetZLength(maxZ-minZ)
        cube.SetCenter((maxX+minX)/2,(maxY+minY)/2,(maxZ+minZ)/2)
        # make box transparent

        cubeMapper = vtk.vtkPolyDataMapper()
        cubeMapper.SetInputConnection(cube.GetOutputPort())
        cubeActor = vtk.vtkActor()
        cubeActor.GetProperty().SetOpacity(0.5)
        cubeActor.GetProperty().SetColor(0.5,0.5,0.5)
        cubeActor.GetProperty().SetObjectName(boxName)
        cubeActor.SetMapper(cubeMapper)
        # remove the previous box
        currentActors = self.ren.GetActors()
        for actor in currentActors:
            if(actor.GetProperty().GetObjectName()==boxName):
                self.ren.RemoveActor(actor)
        self.ren.AddActor(cubeActor)
        currentActors = self.ren.GetActors()
        
        #self.ren.ResetCamera()
        self.iren.Start()
    
    def loadSTL(self,stlFile = r"C:\Users\mrtha\Desktop\GitHub\foamAutoGUI\src\pipe.stl"):
        ampersandIO.printMessage("Loading STL file")
        stl_name = stlFile.split("/")[-1]
        if(stl_name in self.surfaces):
            self.updateStatusBar("STL file already loaded")
            return
        self.surfaces.append(stl_name)
        print(self.surfaces)
        idx = len(self.surfaces)
        self.listWidgetObjList.insertItem(idx,stl_name)
        message = "Loaded STL file: "+stlFile
        self.updateStatusBar(message) 

    def update_list(self):
        self.listWidgetObjList.clear()
        for i in range(len(self.project.stl_files)):
            self.listWidgetObjList.insertItem(i,self.project.stl_files[i]['name'])

    def updatePropertyBox(self):
        # find the selected item in the list
        item = self.listWidgetObjList.currentItem()
        idx = self.listWidgetObjList.row(item)
        
        self.current_stl_file = item.text()
        #print("Selected Item: ",self.current_stl_file)
        # find the properties of the selected item
        #print("Current STL File: ",self.current_stl_file)
        #print(self.project.stl_files)
        stl_properties = self.project.get_stl_properties(self.current_stl_file)
        if stl_properties==None:
            return
        purpose,refMin,refMax,featureEdges,featureLevel,nLayers,property,bounds = stl_properties
        #print("STL Properties: ",refMin,refMax,featureEdges,featureLevel,nLayers,property,bounds)
        return
        # update the property box
        self.tableViewProperties.setItem(0,0,QtWidgets.QTableWidgetItem("Refinement Min"))
        #self.tableViewProperties.setItem(0,0,QtWidgets.QTableWidgetItem(str(refMin)))
        self.tableViewProperties.setItem(0,1,QtWidgets.QTableWidgetItem(str(refMax)))
        self.tableViewProperties.setItem(1,0,QtWidgets.QTableWidgetItem(str(featureEdges)))
        self.tableViewProperties.setItem(1,1,QtWidgets.QTableWidgetItem(str(featureLevel)))
        self.tableViewProperties.setItem(2,0,QtWidgets.QTableWidgetItem(str(nLayers)))
        self.tableViewProperties.setItem(2,1,QtWidgets.QTableWidgetItem(str(property)))
        self.tableViewProperties.setItem(3,0,QtWidgets.QTableWidgetItem(str(bounds[0])))
        
    def updateStatusBar(self,message="Go!"):
        self.statusbar.showMessage(message)
        self.plainTextTerminal.appendPlainText(message)

    def updateTerminal(self,message="Go!"):
        self.plainTextTerminal.appendPlainText(message)

    def readyStatusBar(self):
        # pause 1 millisecond
        sleep(0.001)
        self.statusbar.showMessage("Ready")

    def prepare_events(self):
        #self.resizeEvent = self.resizeEventTriggered
        #self.closeEvent = self.closeEventTriggered
        # Initiate the button click maps
        self.pushButtonSTLImport.clicked.connect(self.importSTL)
        self.pushButtonSphere.clicked.connect(self.createSphere)
        self.actionNew_Case.triggered.connect(self.createCase)
        self.actionOpen_Case.triggered.connect(self.openCase)
        self.actionSave_Case.triggered.connect(self.saveCase)
        self.pushButtonCreate.clicked.connect(self.createCase)
        self.pushButtonOpen.clicked.connect(self.openCase)
        self.actionExit.triggered.connect(self.close)
        self.pushButtonGenerate.clicked.connect(self.generateCase)
        self.pushButtonSave.clicked.connect(self.saveCase)
        self.radioButtonInternal.clicked.connect(self.chooseInternalFlow)
        self.radioButtonExternal.clicked.connect(self.chooseExternalFlow)
        self.listWidgetObjList.itemClicked.connect(self.updatePropertyBox)
        self.pushButtonDomainAuto.clicked.connect(self.autoDomain)
        self.pushButtonDomainManual.clicked.connect(self.manualDomain)
        self.pushButtonSTLProperties.clicked.connect(self.stlPropertiesDialog)
        self.pushButtonPhysicalProperties.clicked.connect(self.physicalPropertiesDialog)
        self.pushButtonBoundaryCondition.clicked.connect(self.boundaryConditionDialog)
        self.pushButtonNumerics.clicked.connect(self.numericsDialog)
        self.pushButtonControls.clicked.connect(self.controlsDialog)
        #self.checkBoxOnGround.clicked.connect(self.chooseExternalFlow)
        # change view on the VTK widget
        self.pushButtonFitAll.clicked.connect(self.vtkFitAll)
        self.pushButtonPlusX.clicked.connect(self.vtkPlusX)
        self.pushButtonPlusY.clicked.connect(self.vtkPlusY)
        self.pushButtonPlusZ.clicked.connect(self.vtkPlusZ)
        self.pushButtonMinusX.clicked.connect(self.vtkMinusX)
        self.pushButtonMinusY.clicked.connect(self.vtkMinusY)
        self.pushButtonMinusZ.clicked.connect(self.vtkMinusZ)
        self.pushButtonShowWire.clicked.connect(self.vtkShowWire)
        self.pushButtonShowSurface.clicked.connect(self.vtkShowSurface)
        self.pushButtonShowEdges.clicked.connect(self.vtkShowEdges)

        #self.resizeEvent = self.resizeEvent
        #self.closeEvent = self.closeEvent
        self.statusbar.showMessage("Ready")

#----------------- Event Handlers -----------------#
    def importSTL(self):
        #self.updateStatusBar("Opening STL")
        #self.openSTL()
        #self.readyStatusBar()
        stl_status = self.project.add_stl_file()
        if stl_status==-1:
            #ampersandIO.printError("STL file not loaded",GUIMode=True,window=self)
            return
        #self.project.analyze_stl_file()
        self.project.add_stl_to_project()
        self.showSTL(stlFile=self.project.current_stl_file)
        self.update_list()
        #self.project.list_stl_files()

    def importMultipleSTL(self):
        # show the file dialog
        filters = "STL files (*.stl)"
        fileDialog = QtWidgets.QFileDialog()
        fileDialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        stlList = fileDialog.getOpenFileNames(self,"Open STL files",r"C:\Users\mrtha\Desktop\GitHub\foamAutoGUI\src",filters)
        print(stlList[0])
        if(len(stlList[0])==0):
            return
        for stl in stlList[0]:
            status = self.project.add_one_stl_file(stl)
            if status==-1:
                ampersandIO.printError(f"STL file {stl} not loaded",GUIMode=True,window=self)
                #return
            self.project.add_stl_to_project()
            self.showSTL(stlFile=stl)
        self.update_list()
        self.readyStatusBar()
    
    def createSphere(self):
        #print("Create Sphere")
        ampersandIO.printMessage("Creating Sphere",GUIMode=True,window=self)
        # create a sphere dialog
        sphereData = sphereDialogDriver()
        if sphereData == None:
            ampersandIO.printError("Sphere Dialog Box Closed",GUIMode=True)
        else:
            x,y,z,r = sphereData
            print("Center: ",x,y,z)
            print("Radius: ",r)
        self.readyStatusBar()

    def resizeEvent(self, event):
        print("Resizing")
        #self.resizeEvent(event)
        #QtWidgets.QMainWindow.resizeEvent(self, event)
        #self.vtkWidget.resize(self.widget.size())

    def closeEventTriggered(self, event):
        print("Closing")
        self.close()

    def chooseInternalFlow(self):
        #print("Choose Internal Flow")
        self.project.internalFlow = True
        self.project.meshSettings['internalFlow'] = True
        self.project.onGround = False
        self.checkBoxOnGround.setEnabled(False)
        self.updateStatusBar("Choosing Internal Flow")
        #sleep(0.001)
        self.readyStatusBar()

    def chooseExternalFlow(self):
        self.project.internalFlow = False
        self.project.meshSettings['internalFlow'] = False
        self.checkBoxOnGround.setEnabled(True)
        self.project.meshSettings['onGround'] = self.checkBoxOnGround.isChecked()
        self.project.onGround = self.checkBoxOnGround.isChecked()
        self.updateStatusBar("Choosing External Flow")
        sleep(0.001)
        self.readyStatusBar()

    def createCase(self):
        if self.project_opened:
            # ask yes or no or cancel
            yNC = yesNoCancelDialogDriver("Save changes to current case files before creating a New Case","Save Changes")
            if yNC==1: # if yes
                # save the project
                self.project.add_stl_to_project()
                self.project.write_settings()
                self.disableButtons()
                self.ren.RemoveAllViewProps()
            elif yNC==-1: # if no
                # close the project
                self.project = None
                self.project_opened = False
                self.disableButtons()
                self.ren.RemoveAllViewProps()
            else: # if cancel
                return
            
        self.updateStatusBar("Creating New Case")

        # clear vtk renderer
        self.ren.RemoveAllViewProps()
        # clear the list widget
        self.listWidgetObjList.clear()
        self.project = ampersandProject(GUIMode=True,window=self)
        
        self.project.set_project_directory(ampersandPrimitives.ask_for_directory(qt=True))
        if self.project.project_directory_path == None:
            ampersandIO.printMessage("No project directory selected.",GUIMode=True,window=self)
            self.updateTerminal("Canceled creating new case")
            self.readyStatusBar()
            return
        project_name = ampersandIO.get_input("Enter the project name: ",GUIMode=True)
        if project_name == None:
            ampersandIO.printError("Project Name not entered",GUIMode=True)
            self.updateTerminal("Canceled creating new case")
            self.readyStatusBar()
            return
        self.project.set_project_name(project_name)
        
        self.project.create_project_path()
        ampersandIO.printMessage("Creating the project",GUIMode=True,window=self)
        ampersandIO.printMessage(f"Project path: {self.project.project_path}",GUIMode=True,window=self)
        self.project.create_project()
        self.project.create_settings()
        
        self.project.set_global_refinement_level()
        # Now enable the buttons
        self.enableButtons()
        self.readyStatusBar()
        self.project_opened = True
        ampersandIO.printMessage(f"Project {project_name} created",GUIMode=True,window=self)
        
        # change window title
        self.setWindowTitle(f"Case Creator: {project_name}")
        self.readyStatusBar()

    def openCase(self):
        if self.project_opened:
            # ask yes or no or cancel
            yNC = yesNoCancelDialogDriver("Save changes to current case files before creating a New Case","Save Changes")
            if yNC==1: # if yes
                # save the project
                self.project.add_stl_to_project()
                self.project.write_settings()
                self.disableButtons()
                self.ren.RemoveAllViewProps()
            elif yNC==-1: # if no
                # close the project
                self.project = None
                self.project_opened = False
                self.disableButtons()
                self.ren.RemoveAllViewProps()
            else: # if cancel
                self.readyStatusBar()
                return
        self.updateStatusBar("Opening Case")
        self.project = ampersandProject(GUIMode=True,window=self)

        # clear vtk renderer
        self.ren.RemoveAllViewProps()
        # clear the list widget
        self.listWidgetObjList.clear()
        projectFound = self.project.set_project_path(ampersandPrimitives.ask_for_directory(qt=True))
        
        if projectFound==-1:
            ampersandIO.printWarning("No project found. Failed to open case directory.",GUIMode=True)
            self.updateTerminal("No project found. Failed to open case directory.")
            
            self.readyStatusBar()
            return -1
        ampersandIO.printMessage(f"Project path: {self.project.project_path}",GUIMode=True,window=self)
        ampersandIO.printMessage("Loading the project",GUIMode=True,window=self)
        self.project.go_inside_directory()
        
        self.project.load_settings()
        self.project.check_0_directory()
        ampersandIO.printMessage("Project loaded successfully",GUIMode=True,window=self)
        self.project.summarize_project()
        self.enableButtons()
        self.autoDomain()
        self.update_list()
        stl_file_paths = self.project.list_stl_paths()
        for stl_file in stl_file_paths:
            self.showSTL(stlFile=stl_file)
        self.readyStatusBar()
        if self.project.internalFlow:
            self.radioButtonInternal.setChecked(True)
            self.checkBoxOnGround.setEnabled(False)
        else:
            self.radioButtonExternal.setChecked(True)
            self.checkBoxOnGround.setChecked(self.project.onGround)
        self.project_opened = True
        ampersandIO.printMessage(f"Project {self.project.project_name} created",GUIMode=True,window=self)
        self.setWindowTitle(f"Case Creator: {self.project.project_name}")
        # change window title
        self.setWindowTitle(f"Case Creator: {self.project.project_name}")
        self.readyStatusBar()

    def generateCase(self):
        self.updateStatusBar("Analyzing Case")
        #if(len(self.project.stl_files)>0):
        #    self.project.analyze_stl_file()
        self.updateStatusBar("Creating Project Files")
        self.project.useFOs = True
        self.project.set_post_process_settings()
        #project.list_stl_files()
        self.project.summarize_project()
        #project.analyze_stl_file()
    
        self.project.write_settings()
        self.project.create_project_files()
        self.updateTerminal("--------------------")
        self.updateTerminal("Case generated")
        self.updateTerminal("--------------------")
        self.readyStatusBar()

    def saveCase(self):
        self.updateStatusBar("Analyzing case before saving")
        #if(len(self.project.stl_files)>0):
        #    self.project.analyze_stl_file()
        self.updateStatusBar("Saving Case")
        self.updateTerminal("Saving Case")
        self.project.useFOs = True
        self.project.set_post_process_settings()
        self.project.write_settings()
        self.updateTerminal("--------------------")
        self.updateTerminal("Case saved")
        self.updateTerminal("--------------------")
        self.readyStatusBar()
    
    def autoDomain(self):
        
        #internalFlow = self.radioButtonInternal.isChecked()
        #self.project.meshSettings['internalFlow'] = internalFlow
        #self.project.internalFlow = internalFlow
        if self.project.internalFlow==True:
            onGround = False
        else:
            onGround = self.checkBoxOnGround.isChecked()
        self.project.meshSettings['onGround'] = onGround
        self.project.onGround = onGround
        if len(self.project.stl_files)==0:
            self.updateTerminal("No STL files loaded")
            self.readyStatusBar()
            return
        self.project.analyze_stl_file()
        #print("On Ground: ",onGround)
        minx = self.project.meshSettings['domain']['minx']
        miny = self.project.meshSettings['domain']['miny']
        minz = self.project.meshSettings['domain']['minz']
        maxx = self.project.meshSettings['domain']['maxx']
        maxy = self.project.meshSettings['domain']['maxy']
        maxz = self.project.meshSettings['domain']['maxz']
        nx = self.project.meshSettings['domain']['nx']
        ny = self.project.meshSettings['domain']['ny']
        nz = self.project.meshSettings['domain']['nz']
        self.lineEditMinX.setText(f"{minx:.2f}")
        self.lineEditMinY.setText(f"{miny:.2f}")
        self.lineEditMinZ.setText(f"{minz:.2f}")
        self.lineEditMaxX.setText(f"{maxx:.2f}")
        self.lineEditMaxY.setText(f"{maxy:.2f}")
        self.lineEditMaxZ.setText(f"{maxz:.2f}")
        self.lineEdit_nX.setText(str(nx))
        self.lineEdit_nY.setText(str(ny))
        self.lineEdit_nZ.setText(str(nz))
        self.add_box_to_VTK(minX=minx,minY=miny,minZ=minz,maxX=maxx,maxY=maxy,maxZ=maxz,boxName="Domain")
        
    def manualDomain(self):
        minx = float(self.lineEditMinX.text())
        miny = float(self.lineEditMinY.text())
        minz = float(self.lineEditMinZ.text())
        maxx = float(self.lineEditMaxX.text())
        maxy = float(self.lineEditMaxY.text())
        maxz = float(self.lineEditMaxZ.text())
        nx = int(self.lineEdit_nX.text())
        ny = int(self.lineEdit_nY.text())
        nz = int(self.lineEdit_nZ.text())
        if(nx<=0 or ny<=0 or nz<=0):
            ampersandIO.printError("Invalid Domain Size",GUIMode=True)
            self.readyStatusBar()
            return
        if(minx>maxx or miny>maxy or minz>maxz):
            ampersandIO.printError("Invalid Domain Size",GUIMode=True)
            self.readyStatusBar()
            return
        self.project.meshSettings['domain']['minx'] = minx
        self.project.meshSettings['domain']['miny'] = miny
        self.project.meshSettings['domain']['minz'] = minz
        self.project.meshSettings['domain']['maxx'] = maxx
        self.project.meshSettings['domain']['maxy'] = maxy
        self.project.meshSettings['domain']['maxz'] = maxz
        self.project.meshSettings['domain']['nx'] = nx
        self.project.meshSettings['domain']['ny'] = ny
        self.project.meshSettings['domain']['nz'] = nz
        self.updateStatusBar("Manual Domain Set")
        self.add_box_to_VTK(minX=minx,minY=miny,minZ=minz,maxX=maxx,maxY=maxy,maxZ=maxz,boxName="Domain")
        self.readyStatusBar()
        #print("Domain: ",minx,miny,minz,maxx,maxy,maxz,nx,ny,nz)

    def stlPropertiesDialog(self):
        stl = self.current_stl_file
        if stl==None:
            return
        currentStlProperties = self.project.get_stl_properties(stl)
        # open STL properties dialog
        stlProperties = STLDialogDriver(stl,stlProperties=currentStlProperties)
        # The properties are:
        #refMin,refMax,refLevel,nLayers,usage,edgeRefine,ami,None
        print(stlProperties)
        if stlProperties==None:
            return
        # update the properties
        status = self.project.set_stl_properties(stl,stlProperties)
        if status==-1:
            ampersandIO.printError("STL Properties not updated",GUIMode=True)   
        else:
            #self.updateStatusBar(f"{stl}: Properties Updated")
            self.updateTerminal(f"{stl} Properties Updated")
            self.readyStatusBar()

    def physicalPropertiesDialog(self):
        physicalProperties = physicalPropertiesDialogDriver()

    def boundaryConditionDialog(self):
        boundaryConditions = boundaryConditionDialogDriver()

    def numericsDialog(self):
        numerics = numericsDialogDriver()  

    def controlsDialog(self):
        controls = controlsDialogDriver()

    def vtkFitAll(self):
        print("Fitting all")
        self.ren.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()
        #self.ren.ResetCamera()
        #self.iren.Start()

    def vtkPlusX(self):
        print("Plus X side")
        self.ren.GetActiveCamera().SetPosition(1, 0, 0)
        self.ren.GetActiveCamera().SetFocalPoint(0, 0, 0)
        self.ren.GetActiveCamera().SetViewUp(0, 0, 1)
        self.ren.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()
    
    def vtkPlusY(self):
        print("Plus Y side")
        self.ren.GetActiveCamera().SetPosition(0, 1, 0)
        self.ren.GetActiveCamera().SetFocalPoint(0, 0, 0)
        self.ren.GetActiveCamera().SetViewUp(0, 0, 1)
        self.ren.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()

    def vtkPlusZ(self):
        print("Plus Z side")
        self.ren.GetActiveCamera().SetPosition(0, 0, 1)
        self.ren.GetActiveCamera().SetFocalPoint(0, 0, 0)
        self.ren.GetActiveCamera().SetViewUp(0, 1, 0)
        self.ren.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()
    
    def vtkMinusX(self):
        print("Minus X side")
        self.ren.GetActiveCamera().SetPosition(-1, 0, 0)
        self.ren.GetActiveCamera().SetFocalPoint(0, 0, 0)
        self.ren.GetActiveCamera().SetViewUp(0, 0, 1)
        self.ren.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()
    
    def vtkMinusY(self):
        print("Minus Y side")
        self.ren.GetActiveCamera().SetPosition(0, -1, 0)
        self.ren.GetActiveCamera().SetFocalPoint(0, 0, 0)
        self.ren.GetActiveCamera().SetViewUp(0, 0, 1)
        self.ren.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()

    def vtkMinusZ(self):
        print("Minus Z side")
        self.ren.GetActiveCamera().SetPosition(0, 0, -1)
        self.ren.GetActiveCamera().SetFocalPoint(0, 0, 0)
        self.ren.GetActiveCamera().SetViewUp(0, 1, 0)
        self.ren.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()

    def vtkShowWire(self):
        print("Show Wire")
        actors = self.ren.GetActors()
        for actor in actors:
            actor.GetProperty().SetRepresentationToWireframe()
        self.vtkWidget.GetRenderWindow().Render()
    
    def vtkShowSurface(self):
        print("Show Surface")
        actors = self.ren.GetActors()
        for actor in actors:
            actor.GetProperty().SetRepresentationToSurface()
        self.vtkWidget.GetRenderWindow().Render()

    def vtkShowEdges(self):
        print("Show Edges")
        actors = self.ren.GetActors()
        for actor in actors:
            actor.GetProperty().EdgeVisibilityOn()
        self.vtkWidget.GetRenderWindow().Render()


#-------------- End of Event Handlers -------------#


def main():

    app = QApplication(sys.argv)
    w = mainWindow()
    w.show()
    app.exec()

if __name__ == "__main__":
    main()
