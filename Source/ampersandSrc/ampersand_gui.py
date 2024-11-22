from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QMainWindow
from PySide6 import QtWidgets
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
import sys
from time import sleep

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



class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_ui()
        self.surfaces = []
    
    def load_ui(self):
        ui_file = QFile("ampersandInputForm.ui")
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file, None)
        ui_file.close()
        self.setWindowTitle("Ampersand Input Form")
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
            print("Current CAD File: ",fname)
            return fname
        
    def openSTLDialog(self):
        fname,ftype = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 
        'c:\\',"STL files (*.stl *.obj)")
        if(fname==""):
            return -1 # STL file not loaded
        else:
            #print("Current STL File: ",fname)
            return fname

    def openSTL(self):
        stlFileName = self.openSTLDialog()
        if(stlFileName==-1):
            pass
        else:
            #print("Copying stl file")
            stl = stlFileName #self.copySTL(stlFileName=stlFileName)
            if(stl!=-1):
                self.showSTL(stlFile=stl)
                self.loadSTL(stlFile=stl)

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
        self.ren.SetBackground(0, 0, 0)
        #self.ren.SetBackground(0.1, 0.2, 0.4)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

    # this function will read STL file and show it in the VTK renderer
    def showSTL(self,stlFile=r"C:\Users\mrtha\Desktop\GitHub\foamAutoGUI\src\pipe.stl"):
        # Read stl
        try:
            self.reader = vtk.vtkSTLReader()
            self.reader.SetFileName(stlFile)
            self.render3D()
        except:
            print("Reading STL not successful. Try again")

    def render3D(self):  # self.ren and self.iren must be used. other variables are local variables
        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(self.reader.GetOutputPort())
        # Create an actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().EdgeVisibilityOn()
        colors = vtk.vtkNamedColors()
        self.ren.SetBackground(colors.GetColor3d("SlateGray"))
        self.ren.AddActor(actor)
        style = vtk.vtkInteractorStyleTrackballCamera()
        self.iren.SetInteractorStyle(style)
        camera = vtk.vtkCamera()
        camera.SetPosition(0, 1, 0)
        camera.SetFocalPoint(0, 0, 0)
        camera.SetViewUp(0, 0, 1)
        camera.Azimuth(30)
        camera.Elevation(30)
        self.ren.SetActiveCamera(camera)
        self.ren.ResetCamera()
        self.ren.ResetCameraClippingRange()
        # add coordinate axes
        axes = vtk.vtkAxesActor()
        self.ren.AddActor(axes)
        self.ren.SetBackground(0.1, 0.2, 0.4)

        #renWin.Render()
        self.iren.Start()

    def loadSTL(self,stlFile = r"C:\Users\mrtha\Desktop\GitHub\foamAutoGUI\src\pipe.stl"):
        self.updateStatusBar("Loading STL file")
        #stlFile = r"C:\Users\mrtha\Desktop\GitHub\foamAutoGUI\src\pipe.stl"
        #surfaces = readSTL(stlFileName=stlFile)
        
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

    
    def updateStatusBar(self,message="Go!"):
        self.window.statusbar.showMessage(message)
        self.window.plainTextTerminal.appendPlainText(message)

    def readyStatusBar(self):
        # pause 1 millisecond
        sleep(0.001)
        self.window.statusbar.showMessage("Ready")

    def prepare_events(self):
        # Initiate the button click maps
        self.window.pushButtonSTLImport.clicked.connect(self.importSTL)
        self.window.pushButtonSphere.clicked.connect(self.createSphere)

        self.window.statusbar.showMessage("Ready")

#----------------- Event Handlers -----------------#
    def importSTL(self):
        print("Open STL")
        self.updateStatusBar("Opening STL")
        self.openSTL()
    
    def createSphere(self):
        print("Create Sphere")
        self.updateStatusBar("Creating Sphere")
    
    def chooseInternalFlow(self):
        print("Choose Internal Flow")
        self.updateStatusBar("Choosing Internal Flow")
#-------------- End of Event Handlers -------------#


def main():

    app = QApplication(sys.argv)
    w = mainWindow()
    w.window.show()
    app.exec()

if __name__ == "__main__":
    main()
