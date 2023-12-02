import tkinter as tk 
import tkinter.simpledialog  # Import simpledialog for user input
from tkinter.simpledialog import askstring
from tkinter import ttk, filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import subprocess
import os
import re 
import signal
import time  # Add this import for demonstration purposes
import shutil  # For file copying
import threading  # Import threading for running simulation in a separate thread
import matplotlib.pyplot as plt
from tkinter import Listbox


class ReplacePropertiesPopup:
    def __init__(self, parent, thermo_type_params, mixture_params, old_values_thermo_type, old_values_mixture):
        self.parent = parent
        self.thermo_type_params = thermo_type_params
        self.mixture_params = mixture_params
        self.old_values_thermo_type = old_values_thermo_type
        self.old_values_mixture = old_values_mixture
        self.new_values_mixture = {}  

        self.popup = tk.Toplevel(parent.root)
        self.popup.title("Update Physical Properties")
        self.popup.geometry("520x650")  # Set the size of the popup window

        # Create a label for the "thermoType" group
        thermo_type_label = ttk.Label(self.popup, text="thermoType", font=("TkDefaultFont", 15, "bold"), foreground="red")
        thermo_type_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        # Show old values of the thermoType block as labels
        row_counter = 1
        for param in thermo_type_params:
            ttk.Label(self.popup, text=f"{param}").grid(row=row_counter, column=1, sticky="w", padx=30, pady=2)
            label = ttk.Label(self.popup, text=str(old_values_thermo_type.get(param, "")), foreground="blue")
            label.grid(row=row_counter, column=2, pady=2)
            row_counter += 1

        # Create a label for the "mixture" group
        mixture_label = ttk.Label(self.popup, text="mixture", font=("TkDefaultFont", 15, "bold"), foreground="red")
        mixture_label.grid(row=row_counter, column=0, sticky="w", padx=10, pady=10)
        row_counter += 1

        # Create entry fields for each parameter in the "mixture" group
        for param in mixture_params:
            ttk.Label(self.popup, text=f"{param}").grid(row=row_counter, column=1, sticky="w", padx=30, pady=2)
            entry = ttk.Entry(self.popup)
            entry.insert(0, str(old_values_mixture.get(param, "")))  # Pre-fill with old values if available
            entry.config(font=("TkDefaultFont", 9, "bold"), foreground="blue")
            entry.grid(row=row_counter, column=2, pady=2)
            self.new_values_mixture[param] = entry
            row_counter += 1
            row_counter_plus = row_counter + 1 

        # Create an "Update" button that calls the replace_values method for the mixture block
        style = ttk.Style()
        
        #style.configure("TButton", padding=10, relief="flat", background="#3EAAAF", foreground="black")
        style.configure("TButton", padding=10, relief="flat", background="lightblue", foreground="black")
        updateButton = ttk.Button(self.popup, text="Update", command=self.replace_mixture_values).grid(row=row_counter,         column=2, pady=10, padx=10)
        addButton = ttk.Button(self.popup, text="Add parameter", command=self.add_missing_parameters).grid(row=row_counter_plus, column=2, pady=10, padx=10)

        
    def replace_mixture_values(self):
        file_content = self.parent.selected_file_content

        # Define the lines to be preserved
        foamfile_start = 'FoamFile\n{'
        foamfile_end = '}'

        # Extract the FoamFile block content
        foamfile_content = re.search(f'{foamfile_start}(.*?){foamfile_end}', file_content, re.DOTALL).group()

        # Split the file content into header, FoamFile, and body
        foamfile_end_position = file_content.find(foamfile_end, file_content.find(foamfile_start)) + len(foamfile_end)
        foamfile_content = file_content[file_content.find(foamfile_start):foamfile_end_position]
        body_content = file_content[foamfile_end_position:]

        # Replace old values with new ones in the body content for the mixture block
        for param, entry in self.new_values_mixture.items():
            value = entry.get()
            if value != "":
                old_pattern = f'{param}\\s*([^;]+)'
                new_pattern = f'{param} {value}'
                body_content = re.sub(old_pattern, new_pattern, body_content)

        # Combine the header, FoamFile, and updated body content
        file_content = f'{self.parent.header}{foamfile_content}{body_content}'
        
        # Show a confirmation popup
        confirmation = tk.messagebox.askyesno("Confirmation", "Are you sure you want to update the file?")
        if confirmation:
            # Write the updated content to the file
            with open(self.parent.selected_file_path, 'w') as file:
                file.write(file_content)

            self.parent.status_label.config(text="Values replaced successfully", foreground="green")
            tk.messagebox.showinfo("Update", "Mixture block updated successfully.")
            self.popup.destroy()
        else:
            tk.messagebox.showinfo("Update Canceled", "No changes were made.")
            
    def add_missing_parameters(self):
        added_values = {}
        for prop in self.mixture_params:
            value = simpledialog.askstring("Add Missing Parameter", f"Enter value for {prop}:")
            if value is not None:
                added_values[prop] = value

        if added_values:
            file_content = self.selected_file_content
            for prop, value in added_values.items():
                file_content += f'\n{prop} {value};'

            with open(self.selected_file_path, 'a') as file:
                file.write(file_content)

            self.status_label.config(text="Parameters added successfully", foreground="green")

