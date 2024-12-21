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
from dialogBoxes import set_src, meshPointDialogDriver
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

#os.chdir(r"C:\Users\Ridwa\Desktop\CFD\01_CFD_Software_Development\ampersandCFD\src")
# get the absolute path of the current directory
src = os.path.dirname(os.path.abspath(__file__))

# set the source directory for the dialog boxes
set_src(src)

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
        self.lenX,self.lenY,self.lenZ = 1e-3,1e-3,1e-3
        self.current_stl_file = None
        self.colorCounter = 0
        self.listOfColors = ["Pink","Red","Green","Blue","Yellow","Orange","Purple","Cyan","Magenta","Brown",]
        # disable all the buttons and input fields
        self.disableButtons()

    def disableButtons(self):
        self.window.pushButtonSTLImport.setEnabled(False)
        self.window.pushButtonSphere.setEnabled(False)
        self.window.pushButtonBox.setEnabled(False)
        self.window.pushButtonCylinder.setEnabled(False)
        self.window.radioButtonInternal.setEnabled(False)
        self.window.radioButtonExternal.setEnabled(False)
        self.window.checkBoxOnGround.setEnabled(False)
        self.window.pushButtonSTLProperties.setEnabled(False)
        self.window.pushButtonPhysicalProperties.setEnabled(False)
        self.window.pushButtonBoundaryCondition.setEnabled(False)
        self.window.pushButtonNumerics.setEnabled(False)
        self.window.pushButtonControls.setEnabled(False)
        self.window.pushButtonDomainAuto.setEnabled(False)
        self.window.pushButtonDomainManual.setEnabled(False)
        self.window.pushButtonSteadyTransient.setEnabled(False)
        self.window.pushButtonSummarize.setEnabled(False)
        self.window.pushButtonFitAll.setEnabled(False)
        self.window.pushButtonPlusX.setEnabled(False)
        self.window.pushButtonPlusY.setEnabled(False)
        self.window.pushButtonPlusZ.setEnabled(False)
        self.window.pushButtonMinusX.setEnabled(False)
        self.window.pushButtonMinusY.setEnabled(False)
        self.window.pushButtonMinusZ.setEnabled(False)
        self.window.pushButtonShowWire.setEnabled(False)
        self.window.pushButtonShowSurface.setEnabled(False)
        self.window.pushButtonShowEdges.setEnabled(False)
        self.window.pushButtonAddSTL.setEnabled(False)
        self.window.pushButtonRemoveSTL.setEnabled(False)
        self.window.pushButtonMeshPoint.setEnabled(False)

        #self.window.pushButtonCreate.setEnabled(False)
        #self.window.pushButtonOpen.setEnabled(False)
        self.window.pushButtonGenerate.setEnabled(False)
        self.window.pushButtonSave.setEnabled(False)
        self.window.lineEditMinX.setEnabled(False)
        self.window.lineEditMinY.setEnabled(False)
        self.window.lineEditMinZ.setEnabled(False)
        self.window.lineEditMaxX.setEnabled(False)
        self.window.lineEditMaxY.setEnabled(False)
        self.window.lineEditMaxZ.setEnabled(False)
        self.window.lineEdit_nX.setEnabled(False)
        self.window.lineEdit_nY.setEnabled(False)
        self.window.lineEdit_nZ.setEnabled(False)
        # change color of widget 
        self.window.widget.setStyleSheet('''background-color: lightgrey;''')
        self.window.plainTextTerminal.appendPlainText("Welcome to SplashFOAM Case Creator")
       
    def enableButtons(self):
        self.window.pushButtonSTLImport.setEnabled(True)
        self.window.pushButtonSphere.setEnabled(True)
        self.window.pushButtonBox.setEnabled(True)
        self.window.pushButtonCylinder.setEnabled(True)
        self.window.radioButtonInternal.setEnabled(True)
        self.window.radioButtonExternal.setEnabled(True)
        self.window.checkBoxOnGround.setEnabled(True)
        self.window.pushButtonSTLProperties.setEnabled(True)
        self.window.pushButtonPhysicalProperties.setEnabled(True)
        self.window.pushButtonBoundaryCondition.setEnabled(True)
        self.window.pushButtonNumerics.setEnabled(True)
        self.window.pushButtonControls.setEnabled(True)
        self.window.pushButtonCreate.setEnabled(True)
        self.window.pushButtonOpen.setEnabled(True)
        self.window.pushButtonGenerate.setEnabled(True)
        self.window.pushButtonSave.setEnabled(True)
        self.window.pushButtonDomainAuto.setEnabled(True)
        self.window.pushButtonDomainManual.setEnabled(True)
        self.window.pushButtonSteadyTransient.setEnabled(True)
        self.window.pushButtonSummarize.setEnabled(True)
        self.window.pushButtonFitAll.setEnabled(True)
        self.window.pushButtonPlusX.setEnabled(True)
        self.window.pushButtonPlusY.setEnabled(True)
        self.window.pushButtonPlusZ.setEnabled(True)
        self.window.pushButtonMinusX.setEnabled(True)
        self.window.pushButtonMinusY.setEnabled(True)
        self.window.pushButtonMinusZ.setEnabled(True)
        self.window.pushButtonShowWire.setEnabled(True)
        self.window.pushButtonShowSurface.setEnabled(True)
        self.window.pushButtonShowEdges.setEnabled(True)
        self.window.pushButtonAddSTL.setEnabled(True)
        self.window.pushButtonRemoveSTL.setEnabled(True)
        self.window.pushButtonMeshPoint.setEnabled(True)


        self.window.lineEditMinX.setEnabled(True)
        self.window.lineEditMinY.setEnabled(True)
        self.window.lineEditMinZ.setEnabled(True)
        self.window.lineEditMaxX.setEnabled(True)
        self.window.lineEditMaxY.setEnabled(True)
        self.window.lineEditMaxZ.setEnabled(True)
        self.window.lineEdit_nX.setEnabled(True)
        self.window.lineEdit_nY.setEnabled(True)
        self.window.lineEdit_nZ.setEnabled(True)

    def load_ui(self):
        loader = QUiLoader()
        ui_path = os.path.join(src, "ampersandInputForm.ui")
        ui_file = QFile(ui_path)
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file, None)
        ui_file.close()
        self.setCentralWidget(self.window)
        self.setGeometry(100, 100, 1400, 880)
        self.setWindowTitle("Case Creator GUI")
        self.prepare_vtk()
        self.prepare_subWindows()
        self.prepare_events()

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
        self.vtkWidget = QVTKRenderWindowInteractor(self.window.widget)
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
            stl_name = os.path.basename(stlFile)
            print("STL Name: ",stl_name)
            self.render3D(actorName=stl_name)
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
        axes.SetTotalLength(0.1, 0.1, 0.1)
        self.ren.AddActor(axes)
        self.iren.Start()
      

    def render3D(self,actorName=None):  # self.ren and self.iren must be used. other variables are local variables
        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(self.reader.GetOutputPort())
        # Create an actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        if actorName:
            actor.SetObjectName(actorName)
            #print("Actor Name: ",actor.GetObjectName())
        #actor.GetProperty().EdgeVisibilityOn()
        # set random colors to the actor
        colors = vtk.vtkNamedColors()
        
        if(self.colorCounter>9):
            self.colorCounter = 0
        actor.GetProperty().SetColor(colors.GetColor3d(self.listOfColors[self.colorCounter]))
        self.ren.AddActor(actor)
        axes = vtk.vtkAxesActor()
        #self.project.update_max_lengths()
        #charLen = min(self.project.lenX,self.project.lenY,self.project.lenZ)*0.5
        #maxLen = max(self.project.lenX,self.project.lenY,self.project.lenZ)
        #charLen = max(charLen,maxLen*0.2,0.01)
        axes.SetTotalLength(0.2, 0.2, 0.2)
        self.ren.AddActor(axes)
        
        self.colorCounter += 1
        
        #self.iren.Start()

    def add_object_to_VTK(self,object,objectName="sphere",opacity=0.5,removePrevious=False,color=(0.5,0.5,0.5)):
        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(object.GetOutputPort())
        
        # Create an actor
        actor = vtk.vtkActor()
        actor.GetProperty().SetOpacity(opacity)
        if color:
            actor.GetProperty().SetColor(color)
        else:
            actor.GetProperty().SetColor(0.5,0.5,0.5)
        actor.GetProperty().SetObjectName(objectName)
        actor.GetProperty().EdgeVisibilityOn()
        actor.SetMapper(mapper)
        # remove the previous object
        if(removePrevious):
            currentActors = self.ren.GetActors()
            for act in currentActors:
                if(act.GetProperty().GetObjectName()==objectName):
                    print("Removing previous object: ",objectName)
                    self.ren.RemoveActor(act)
        self.ren.AddActor(actor)
        self.iren.Start()

    def add_sphere_to_VTK(self,center=(0.0,0.0,0.0),radius=1.0,objectName="sphere",removePrevious=True):
        # Create a sphere
        sphere = vtk.vtkSphereSource()
        sphere.SetCenter(center)
        sphere.SetRadius(radius)
        self.add_object_to_VTK(sphere,objectName=objectName,removePrevious=removePrevious)
       

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
        self.window.listWidgetObjList.insertItem(idx,stl_name)
        message = "Loaded STL file: "+stlFile
        self.updateStatusBar(message) 

    def update_list(self):
        self.window.listWidgetObjList.clear()
        for i in range(len(self.project.stl_files)):
            self.window.listWidgetObjList.insertItem(i,self.project.stl_files[i]['name'])

    def listClicked(self):
        # find the selected item in the list
        item = self.window.listWidgetObjList.currentItem()
        idx = self.window.listWidgetObjList.row(item)
        
        self.current_stl_file = item.text()
        #print("Selected Item: ",self.current_stl_file)
        #actors = self.ren.GetActors()
        self.vtkHilightSTL(self.current_stl_file)
        
        stl_properties = self.project.get_stl_properties(self.current_stl_file)
        if stl_properties==None:
            return
        purpose,refMin,refMax,featureEdges,featureLevel,nLayers,property,bounds = stl_properties
        #print("STL Properties: ",refMin,refMax,featureEdges,featureLevel,nLayers,property,bounds)
        return
        # update the property box
        self.window.tableViewProperties.setItem(0,0,QtWidgets.QTableWidgetItem("Refinement Min"))
        #self.window.tableViewProperties.setItem(0,0,QtWidgets.QTableWidgetItem(str(refMin)))
        self.window.tableViewProperties.setItem(0,1,QtWidgets.QTableWidgetItem(str(refMax)))
        self.window.tableViewProperties.setItem(1,0,QtWidgets.QTableWidgetItem(str(featureEdges)))
        self.window.tableViewProperties.setItem(1,1,QtWidgets.QTableWidgetItem(str(featureLevel)))
        self.window.tableViewProperties.setItem(2,0,QtWidgets.QTableWidgetItem(str(nLayers)))
        self.window.tableViewProperties.setItem(2,1,QtWidgets.QTableWidgetItem(str(property)))
        self.window.tableViewProperties.setItem(3,0,QtWidgets.QTableWidgetItem(str(bounds[0])))
        
    def updateStatusBar(self,message="Go!"):
        self.window.statusbar.showMessage(message)
        #self.window.plainTextTerminal.appendPlainText(message)
        self.window.plainTextTerminal.insertPlainText(message+"\n")

    def updateTerminal(self,message="Go!"):
        self.window.plainTextTerminal.insertPlainText(message+"\n")
        #self.window.plainTextTerminal.appendPlainText(message)
       
        self.window.plainTextTerminal.verticalScrollBar().setValue(self.window.plainTextTerminal.verticalScrollBar().maximum())
        
    def readyStatusBar(self):
        # pause 1 millisecond
        sleep(0.001)
        self.window.statusbar.showMessage("Ready")

    def prepare_events(self):
        #self.window.resizeEvent = self.resizeEventTriggered
        #self.window.closeEvent = self.closeEventTriggered
        # Initiate the button click maps
        self.window.pushButtonSTLImport.clicked.connect(self.importSTL)
        self.window.pushButtonSphere.clicked.connect(self.createSphere)
        self.window.actionNew_Case.triggered.connect(self.createCase)
        self.window.actionOpen_Case.triggered.connect(self.openCase)
        self.window.actionSave_Case.triggered.connect(self.saveCase)
        self.window.pushButtonCreate.clicked.connect(self.createCase)
        self.window.pushButtonOpen.clicked.connect(self.openCase)
        self.window.actionExit.triggered.connect(self.close)
        self.window.pushButtonGenerate.clicked.connect(self.generateCase)
        self.window.pushButtonSave.clicked.connect(self.saveCase)
        self.window.radioButtonInternal.clicked.connect(self.chooseInternalFlow)
        self.window.radioButtonExternal.clicked.connect(self.chooseExternalFlow)
        self.window.listWidgetObjList.itemClicked.connect(self.listClicked)
        self.window.pushButtonDomainAuto.clicked.connect(self.autoDomainDriver)
        self.window.pushButtonDomainManual.clicked.connect(self.manualDomain)
        self.window.pushButtonSTLProperties.clicked.connect(self.stlPropertiesDialog)
        self.window.pushButtonPhysicalProperties.clicked.connect(self.physicalPropertiesDialog)
        self.window.pushButtonBoundaryCondition.clicked.connect(self.boundaryConditionDialog)
        self.window.pushButtonNumerics.clicked.connect(self.numericsDialog)
        self.window.pushButtonControls.clicked.connect(self.controlsDialog)
        self.window.pushButtonSteadyTransient.clicked.connect(self.toggleSteadyTransient)
        self.window.pushButtonSummarize.clicked.connect(self.summarizeProject)
        self.window.pushButtonAddSTL.clicked.connect(self.importSTL)
        self.window.pushButtonRemoveSTL.clicked.connect(self.removeSTL)
        self.window.pushButtonMeshPoint.clicked.connect(self.setMeshPoint)
        #self.window.checkBoxOnGround.clicked.connect(self.chooseExternalFlow)
        # change view on the VTK widget
        self.window.pushButtonFitAll.clicked.connect(self.vtkFitAll)
        self.window.pushButtonPlusX.clicked.connect(self.vtkPlusX)
        self.window.pushButtonPlusY.clicked.connect(self.vtkPlusY)
        self.window.pushButtonPlusZ.clicked.connect(self.vtkPlusZ)
        self.window.pushButtonMinusX.clicked.connect(self.vtkMinusX)
        self.window.pushButtonMinusY.clicked.connect(self.vtkMinusY)
        self.window.pushButtonMinusZ.clicked.connect(self.vtkMinusZ)
        self.window.pushButtonShowWire.clicked.connect(self.vtkShowWire)
        self.window.pushButtonShowSurface.clicked.connect(self.vtkShowSurface)
        self.window.pushButtonShowEdges.clicked.connect(self.vtkShowEdges)
        

        #self.window.resizeEvent = self.resizeEvent
        self.window.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        self.window.resizeEvent = self.resizeEvent
        self.window.widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        #self.window.closeEvent = self.closeEvent
        self.window.statusbar.showMessage("Ready")

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
        #self.showSTL(stlFile=self.project.current_stl_file)
        stl_file_paths = self.project.list_stl_paths()
        for stl_file in stl_file_paths:
            self.showSTL(stlFile=stl_file)
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

    def removeSTL(self):
        # show warning message box
        
        item = self.window.listWidgetObjList.currentItem()
        if item==None or item.text()=="":
            return
        idx = self.window.listWidgetObjList.row(item)
        stl = item.text()
        self.project.remove_stl_file_by_name(stl)
        self.update_list()
        self.readyStatusBar()

    def createSphere(self):
       
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
        
        terminalHeight = 302
        vtkWidgetWidth = self.window.width()-560
        vtkWidgetHeight = self.window.height()-terminalHeight-20
        terminalX = self.window.widget.pos().x()
        terminalY = self.window.widget.pos().y()+vtkWidgetHeight+10
        terminalWidth = vtkWidgetWidth
        
        self.window.widget.resize(vtkWidgetWidth,vtkWidgetHeight)
        self.vtkWidget.resize(vtkWidgetWidth,vtkWidgetHeight)
        self.vtkWidget.GetRenderWindow().Render()
        self.window.plainTextTerminal.resize(self.window.width()-560,self.window.plainTextTerminal.height())
       
        self.window.plainTextTerminal.move(terminalX,terminalY)
        self.window.plainTextTerminal.resize(terminalWidth,terminalHeight-20)
        self.window.plainTextTerminal.update()
        self.window.plainTextTerminal.repaint()
        self.readyStatusBar()


    def closeEventTriggered(self, event):
        
        self.close()

    def toggleSteadyTransient(self):
        buttonText = self.window.pushButtonSteadyTransient.text()
        if buttonText=="Steady-State":
            self.window.pushButtonSteadyTransient.setText("Transient")
            ampersandIO.printMessage("Transient Flow Selected",GUIMode=True,window=self)
            self.project.transient = True
        else:
            self.window.pushButtonSteadyTransient.setText("Steady-State")
            ampersandIO.printMessage("Steady-State Flow Selected",GUIMode=True,window=self)
            self.project.transient = False
        self.project.set_transient_settings()
        self.readyStatusBar()

    def chooseInternalFlow(self):
        
        self.project.internalFlow = True
        self.project.meshSettings['internalFlow'] = True
        self.project.onGround = False
        self.window.checkBoxOnGround.setEnabled(False)
        self.updateStatusBar("Choosing Internal Flow")
        #sleep(0.001)
        self.readyStatusBar()

    def chooseExternalFlow(self):
        self.project.internalFlow = False
        self.project.meshSettings['internalFlow'] = False
        self.window.checkBoxOnGround.setEnabled(True)
        self.project.meshSettings['onGround'] = self.window.checkBoxOnGround.isChecked()
        self.project.onGround = self.window.checkBoxOnGround.isChecked()
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
        # clear terminal
        self.window.plainTextTerminal.clear()
        # clear vtk renderer
        self.ren.RemoveAllViewProps()
        # clear the list widget
        self.window.listWidgetObjList.clear()
        self.project = None # clear the project
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
        # clear terminal
        self.window.plainTextTerminal.clear()
        # clear the case
        self.project = None
        self.project = ampersandProject(GUIMode=True,window=self)

        # clear vtk renderer
        self.ren.RemoveAllViewProps()
        # clear the list widget
        self.window.listWidgetObjList.clear()
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
        self.autoDomain(analyze=False)
        #self.vtkUpdateAxes()
        self.update_list()
        stl_file_paths = self.project.list_stl_paths()
        for stl_file in stl_file_paths:
            self.showSTL(stlFile=stl_file)
        self.readyStatusBar()
        if self.project.internalFlow:
            self.window.radioButtonInternal.setChecked(True)
            self.window.checkBoxOnGround.setEnabled(False)
        else:
            self.window.radioButtonExternal.setChecked(True)
            self.window.checkBoxOnGround.setChecked(self.project.onGround)
        self.project_opened = True
        ampersandIO.printMessage(f"Project {self.project.project_name} created",GUIMode=True,window=self)
        self.setWindowTitle(f"Case Creator: {self.project.project_name}")
        self.vtkDrawMeshPoint()
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

    def autoDomainDriver(self):
        self.analyze = True
        self.autoDomain(self.analyze)
    
    def autoDomain(self,analyze=True):
       
        if self.project.internalFlow==True:
            onGround = False
        else:
            onGround = self.window.checkBoxOnGround.isChecked()
        self.project.meshSettings['onGround'] = onGround
        self.project.onGround = onGround
        if len(self.project.stl_files)==0:
            self.updateTerminal("No STL files loaded")
            self.readyStatusBar()
            return
        if analyze:
            self.project.analyze_stl_file()
        
        minx = self.project.meshSettings['domain']['minx']
        miny = self.project.meshSettings['domain']['miny']
        minz = self.project.meshSettings['domain']['minz']
        maxx = self.project.meshSettings['domain']['maxx']
        maxy = self.project.meshSettings['domain']['maxy']
        maxz = self.project.meshSettings['domain']['maxz']
        nx = self.project.meshSettings['domain']['nx']
        ny = self.project.meshSettings['domain']['ny']
        nz = self.project.meshSettings['domain']['nz']
       
        self.window.lineEditMinX.setText(f"{minx:.2f}")
        self.window.lineEditMinY.setText(f"{miny:.2f}")
        self.window.lineEditMinZ.setText(f"{minz:.2f}")
        self.window.lineEditMaxX.setText(f"{maxx:.2f}")
        self.window.lineEditMaxY.setText(f"{maxy:.2f}")
        self.window.lineEditMaxZ.setText(f"{maxz:.2f}")
        self.window.lineEdit_nX.setText(str(nx))
        self.window.lineEdit_nY.setText(str(ny))
        self.window.lineEdit_nZ.setText(str(nz))
        self.add_box_to_VTK(minX=minx,minY=miny,minZ=minz,maxX=maxx,maxY=maxy,maxZ=maxz,boxName="Domain")
        
        
        self.vtkDrawMeshPoint()
        self.readyStatusBar()
        
    def manualDomain(self):
        minx = float(self.window.lineEditMinX.text())
        miny = float(self.window.lineEditMinY.text())
        minz = float(self.window.lineEditMinZ.text())
        maxx = float(self.window.lineEditMaxX.text())
        maxy = float(self.window.lineEditMaxY.text())
        maxz = float(self.window.lineEditMaxZ.text())
        nx = int(self.window.lineEdit_nX.text())
        ny = int(self.window.lineEdit_nY.text())
        nz = int(self.window.lineEdit_nZ.text())
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
        

    def stlPropertiesDialog(self):
        stl = self.current_stl_file
        if stl==None:
            return
        currentStlProperties = self.project.get_stl_properties(stl)
        
        # open STL properties dialog
        stlProperties = STLDialogDriver(stl,stlProperties=currentStlProperties)
        # The properties are:
       
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

        # assign initial values from read data
        rho = self.project.physicalProperties['rho']
        nu = self.project.physicalProperties['nu']
        cp = self.project.physicalProperties['Cp']
        turbulence_model = self.project.physicalProperties['turbulenceModel']
        fluid = self.project.physicalProperties['fluid']
        initialProperties = (fluid,rho,nu,cp,turbulence_model)
        
        physicalProperties = physicalPropertiesDialogDriver(initialProperties)
        fluid,rho,nu,cp,turbulence_model = physicalProperties
        # update the project physical properties
        ampersandIO.printMessage("Updating Physical Properties",GUIMode=True)
        ampersandIO.printMessage(f"Updated Properties: {physicalProperties}",GUIMode=True,window=self)
        self.project.physicalProperties['fluid'] = fluid
        self.project.physicalProperties['rho'] = rho
        self.project.physicalProperties['nu'] = nu
        self.project.physicalProperties['Cp'] = cp
        self.project.physicalProperties['turbulenceModel'] = turbulence_model

    def boundaryConditionDialog(self):
        stl = self.project.get_stl(self.current_stl_file)
        if stl==None:
            ampersandIO.printError("STL not found",GUIMode=True)
            return
        
        boundaryConditions = boundaryConditionDialogDriver(stl)
        if boundaryConditions==None:
            return
        # update the boundary conditions
        self.project.set_boundary_condition(self.current_stl_file,boundaryConditions)

    def numericsDialog(self):
        numerics = numericsDialogDriver()  

    def controlsDialog(self):
        controls = controlsDialogDriver()

    def summarizeProject(self):
        self.project.summarize_project()
        self.readyStatusBar()

    def setMeshPoint(self):
        # open the mesh point dialog
        meshPoint = meshPointDialogDriver(self.project.get_location_in_mesh())
        ampersandIO.printMessage("Mesh Point: ",meshPoint,GUIMode=True,window=self)
        if meshPoint==None:
            return
        
        self.project.set_location_in_mesh(meshPoint)
        self.vtkDrawMeshPoint()

