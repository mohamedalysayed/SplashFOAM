import tkinter as tk
import re
from tkinter import ttk, simpledialog

class ReplaceControlDictParameters:
    def __init__(self, parent, control_dict_params, existing_values):
        self.parent = parent
        self.control_dict_params = control_dict_params
        self.existing_values = existing_values
        self.entry_widgets = {}
        self.new_values = {}
        
        # Show a confirmation popup -  Top Level 
        confirmation = tk.messagebox.askyesno("Simulation run", "In the following you can configure the setup of your simulation, or run it in the default mode. Are you ready?!")
        if confirmation:

            self.popup = tk.Toplevel(parent.root)
            self.popup.title("Update ControlDict Parameters")
            self.popup.geometry("400x800")

            # Create a label for the "ControlDict Parameters" group
            control_dict_label = ttk.Label(self.popup, text="ControlDict Parameters", font=("TkDefaultFont", 15, "bold"),
                                           foreground="red")
            control_dict_label.pack(pady=10)

            # Create entry fields for each parameter in the "ControlDict Parameters" group
            for param in control_dict_params:
                ttk.Label(self.popup, text=f"{param}").pack()
                entry_var = tk.StringVar()
                entry_var.set(existing_values.get(param, ""))
                entry = ttk.Entry(self.popup, textvariable=entry_var)
                entry.config(font=("TkDefaultFont", 9, "bold"), foreground="blue")
                entry.pack(pady=2)
                self.new_values[param] = entry_var
                self.entry_widgets[param] = entry

            # Create an "Update" button that calls the update_convtrol_dict_parameters method
            style = ttk.Style()
            style.configure("TButton", padding=20, relief="flat", background="lightblue", foreground="black", font=(12))  
            update_button = ttk.Button(self.popup, text="Update", command=self.update_control_dict_parameters)
            update_button.pack(pady=10)
            
            # Create a "Launch" button immediately starts the simulation 
            style = ttk.Style()
            style.configure("TButton", padding=20, relief="flat", background="lightblue", foreground="black", font=(12))  
            launch_button = ttk.Button(self.popup, text="Launch Simulation", command=self.launch_simulation_and_close)
            launch_button.pack(pady=10)
        else:
            tk.messagebox.showinfo("Process Canceled", "No changes were made nor simulations were run.")
            
            # Giving the user the possibility to re-run the simulation
            self.parent.simulation_running = False

    def update_control_dict_parameters(self):

        # Get the new values from the entry fields
        new_values = {param: entry.get() for param, entry in self.new_values.items()}

        # Update controlDict parameters
        self.replace_control_dict_parameters(new_values)
        
    def launch_simulation_and_close(self):
        # Close the popup window
        self.popup.destroy()
        
        # Now, run the simulation
        self.parent.run_openfoam_simulation()

    def replace_control_dict_parameters(self, new_values):
        controlDict_start = 'FoamFile\n{'
        controlDict_end = '}'
        
        # Extract the FoamFile block content
        controlDict_content = re.search(f'{controlDict_start}(.*?){controlDict_end}', self.parent.selected_control_file_content, re.DOTALL).group()

        # Split the file content into header, FoamFile, and body
        controlDict_end_position = self.parent.selected_control_file_content.find(controlDict_end, self.parent.selected_control_file_content.find(controlDict_start)) + len(controlDict_end)
        controlDict_content = self.parent.selected_control_file_content[self.parent.selected_control_file_content.find(controlDict_start):controlDict_end_position]
        body_content = self.parent.selected_control_file_content[controlDict_end_position:]

        # Replace old values with new ones in the body content for control file parameters
        for param, entry in self.new_values.items():
            value = new_values[param]  # gets the new values from the user 
            if value != "":
                old_pattern = f'{param}\\s*([^;]+)'
                new_pattern = f'{param} {value}'

                # Access the entry widget directly from the dictionary
                entry_widget = self.entry_widgets[param]
                if isinstance(entry_widget, ttk.Entry):
                    body_content = re.sub(old_pattern, new_pattern, body_content)

        # Combine the header, FoamFile, and updated body content
        file_content = f'{self.parent.header}{controlDict_content}{body_content}'

        # Show a confirmation popup
        confirmation = tk.messagebox.askyesno("Confirmation", "Are you sure you want to update the file?")
        if confirmation:
            # Write the updated content to the file
            with open(self.parent.control_dict_file_path, 'w') as file:
                file.write(file_content)

            # Show a confirmation popup after updating controlDict parameters
            tk.messagebox.showinfo("Update", "ControlDict parameters updated successfully.")
        else:
            tk.messagebox.showinfo("Update Canceled", "No changes were made.")
