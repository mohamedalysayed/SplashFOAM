import tkinter as tk
from tkinter import ttk
import re
from tkinter import simpledialog, messagebox

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
            value = entry.get() # gets the new values from the user 
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

            self.parent.status_label.config(text="Values replaced successfully")
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

            self.status_label.config(text="Parameters added successfully")

if __name__ == "__main__":
    # Code to instantiate and run the ReplacePropertiesPopup class if this script is run 
    pass
