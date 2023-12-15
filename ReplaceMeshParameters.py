import tkinter as tk
import re
from tkinter import ttk, simpledialog

class ReplaceMeshParameters:
    def __init__(self, parent, mesh_params, existing_values):
        self.parent = parent
        self.mesh_params = mesh_params
        self.existing_values = existing_values
        self.entry_widgets = {}  # Dictionary to store references to entry widgets
        self.new_values = {}

        self.popup = tk.Toplevel(parent.root)
        self.popup.title("Update Mesh Parameters")
        self.popup.geometry("300x400")  # Set the size of the popup window

        # Create a label for the "Mesh Parameters" group
        mesh_label = ttk.Label(self.popup, text="Mesh Parameters", font=("TkDefaultFont", 15, "bold"), foreground="red")
        mesh_label.pack(pady=10)

        # Create entry fields for each parameter in the "Mesh Parameters" group
        for param in mesh_params:
            ttk.Label(self.popup, text=f"{param}").pack()
            entry_var = tk.StringVar()
            entry_var.set(existing_values.get(param, ""))
            entry = ttk.Entry(self.popup, textvariable=entry_var)
            entry.config(font=("TkDefaultFont", 9, "bold"), foreground="blue")
            entry.pack(pady=2)
            self.new_values[param] = entry_var
            self.entry_widgets[param] = entry  # Store a reference to the entry widget
            
        # Create an "Update" button that calls the update_mesh_parameters method
        style = ttk.Style()
        style.configure("TButton", padding=10, relief="flat", background="lightblue", foreground="black")
        update_button = ttk.Button(self.popup, text="Update", command=self.update_mesh_parameters)
        update_button.pack(pady=10)

    def update_mesh_parameters(self):
        # Close the popup
        self.popup.destroy()

        # Get the new values from the entry fields
        new_values = {param: entry.get() for param, entry in self.new_values.items()}

        # Update mesh parameters (you need to implement this part based on your application's needs)
        self.replace_mesh_parameters(new_values)

    def replace_mesh_parameters(self, new_values):
        meshdict_start = 'FoamFile\n{'
        meshdict_end = '}'
        
        # Extract the FoamFile block content
        meshdict_content = re.search(f'{meshdict_start}(.*?){meshdict_end}', self.parent.selected_mesh_file_content, re.DOTALL).group()

        # Split the file content into header, FoamFile, and body
        meshdict_end_position = self.parent.selected_mesh_file_content.find(meshdict_end, self.parent.selected_mesh_file_content.find(meshdict_start)) + len(meshdict_end)
        meshdict_content = self.parent.selected_mesh_file_content[self.parent.selected_mesh_file_content.find(meshdict_start):meshdict_end_position]
        body_content = self.parent.selected_mesh_file_content[meshdict_end_position:]

        # Replace old values with new ones in the body content for mesh parameters
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
        file_content = f'{self.parent.header}{meshdict_content}{body_content}'

        # Show a confirmation popup
        confirmation = tk.messagebox.askyesno("Confirmation", "Are you sure you want to update the file?")
        if confirmation:
            # Write the updated content to the file
            with open(self.parent.mesh_dict_file_path, 'w') as file:
                file.write(file_content)

            self.parent.status_label.config(text="Mesh parameters' values are updated successfully!", foreground="green")
            
#            #_______________________________________________________________________________________
            # Show a confirmation popup after ReplaceMeshParameters finishes
            confirmation = tk.messagebox.askyesno("Confirmation", "Do you want to start meshing?")
            if confirmation:
                self.popup.destroy()  # Close the ReplaceMeshParameters popup
                self.parent.start_meshing()   #Start the meshing process
            else:
                tk.messagebox.showinfo("Meshing Canceled", "No mesh will be created.")
#            #_______________________________________________________________________________________
##            tk.messagebox.showinfo("Update", "Mesh parameters updated successfully.")
##            self.popup.destroy()
        else:
            tk.messagebox.showinfo("Update Canceled", "No changes were made.")
            
            
           