#__________________
#
# TERMINAL APP 
#__________________           
class TerminalApp:  
    def __init__(self, root):
        self.root = root
        self.root.config(background="white") # black
        self.root.title("Splash - OpenFOAM")
        
        # Display a welcome message
        self.show_welcome_message()
        
        #  Source OpenFOAM Libraries
        #self.source_openfoam_libraries()
        
        # Add logos
        self.add_logos()

        # Create a button to import a geometry
        style = ttk.Style()
        style.configure("TButton", padding=10, relief="flat", background="lightblue", foreground="black")
        self.import_button = ttk.Button(self.root, text="Import Geometry", command=self.import_geometry)
        self.import_button.grid(row=0, column=2, pady=10, padx=10)
        
        # Create a button to open a directory dialog
        style = ttk.Style()
        style.configure("TButton", padding=10, relief="flat", background="cyan", foreground="black")
        self.browse_button = ttk.Button(self.root, text="Physical Properties", command=self.browse_directory)
        self.browse_button.grid(row=1, column=2, pady=10, padx=10, sticky="ew")
        self.geometry_loaded = False
        
        # Create a mesh type variable
        self.mesh_type_var = tk.StringVar(value="Cartesian")
        # Create a button to create the mesh
        style = ttk.Style()
        style.configure("TButton", padding=10, relief="flat", background="cyan", foreground="black")
        self.create_mesh_button = ttk.Button(self.root, text="Create Mesh", command=self.create_mesh)
        self.create_mesh_button.grid(row=2, column=2, pady=10, padx=10)
        
        # Create a button to initialize the case directory
        style = ttk.Style()
        style.configure("TButton", padding=10, relief="flat", background="cyan", foreground="black")
        self.initialize_case_button = ttk.Button(self.root, text="Initialize Case", command=self.initialize_case)
        self.initialize_case_button.grid(row=3, column=2, pady=10, padx=10, sticky="ew")
        
        # Create a button to run simulation
        style = ttk.Style()
        style.configure("TButton", padding=10, relief="flat", background="cyan", foreground="black")
        #self.run_simulation_button = ttk.Button(self.root, text="Run Simulation", command=self.run_openfoam_simulation)
        self.run_simulation_button = ttk.Button(self.root, text="Run Simulation", command=self.run_simulation)
        self.run_simulation_button.grid(row=4, column=2, pady=10, padx=10, sticky="ew")
        
        # Stop Simulation Button
        style = ttk.Style()
        style.configure("TButton", padding=10, relief="flat", background="cyan", foreground="black")
        #style.configure("TButton", padding=10, relief="flat", background="lightblue", foreground="black")
        self.stop_simulation_button = ttk.Button(self.root, text="Stop Simulation", command=self.stop_simulation)
        self.stop_simulation_button.grid(row=5, column=2, pady=10, padx=10, sticky="ew")
        #self.stop_simulation_button["state"] = tk.DISABLED  # Initially disable the button
        
        # Create a canvas for the custom progress bar
        self.progress_bar_canvas = tk.Canvas(self.root, width=200, height=20, background="white", bd=0, highlightthickness=0)
        self.progress_bar_canvas.grid(row=6, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

        # Initialize variables for simulation thread
        self.simulation_thread = None
        self.simulation_running = False
        
        # Initialize the available fuels to choose from
        self.fuels = ["Methanol", "Ammonia", "Dodecane"]
        
        # Create a label for the "Fuel Selector" dropdown
        self.fuel_selector_label = ttk.Label(self.root, text="Fuel Options ▼", font=("TkDefaultFont", 12), background="cyan") # , foreground="green")
        self.fuel_selector_label.grid(row=1, column=0, pady=10, padx=10, sticky="w")

        # Define the fuel options
        fuels = ["Methanol", "Ammonia", "Dodecane"]

        # Create a StringVar to store the selected fuel
        self.selected_fuel = tk.StringVar()

        # Set a default value for the dropdown
        default_value = "Methanol"
        self.selected_fuel.set(default_value)

        # Create a dropdown menu for fuel selection
        self.fuel_selector = ttk.Combobox(self.root, textvariable=self.selected_fuel, values=fuels)
        self.fuel_selector.grid(row=2, column=0, pady=10, padx=10, sticky="w")

        # Bind an event handler to the <<ComboboxSelected>> event
        self.fuel_selector.bind("<<ComboboxSelected>>", self.on_fuel_selected)
       
        # Create a label for status messages
        self.status_label = ttk.Label(self.root, text="", foreground="blue")
        self.status_label.grid(row=0, column=0, pady=5, padx=10, sticky="w")

        # ... (other initialization code)
        self.selected_file_path = None
        self.selected_file_content = None
        self.header = """/*--------------------------------*- C++ -*----------------------------------*\\
  =========                 |
  \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\\\    /   O peration     | Website:  https://openfoam.org
    \\\\  /    A nd           | Version:  10
     \\\\/     M anipulation  |
\\*---------------------------------------------------------------------------*/\n"""
        self.thermo_type_params = ["type", "mixture", "transport", "thermo", "equationOfState", "specie", "energy"]
        self.mixture_params = ["molWeight", "rho", "rho0", "p0", "B", "gamma", "Cv", "Cp", "Hf", "mu", "Pr"]

    def browse_directory(self):
        selected_file = filedialog.askopenfilename()

        if selected_file and os.path.basename(selected_file).startswith("physicalProperties"):
            self.selected_file_path = selected_file
            self.status_label.config(text=f"Selected file: {selected_file}", foreground="blue")

            # Update the current fuel status label
            current_fuel = self.detect_current_fuel()
            if current_fuel:
                self.status_label.config(text=f"Current fuel: {current_fuel}", foreground="blue")

                # Check if the detected current fuel matches any of the available fuels
                # If it does, set it as the selected fuel in the dropdown
                for fuel in self.fuels:
                    if fuel.lower() == current_fuel.lower():
                        self.selected_fuel.set(fuel)
                        break

            with open(selected_file, 'r') as file:
                file_content = file.read()
                self.selected_file_content = file_content
                old_values_mixture = {param: match.group(1) for param in self.mixture_params
                                      for match in re.finditer(f'{param}\s+(\S+)(;|;//.*)', file_content)}
                old_values_thermo_type = {param: match.group(1) for param in self.thermo_type_params
                                           for match in re.finditer(f'{param}\s+(\S+)(;|;//.*)', file_content)}
                self.open_replace_properties_popup(old_values_mixture, old_values_thermo_type)
        else:
            tk.messagebox.showerror("Error", "Selected file is not a physicalProperties file! Please look for the constant dir in your OF case!")
            

    def open_replace_properties_popup(self, old_values_mixture, old_values_thermo_type):
        selected_file = self.selected_file_path
        if selected_file:
            # Open a popup to replace the properties for the mixture and thermoType blocks
            ReplacePropertiesPopup(self, self.thermo_type_params, self.mixture_params, old_values_thermo_type, old_values_mixture)

        else:
            tk.messagebox.showerror("Error", "Please select a valid file first.")
            
    def detect_current_fuel(self):
        # Assuming the path is in the format '.../OpenFOAM-<version>/cases/<case_name>/constant/physicalProperties'
        parts = os.path.abspath(self.selected_file_path).split('.')   #split(os.sep)
        #partsi = os.path.abspath(self.selected_file_path).split('constant')   #split(os.sep)
        try:
            #index = parts.index('constant') 
            current_fuel = parts[1] # 0 + 1
            #print(current_fuel)
            return current_fuel
        except ValueError:
            return None
                  
    def on_fuel_selected(self, event):
        selected_fuel = self.fuel_options_menu.get().lower()
        if selected_fuel and selected_fuel != "Fuel Options":
            current_fuel = self.detect_current_fuel()
            if current_fuel:
                self.status_label.config(text=f"Current fuel: {current_fuel}", foreground="blue")
                self.replace_fuel(selected_fuel, current_fuel)

    def replace_fuel(self, selected_fuel, current_fuel):
        # Assuming the 'constant' directory is inside the case directory
        case_directory = os.path.dirname(os.path.dirname(self.selected_file_path))
            
        
        # Use find and exec to run sed on all files under the 'constant' directory
        #sed_command = f"sed -i 's/{current_fuel}/{selected_fuel}/g' {self.selected_file_path}" 
        sed_command = f"find {case_directory}/constant -type f -exec sed -i 's/{current_fuel}/{selected_fuel}/g' {{}} +"
        
        # Execute the sed command
        subprocess.run(sed_command, shell=True)
        
        # --------------------- Renaming files inside constant/ after the selected fuel ----------------------->
        # Rename the file associated with the current fuel
        current_file_path = os.path.join(case_directory, 'constant', f'physicalProperties.{current_fuel.lower()}')
        new_file_path = os.path.join(case_directory, 'constant', f'physicalProperties.{selected_fuel.lower()}')
        try:
            os.rename(current_file_path, new_file_path)
            tk.messagebox.showinfo("Fuel option", f"Fuel has been updated to {selected_fuel}!")
        except FileNotFoundError:
            # Handle the case where the file does not exist
            pass
            
        # Update the status label
        self.status_label.config(text=f"Fuel replaced. Selected fuel: {selected_fuel}", foreground="green")
        # -----------------------------------------------------------------------------------------------------<

            
    # -------------- Welcome Message --------------------------    
    def show_welcome_message(self):
        welcome_message = "Welcome to Splash - OpenFOAM!\n\n"\
                          "This is your interactive OpenFOAM simulation tool.\n"\
                          "Start by importing geometry and configuring your case."

        # You can choose to display the welcome message in a label or a messagebox
        # Label Example:
        welcome_label = ttk.Label(self.root, text=welcome_message, font=("TkDefaultFont", 12), background="lightblue")
        welcome_label.grid(row=0, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

        # OR

        # Messagebox Example:
        messagebox.showinfo("Welcome", welcome_message)
        welcome_label.destroy()
    # -------------- Welcome Message --------------------------    
    
    # -------------- Main logos --------------------------    
    def add_logos(self):

        # Load and display SMLT logo
        #self.logo_image = Image.open("logoWinGD.jpg")  # Replace with your logo file name
        self.logo_image = Image.open("logos/simulitica_logo.png")  # Replace with your logo file name
        self.logo_image = self.logo_image.resize((100, 60))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(self.root, image=self.logo_image)
        self.logo_label.grid(row=3, column=0, pady=10, padx=10, sticky="ew")

#        # Load and display openfoam logo
#        #self.logo_image = Image.open("logoWinGD.jpg")  # Replace with your logo file name
#        self.logo_image = Image.open("logos/simulitica_logo.png")  # Replace with your logo file name
#        self.logo_image = self.logo_image.resize((100, 60))
#        self.logo_image = ImageTk.PhotoImage(self.logo_image)
#        self.logo_label = tk.Label(self.root, image=self.logo_image)
#        self.logo_label.grid(row=3, column=0, pady=10, padx=10, sticky="ew")

        # Create a label for copyright text
        self.copyright_label = ttk.Label(self.root, text="© 2023 Simulitica Ltd")
        self.copyright_label.grid(row=4, column=0, pady=10, padx=10, sticky="ew")
            
   # -------------- Main logos --------------------------        
        
        
    # -------------- importing the geometry --------------------------------------------------------------------    
    def import_geometry(self):
        file_path = filedialog.askopenfilename(
            title="Select Geometry File",
            filetypes=[("STL Files", "*.stl"), ("OBJ Files", "*.obj"), ("All Files", "*.*")],
            initialdir=os.path.dirname(self.selected_file_path) if self.selected_file_path else None
        )

        if file_path:
            self.selected_file_path = file_path
            meshing_folder = os.path.join(os.path.dirname(self.selected_file_path), "Meshing")
            self.status_label.config(text="The geometry file is successfully imported!", foreground="blue")
            # To enable meshing to start
            self.geometry_loaded = True

            # Create the Meshing folder if it doesn't exist
            if not os.path.exists(meshing_folder):
                os.makedirs(meshing_folder)

            # Copy and rename the geometry file
            geometry_filename = f"CAD.{file_path.split('.')[-1].lower()}"
            geometry_dest = os.path.join(meshing_folder, geometry_filename)
            shutil.copyfile(self.selected_file_path, geometry_dest)
            
            # CAD programs logo paths 
            freecad_logo_path = os.path.join("logos", "freecad_logo.png")
            gmsh_logo_path = os.path.join("logos", "gmsh_logo.png")
            paraview_logo_path = os.path.join("logos", "paraview_logo.png")


            # Create a popup to ask the user whether to open the CAD file in FreeCAD, Gmsh, or ParaView
            popup = tk.Toplevel(self.root)
            popup.title("Choose CAD Viewer")
            popup.geometry("400x400")

            def open_freecad():
                subprocess.run(["freecad", geometry_dest, "&"], check=True)
                # Zoom to fit
                try:
                    doc = FreeCAD.ActiveDocument
                    doc.getObject(geometry_filename).ViewObject.Proxy.fit()
                except Exception as e:
                    print(f"Error zooming to fit in FreeCAD: {e}")
                popup.destroy()

            def open_gmsh():
                subprocess.run(["gmsh", geometry_dest, "&"], check=True)
                popup.destroy()

            def open_paraview():
                subprocess.run(["paraview", geometry_dest], check=True)
                popup.destroy()

            # Load logos
            freecad_logo = Image.open(freecad_logo_path).resize((160, 50), Image.ANTIALIAS)
            gmsh_logo = Image.open(gmsh_logo_path).resize((80, 70), Image.ANTIALIAS)
            paraview_logo = Image.open(paraview_logo_path).resize((200, 40), Image.ANTIALIAS)

            freecad_logo = ImageTk.PhotoImage(freecad_logo)
            gmsh_logo = ImageTk.PhotoImage(gmsh_logo)
            paraview_logo = ImageTk.PhotoImage(paraview_logo)

            # Create buttons with logos for the CAD viewers
            freecad_button = ttk.Button(popup, text="Open in FreeCAD", command=open_freecad, image=freecad_logo, compound="top")
            freecad_button.image = freecad_logo
            freecad_button.pack(side=tk.TOP, padx=30, pady=10)

            gmsh_button = ttk.Button(popup, text="Open in Gmsh", command=open_gmsh, image=gmsh_logo, compound="top")
            gmsh_button.image = gmsh_logo
            gmsh_button.pack(side=tk.TOP, padx=20, pady=10)

            paraview_button = ttk.Button(popup, text="Open in ParaView", command=open_paraview, image=paraview_logo, compound="top")
            paraview_button.image = paraview_logo
            paraview_button.pack(side=tk.TOP, padx=30, pady=10)

            popup.mainloop()
    
        else:
            tk.messagebox.showerror("Error", "No file selected for import")
        # -------------- importing the geometry --------------------------------------------------------------------    
            
            
    # --------------------- running the simulation ---------------------------
    def initialize_case(self):
        selected_directory = filedialog.askdirectory()
        if selected_directory:
            self.selected_file_path = selected_directory
            self.status_label.config(text=f"Case directory identified: {selected_directory}", foreground="blue")
            self.run_simulation_button["state"] = tk.NORMAL  # Enable the "Run Simulation" button
        else:
            self.status_label.config(text="No directory selected.", foreground="red")
            self.run_simulation_button["state"] = tk.DISABLED  # Disable the "Run Simulation" button


    def run_simulation(self):
        if self.selected_file_path is None:
            tk.messagebox.showerror("Error", "Please initialize the case directory before running the simulation.")
            return

        if not self.simulation_running:
            self.simulation_thread = threading.Thread(target=self.run_openfoam_simulation)
            self.simulation_thread.start()
            self.simulation_running = True
            self.stop_simulation_button["state"] = tk.NORMAL
        else:
            tk.messagebox.showinfo("Simulation Running", "Simulation is already running.")

    def run_openfoam_simulation(self):
        allrun_script = os.path.join(self.selected_file_path, "Allrun")
        if os.path.exists(allrun_script):
            chmod_command = ["chmod", "+x", allrun_script]
            subprocess.run(chmod_command, check=True)

            try:
                self.start_progress_bar()
                process = subprocess.run(["./Allrun"], cwd=self.selected_file_path, text=True, capture_output=True)
                print(process.stdout)
                print(process.stderr)

                if "Execution halted" not in process.stderr:
                    tk.messagebox.showinfo("Simulation Finished", "Simulation completed successfully.")
                else:
                    tk.messagebox.showerror("Simulation Error", "There was an error during simulation. Check the console output.")
            except subprocess.CalledProcessError as e:
                tk.messagebox.showerror("Error", f"Error running Allrun script: {e.stderr}")
            finally:
                self.stop_progress_bar()
                self.stop_simulation_button["state"] = tk.DISABLED
        else:
            tk.messagebox.showerror("Error", "Allrun script not found!")

    def stop_simulation(self):
        if not self.simulation_running:
            tk.messagebox.showinfo("Nothing to Stop", "There's no simulation currently running to stop.")
            return

        control_dict_path = os.path.join(self.selected_file_path, "system", "controlDict")
        if os.path.exists(control_dict_path):
            try:
                self.replace_end_time_with_write_now(control_dict_path)
                tk.messagebox.showinfo("Stop Simulation", "Simulation stopped successfully.")
                self.replace_write_now_with_end_time(control_dict_path)
            except subprocess.CalledProcessError as e:
                tk.messagebox.showerror("Error", f"Error stopping simulation: {e.stderr}")
        else:
            tk.messagebox.showerror("Error", "controlDict file not found!")

        self.stop_simulation_button["state"] = tk.DISABLED

    def replace_end_time_with_write_now(self, control_dict_path):
        subprocess.run(["sed", "-i", 's/endTime/writeNow/g', control_dict_path], check=True)
    def replace_write_now_with_end_time(self, control_dict_path):
        subprocess.run(["sed", "-i", 's/writeNow/endTime/g', control_dict_path], check=True)
        
                
    def start_progress_bar(self):
        # Start the custom progress bar with a sliding and fading effect
        self.progress_bar_canvas.delete("progress")
        self.progress_bar_canvas.coords("progress", 0, 0, 0, 20)
        self.fade_progress_color(0)

    def fade_progress_color(self, progress):
        # Darken the color by reducing the intensity
        intensity = int(255 - (progress * 2.55))
        color = "#{:02x}{:02x}{:02x}".format(intensity, 200, 80)

        # Set the new color and adjust the progress bar position
        self.progress_bar_canvas.itemconfig("progress", fill=color)
        self.progress_bar_canvas.coords("progress", progress, 0, progress + 200, 20)

        # Schedule the next fade iteration
        if progress < 100:
            self.root.after(50, lambda: self.fade_progress_color(progress + 1))

    def stop_progress_bar(self):
        # Stop the custom progress bar
        self.progress_bar_canvas.delete("progress")
        self.progress_bar_canvas.create_rectangle(0, 0, 200, 20, fill="lightblue", outline="#78c850", tags="progress")
        
    def create_mesh(self):
        # Check if geometry is loaded
        if not self.geometry_loaded:
            messagebox.showinfo("Geometry Not Loaded", "Please load a geometry before creating the mesh.")
            return

        # Ask the user for mesh type using clickable buttons
        mesh_type = self.ask_mesh_type()

        if mesh_type is not None:
            # Execute the meshing command based on the selected mesh type
            if mesh_type == "Cartesian":
                # Execute Cartesian mesh command
                pass  # Replace with the actual command
            elif mesh_type == "Polyhedral":
                # Execute Polyhedral mesh command
                pass  # Replace with the actual command
            elif mesh_type == "Tetrahedral":
                # Execute Polyhedral mesh command
                pass  # Replace with the actual command

    def ask_mesh_type(self):
        # Create a popup to ask the user for mesh type
        popup = tk.Toplevel(self.root)

        # Add clickable buttons for mesh type
        ttk.Radiobutton(popup, text="Cartesian", variable=self.mesh_type_var, value="Cartesian").pack()
        ttk.Radiobutton(popup, text="Polyhedral", variable=self.mesh_type_var, value="Polyhedral").pack()
        ttk.Radiobutton(popup, text="Tetrahedral", variable=self.mesh_type_var, value="Tetrahedral").pack()

        # Add a button to confirm the selection
        ttk.Button(popup, text="OK", command=popup.destroy).pack()

        # Wait for the popup to be closed
        self.root.wait_window(popup)

        # Return the selected mesh type
        return self.mesh_type_var.get()
         
    
###    def source_openfoam_libraries(self):
###        # Get the path to the user's home directory
###        home_directory = os.path.expanduser("~")

###        # Construct the full path to the OpenFOAM bashrc file
###        openfoam_bashrc = os.path.join(home_directory, "OpenFOAM", "OpenFOAM-v2012", "etc", "bashrc")

###        # Set up the environment for OpenFOAM by sourcing the relevant bashrc file
###        source_command = f"source {openfoam_bashrc} && exec $SHELL"
###        subprocess.run(source_command, shell=True, check=True)

###        # Now the environment should be set up, and you can run the 'of11' command
###        current_directory = os.getcwd()
###        process = subprocess.run(["of11"], cwd=current_directory, check=True, capture_output=True, text=True)
###        
###        # Check if the command was successful
###        if process.returncode == 0:
###            # Print only if the command was successful
###            print("Command output:", process.stdout)
###        else:
###            # Print both stdout and stderr if the command failed
###            print("Command output:", process.stdout)
###            print("Command error:", process.stderr)
        
        
        
if __name__ == "__main__":
    root = tk.Tk()
    app = TerminalApp(root)
    root.mainloop()   


#        # Monitor residuals using foamMonitor
#        self.monitor_residuals()

#    def monitor_residuals(self):
#        residuals_file = os.path.join(os.path.dirname(self.selected_file_path), "postProcessing", "residuals", "0", "residuals.dat")

#        # Check if the residuals file exists
#        if not os.path.exists(residuals_file):
#            tk.messagebox.showerror("Error", "Residuals file not found!")
#            return

#        # Run foamMonitor to continuously monitor residuals
#        foam_monitor_command = f"foamMonitor -l {residuals_file}"
#        process = subprocess.Popen(foam_monitor_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

#        # Read and display residuals in real-time
#        for line in iter(process.stdout.readline, b''):
#            print(line.decode("utf-8"))

#            # Extract residuals from the output and update the plot
#            residuals = [float(x) for x in re.findall(r"residual\s*=\s*([\d.]+)", line.decode("utf-8"))]

#            if residuals:
#                self.update_plot(residuals)

#        process.stdout.close()
#        process.stderr.close()

#        # Wait for foamMonitor to finish
#        process.wait()

#        # Update UI
#        self.simulation_running = False
#        print("Residual monitoring completed.")

#    def update_plot(self, residuals):
#        # Update the plot with new residuals
#        self.ax.clear()
#        self.ax.plot(residuals, label="Residuals")
#        self.ax.set_xlabel("Iteration")
#        self.ax.set_ylabel("Residual Value")
#        self.ax.legend()
#        self.canvas.draw()
    # --------------------- running the simulation ---------------------------
            
            

#    def import_geometry(self):
#        # Ask the user to select a geometry file
#        geometry_file = filedialog.askopenfilename(
#            #filetypes=[("Geometry files", "*.stl;*.obj"), ("All files", "*.*")],
#            filetypes=[("Geometry files", "*.stl"), ("All files", "*.*")],
#            initialdir=os.path.dirname(self.selected_file_path) if self.selected_file_path else None
#        )

#        if geometry_file:
#            # Get the destination path for the "Meshing" folder
#            meshing_folder = os.path.join(os.path.dirname(self.selected_file_path), "Meshing")

#            # Check if the "Meshing" folder exists; if not, create it
#            if not os.path.exists(meshing_folder):
#                os.makedirs(meshing_folder)

#            # Copy the selected geometry file to the "Meshing" folder and rename it to "CAD.stl"
#            geometry_file_name = "CAD.stl"
#            destination_path = os.path.join(meshing_folder, geometry_file_name)
#            shutil.copy(geometry_file, destination_path)

#            # Update the status label
#            self.status_label.config(text=f"Geometry file {geometry_file_name} imported to Meshing folder", foreground="green")
#        else:
#            self.status_label.config(text="Geometry import canceled", foreground="blue")
#            
#        # Check if a file is selected
#        if not self.selected_file_path:
#            self.status_label.config(text="No file selected for import", foreground="red")
#            return
           
         
            
#        # Configure rows and columns to expand
#        self.root.grid_columnconfigure(0, weight=1)
#        self.root.grid_columnconfigure(1, weight=1)
#        self.root.grid_columnconfigure(2, weight=1)
#        self.root.grid_columnconfigure(3, weight=1)

#        # Create an entry field for entering the command
#        self.entry = ttk.Entry(self.root, width=40)
#        self.entry.grid(row=0, column=0, pady=10, padx=10, columnspan=2, sticky="ew")

#        # Create a button to execute the command
#        self.execute_button = ttk.Button(self.root, text="Execute Command", command=self.execute_command)
#        self.execute_button.grid(row=0, column=2, pady=10, padx=10, sticky="ew")

#        # Create a label to display the status of the command execution
#        self.status_label = ttk.Label(self.root, text="", foreground="blue")
#        self.status_label.grid(row=1, column=0, pady=5, padx=10, columnspan=2, sticky="w")

#        # Create a button to stop the command execution
#        self.stop_button = ttk.Button(self.root, text="Stop Command", command=self.stop_command, state=tk.DISABLED)
#        self.stop_button.grid(row=0, column=3, pady=5, padx=10, sticky="ew")

#        # Create a button to start meshing
#        self.mesh_button = ttk.Button(self.root, text="Start Meshing!", command=self.create_mesh)
#        self.mesh_button.grid(row=1, column=3, pady=5, padx=10, sticky="ew")

#        # Create buttons to load and display images or GIFs
#        self.load_image_button = ttk.Button(self.root, text="Load Image or GIF", command=lambda: self.load_image("image1"))
#        self.load_image_button.grid(row=2, column=3, pady=10, padx=10, sticky="ew")

#        # Create labels to display the loaded images or GIFs
#        self.image_labels = []

#        # Load and display the logo
#        #self.logo_image = Image.open("logoWinGD.jpg")  # Replace with your logo file name
#        self.logo_image = Image.open("logoS.png")  # Replace with your logo file name
#        self.logo_image = self.logo_image.resize((100, 100))
#        self.logo_image = ImageTk.PhotoImage(self.logo_image)
#        self.logo_label = tk.Label(self.root, image=self.logo_image)
#        self.logo_label.grid(row=95, column=3, pady=10, padx=10, rowspan=5, columnspan=10, sticky="ew")

#        # Create a label for copyright text
#        self.copyright_label = ttk.Label(self.root, text="© 2023 Simulitica Ltd")
#        self.copyright_label.grid(row=100, column=3, rowspan=5, columnspan=6, pady=10, padx=10, sticky="ew")

#        self.terminal_process = None

#    # -------------------------- COMBOBOX ---------------------------------------
#    #=============================================================================
#    def execute_command(self):
#        #command = "source ~/.bashrc"; self.entry.get()
#        command = self.entry.get()

#        # Create a new terminal window and execute the command
#        self.terminal_process = subprocess.Popen(
#            #f"gnome-terminal -- bash -c 'source ~/.bashrc'",
#            f"gnome-terminal -- bash -c '{command}; exec bash'",
#            shell=True,
#            stdout=subprocess.PIPE,
#            stderr=subprocess.PIPE,
#            text=True,
#            preexec_fn=os.setsid,  # Create a new process group
#        )
#        # Enable the stop button
#        self.stop_button.config(state=tk.NORMAL)

#        # Disable the execute button
#        self.execute_button.config(state=tk.DISABLED)

#        # Monitor the terminal process and display the output
#        self.monitor_terminal()
## ================================================================
#    # Defining the function of meshing button 
#    def create_mesh(self):
#        command = "sh mesh.sh"

#        # Create a new terminal window and execute the command
#        self.terminal_process = subprocess.Popen(
#            f"gnome-terminal -- bash -c '{command}; exec bash'",
#            shell=True,
#            stdout=subprocess.PIPE,
#            stderr=subprocess.PIPE,
#            text=True,
#            preexec_fn=os.setsid,  # Create a new process group
#        )

#        # Enable the stop button
#        self.stop_button.config(state=tk.NORMAL)

#        # Disable the execute button
#        self.execute_button.config(state=tk.NORMAL)

#        # Monitor the terminal process and display the output
#        self.monitor_terminal()
## ================================================================
#    def monitor_terminal(self):
#        if self.terminal_process:
#            try:
#                # Read the standard output and standard error of the terminal
#                output, _ = self.terminal_process.communicate(timeout=0.1)
#                if output:
#                    self.output_text.insert(tk.END, output)
#                    self.output_text.see(tk.END)
#            except subprocess.TimeoutExpired:
#                # The terminal process is still running
#                self.root.after(100, self.monitor_terminal)
#            else:
#                # The terminal process has completed
#                self.execute_button.config(state=tk.NORMAL)
#                self.stop_button.config(state=tk.DISABLED)
#                self.status_label.config(text="Command executed successfully", foreground="green")
#                #self.status_label.delete(0, END)
## ================================================================
#    def stop_command(self):
#        if self.terminal_process:
#            # Terminate the terminal process and its process group
#            os.killpg(os.getpgid(self.terminal_process.pid), signal.SIGTERM)
#            self.status_label.config(text="Command execution stopped", foreground="red")
## ================================================================
#    def load_image(self, image_type):
#        file_path = filedialog.askopenfilename(filetypes=[
#            ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
#            ("GIF files", "*.gif")
#        ])
#        if file_path:
#            # Open and display the selected image or GIF using PIL
#            image = Image.open(file_path)
#            image = image.resize((800, 800))  # Resize the image as needed
#            photo = ImageTk.PhotoImage(image=image)
#            
#            # Create a new label for each loaded image
#            image_label = tk.Label(self.root, image=photo)
#            image_label.image = photo  # Keep a reference to prevent garbage collection
#            
#            # Append the label to the list and place it in the grid
#            self.image_labels.append(image_label)
#            row = len(self.image_labels) + 4
#            #column = 0 if image_type == "image" else (1 if image_type == "image2" else 2)
#            column = 0 
#            image_label.grid(row=row, column=column, pady=5, padx=10, sticky="nsew")
#            
#            self.status_label.config(text=f"{image_type.capitalize()} loaded successfully", foreground="green")
## ================================================================


