#from tkinter import *
import tkinter as tk 
from tkinter.simpledialog import askstring
from tkinter import ttk, filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import subprocess
import os
import re 
import signal


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
        self.popup.geometry("500x600")  # Set the size of the popup window

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
        updateButton = ttk.Button(self.popup, text="Update", command=self.replace_mixture_values).grid(row=row_counter, column=2, pady=10, padx=10)
        addButton = ttk.Button(self.popup, text="Add parameter", command=self.add_missing_parameters).grid(row=row_counter_plus, column=2, pady=10, padx=10)
        #updateButton.pack()
        #addButton.pack()

        
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
                
            
            
class TerminalApp:
        
    def __init__(self, root):
        self.root = root
        self.root.config(background="white") # black
        self.root.title("Splash some colors here!")
        
        # Initialize the available fuels to choose from
        self.fuels = ["Methanol", "Ammonia", "Dodecane"]

        # Create a button to open a directory dialog
        style = ttk.Style()
        #style.configure("TButton", background="#3EAAAF")
        # --> style.configure("TButton", padding=10, relief="flat", background="#3EAAAF", foreground="black")
        style.configure("TButton", padding=10, relief="flat", background="lightblue", foreground="black")
        self.browse_button = ttk.Button(self.root, text="Update Physical Properties", command=self.browse_directory)
        self.browse_button.grid(row=1, column=2, pady=5, padx=10, sticky="ew")

        # Create a label for the "Fuel Selector" dropdown
        #self.fuel_selector_label = ttk.Label(self.root, text="Fuel Options", font=("TkDefaultFont", 10, "bold"), background="lightblue") # , foreground="green")
        self.fuel_selector_label = ttk.Label(self.root, text="Fuel Options →", font=("TkDefaultFont", 12), background="lightblue") # , foreground="green")
        self.fuel_selector_label.grid(row=1, column=0, pady=5, padx=10, sticky="w")

        # Define the fuel options
        fuels = ["Methanol", "Ammonia", "Dodecane"]

        # Create a StringVar to store the selected fuel
        self.selected_fuel = tk.StringVar()

        # Set a default value for the dropdown
        default_value = "Methanol"
        self.selected_fuel.set(default_value)

        # Create a dropdown menu for fuel selection
        self.fuel_selector = ttk.Combobox(self.root, textvariable=self.selected_fuel, values=fuels)
        self.fuel_selector.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        # Bind an event handler to the <<ComboboxSelected>> event
        self.fuel_selector.bind("<<ComboboxSelected>>", self.on_fuel_selected)
       
        # Create a label for status messages
        self.status_label = ttk.Label(self.root, text="", foreground="blue")
        self.status_label.grid(row=2, column=0, pady=5, padx=10, sticky="w")

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
        self.mixture_params = ["molWeight", "rho0", "p0", "B", "gamma", "Cv", "Cp", "Hf", "mu", "Pr"]

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
        selected_fuel = self.selected_fuel.get().lower()
        if selected_fuel:
            current_fuel = self.detect_current_fuel()
            if current_fuel:
                self.status_label.config(text=f"Current fuel: {current_fuel}", foreground="blue")
                self.replace_fuel(selected_fuel, current_fuel)

    def replace_fuel(self, selected_fuel, current_fuel):
        # Assuming the 'constant' directory is inside the case directory
        case_directory = os.path.dirname(os.path.dirname(self.selected_file_path))
            
        
        # Use find and exec to run sed on all files under the 'constant' directory
        #sed_command = f"sed -i 's/{current_fuel}/{selected_fuel}/g' {self.selected_file_path}" # maybe change to one higher level up in case we need to change all files
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
        # -----------------------------------------------------------------------------------------------------<

        # Update the status label
        self.status_label.config(text=f"Fuel replaced. Selected fuel: {selected_fuel}", foreground="green")
       
            
if __name__ == "__main__":
    root = tk.Tk()
    app = TerminalApp(root)
    root.mainloop()            
            
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