# VTK Event Handlers
#----------------- VTK Event Handlers -----------------#
    def vtkFitAll(self):
       
        self.ren.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()
        #self.ren.ResetCamera()
        #self.iren.Start()

    def vtkPlusX(self):
       
        self.ren.GetActiveCamera().SetPosition(1, 0, 0)
        self.ren.GetActiveCamera().SetFocalPoint(0, 0, 0)
        self.ren.GetActiveCamera().SetViewUp(0, 0, 1)
        self.ren.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()
    
    def vtkPlusY(self):
        
        self.ren.GetActiveCamera().SetPosition(0, 1, 0)
        self.ren.GetActiveCamera().SetFocalPoint(0, 0, 0)
        self.ren.GetActiveCamera().SetViewUp(0, 0, 1)
        self.ren.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()

    def vtkPlusZ(self):
        
        self.ren.GetActiveCamera().SetPosition(0, 0, 1)
        self.ren.GetActiveCamera().SetFocalPoint(0, 0, 0)
        self.ren.GetActiveCamera().SetViewUp(0, 1, 0)
        self.ren.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()
    
    def vtkMinusX(self):
        #print("Minus X side")
        self.ren.GetActiveCamera().SetPosition(-1, 0, 0)
        self.ren.GetActiveCamera().SetFocalPoint(0, 0, 0)
        self.ren.GetActiveCamera().SetViewUp(0, 0, 1)
        self.ren.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()
    
    def vtkMinusY(self):
        #print("Minus Y side")
        self.ren.GetActiveCamera().SetPosition(0, -1, 0)
        self.ren.GetActiveCamera().SetFocalPoint(0, 0, 0)
        self.ren.GetActiveCamera().SetViewUp(0, 0, 1)
        self.ren.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()

    def vtkMinusZ(self):
        #print("Minus Z side")
        self.ren.GetActiveCamera().SetPosition(0, 0, -1)
        self.ren.GetActiveCamera().SetFocalPoint(0, 0, 0)
        self.ren.GetActiveCamera().SetViewUp(0, 1, 0)
        self.ren.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()

    def vtkShowWire(self):
        #print("Show Wire")
        actors = self.ren.GetActors()
        for actor in actors:
            actor.GetProperty().SetRepresentationToWireframe()
        self.vtkWidget.GetRenderWindow().Render()
    
    def vtkShowSurface(self):
        #print("Show Surface")
        actors = self.ren.GetActors()
        for actor in actors:
            actor.GetProperty().SetRepresentationToSurface()
            actor.GetProperty().EdgeVisibilityOff()
        self.vtkWidget.GetRenderWindow().Render()

    def vtkShowEdges(self):
        #print("Show Edges")
        actors = self.ren.GetActors()
        for actor in actors:
            actor.GetProperty().SetRepresentationToSurface()
            actor.GetProperty().EdgeVisibilityOn()
        self.vtkWidget.GetRenderWindow().Render()

    def vtkHilightSTL(self,stlFile):
        idx = 0
        actors = self.ren.GetActors()
        
        colors = vtk.vtkNamedColors()
        actor_found = None
        stl_names = [] #self.project.stl_files
        for stl in self.project.stl_files:
            stl_names.append(stl['name'])
        for actor in actors:
            #print("Actor Name: ",actor.GetObjectName())
            #print("STL File: ",stlFile)
            
            if actor.GetObjectName() in stl_names:  
                if actor.GetObjectName() == stlFile:
                    #print("Actor Found: ",actor.GetObjectName())
                    actor_found = actor
                    actor_found.GetProperty().SetColor(1.0, 0.0, 1.0)
                else:
                    # reset colors for other colors
                    actor.GetProperty().SetColor(colors.GetColor3d(self.listOfColors[idx]))
                idx += 1
        self.vtkWidget.GetRenderWindow().Render()


    def vtkUpdateAxes(self):
        axes = vtk.vtkAxesActor()
        self.project.update_max_lengths()
        charLen = min(self.project.lenX,self.project.lenY,self.project.lenZ)*0.5
        maxLen = max(self.project.lenX,self.project.lenY,self.project.lenZ)
        charLen = max(charLen,maxLen*0.2,0.01)
        axes.SetTotalLength(charLen, charLen, charLen)
        self.ren.AddActor(axes)
        self.vtkWidget.GetRenderWindow().Render()

    def vtkDrawMeshPoint(self):
        # estimate size of the mesh point
        lx,ly,lz = self.project.lenX,self.project.lenY,self.project.lenZ
        maxLen = max(lx,ly,lz,0.02)
        locationInMesh = tuple(self.project.get_location_in_mesh())

        print("Location in Mesh: ",locationInMesh)
        print("Drawing Mesh Point")
        self.add_sphere_to_VTK(center=locationInMesh,radius=0.02*maxLen,objectName="MeshPoint",removePrevious=True)

#----------------- End of VTK Event Handlers -----------------#

#-------------- End of Event Handlers -------------#


def main():

    app = QApplication(sys.argv)
    w = mainWindow()
    w.show()
    app.exec()

if __name__ == "__main__":
    main()
