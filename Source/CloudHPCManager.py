import os
import tarfile
import shutil
import requests
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading
import uuid


class CloudHPCManager:
    def __init__(self, selected_directory):
        self.selected_directory = selected_directory  # The loaded case's parent directory
        self.api_key = self.load_api_key()  # Load API key
        self.ssh_key = self.load_ssh_key()  # Load SSH key (optional)
        self.cpu_options = []
        self.ram_options = []
        self.script_options = []

        if not self.api_key or not self.ssh_key:
            self.prompt_for_keys()  # Prompt user for both API key and SSH key if not found
        else:
            self.load_cloud_options()

    def load_api_key(self):
        api_key_file = os.path.join(str(Path.home()), '.cfscloudhpc', 'apikey')
        if os.path.exists(api_key_file):
            with open(api_key_file, 'r') as file:
                return file.readline().strip()
        return ""

    def load_ssh_key(self):
        ssh_key_file = os.path.join(str(Path.home()), '.ssh', 'id_rsa.pub')
        if os.path.exists(ssh_key_file):
            with open(ssh_key_file, 'r') as file:
                return file.readline().strip()
        return ""

    def save_keys(self, api_key, ssh_key):
        config_dir = os.path.join(str(Path.home()), '.cfscloudhpc')
        os.makedirs(config_dir, exist_ok=True)

        with open(os.path.join(config_dir, 'apikey'), 'w') as api_file:
            api_file.write(api_key)

        with open(os.path.join(str(Path.home()), '.ssh', 'id_rsa.pub'), 'w') as ssh_file:
            ssh_file.write(ssh_key)

    def prompt_for_keys(self):
        root = tk.Tk()
        root.title("Enter API and SSH Keys")
        root.geometry("550x300")

        api_key_var = tk.StringVar()
        ssh_key_var = tk.StringVar()

        tk.Label(root, text="Please enter your API Key:").pack(pady=10)
        api_key_entry = tk.Entry(root, textvariable=api_key_var, width=40)
        api_key_entry.pack(pady=20)
        api_key_entry.bind("<Control-v>", lambda event: api_key_entry.event_generate('<<Paste>>'))

        tk.Label(root, text="Please enter your SSH Key:").pack(pady=10)
        ssh_key_entry = tk.Entry(root, textvariable=ssh_key_var, width=40)
        ssh_key_entry.pack(pady=25)
        ssh_key_entry.bind("<Control-v>", lambda event: ssh_key_entry.event_generate('<<Paste>>'))

        api_key_var.set(self.api_key)
        ssh_key_var.set(self.ssh_key)

        def save_keys_and_proceed():
            api_key = api_key_var.get().strip()
            ssh_key = ssh_key_var.get().strip()

            if api_key and ssh_key:
                self.api_key = api_key
                self.ssh_key = ssh_key
                self.save_keys(api_key, ssh_key)
                root.destroy()
                self.load_cloud_options()
            else:
                messagebox.showerror("Error", "Both API Key and SSH Key cannot be empty")

        tk.Button(root, text="Save", command=save_keys_and_proceed).pack(pady=20)
        root.mainloop()

    def load_cloud_options(self):
        headers = {"X-API-key": self.api_key, "accept": "application/json"}

        cpu_response = requests.get('https://cloud.cfdfeaservice.it/api/v2/simulation/view-cpu', headers=headers)
        self.cpu_options = cpu_response.json().get('response', [])

        ram_response = requests.get('https://cloud.cfdfeaservice.it/api/v2/simulation/view-ram', headers=headers)
        self.ram_options = ram_response.json().get('response', [])

        script_response = requests.get('https://cloud.cfdfeaservice.it/api/v2/simulation/view-scripts', headers=headers)
        self.script_options = script_response.json().get('response', [])
      
        
    # Error-handling-enhanced launch_simulation method [FLAG: this method is not fully mature yet]
    def launch_simulation(self, folder_path, cpu, ram, script):
        # Compress the folder
        archive_path = os.path.join(os.path.join(folder_path, os.pardir), "simulation")
        shutil.make_archive(archive_path, 'zip', folder_path)

        # Prepare the data for URL upload
        data = {
            "dirname": os.path.basename(folder_path),  # Folder name extracted here
            "filename": "simulation.zip",
            "contentType": "application/gzip"
        }
        headers = {'X-API-key': self.api_key, 'accept': 'application/json', 'Content-Type': 'application/json'}

        try:
            # Debugging: Check the folder name before the upload
            print(f"Folder name being sent: {os.path.basename(folder_path)}")

            # Request the URL for uploading the file
            url_upload_response = requests.post('https://cloud.cfdfeaservice.it/api/v2/storage/upload-url', headers=headers, json=data)

            # Check if the response is OK
            if url_upload_response.status_code != 200:
                print(f"Error fetching upload URL: {url_upload_response.status_code} - {url_upload_response.text}")
                return

            upload_url = url_upload_response.json().get('response', {}).get('url')
            if not upload_url:
                print(f"Error: No 'url' found in the upload response: {url_upload_response.json()}")
                return

            # Upload the file with the correct content-type
            with open(os.path.join(folder_path, os.pardir, "simulation.zip"), 'rb') as f:
                upload_file_response = requests.put(upload_url, data=f, headers={'Content-Type': 'application/gzip'})
                if upload_file_response.status_code != 200:
                    print(f"Error uploading file: {upload_file_response.status_code} - {upload_file_response.text}")
                    return

            # Launch the simulation
            data = {
                "cpu": int(cpu),
                "ram": ram,
                "folder": os.path.basename(folder_path),  # Use basename to get folder name
                "script": script
            }
            
            # Debugging: Print folder data being sent
            print(f"Launching simulation with folder: {os.path.basename(folder_path)}")
            
            simulation_exec_response = requests.post('https://cloud.cfdfeaservice.it/api/v2/simulation/add', headers=headers, json=data)

            # Check if the simulation execution response is OK
            if simulation_exec_response.status_code != 200:
                print(f"Error launching simulation: {simulation_exec_response.status_code} - {simulation_exec_response.text}")
                return

            # Extract the response
            exec_response = simulation_exec_response.json().get('response')
            if exec_response:
                print(f"Execution ID: {exec_response}")
            else:
                print(f"Error: No 'response' found in the simulation execution response: {simulation_exec_response.json()}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred during the request: {e}")    


    def open_ui(self):
        root = tk.Tk()
        root.title("Cloud HPC - Run")
        root.geometry("400x400")

        api_key_var = tk.StringVar(value=self.api_key)
        ssh_key_var = tk.StringVar(value=self.ssh_key)

        tk.Label(root, text="API Key:").pack(pady=5)
        api_key_entry = tk.Entry(root, textvariable=api_key_var, width=50)
        api_key_entry.pack(pady=5)

        tk.Label(root, text="SSH Key:").pack(pady=5)
        ssh_key_entry = tk.Entry(root, textvariable=ssh_key_var, width=50)
        ssh_key_entry.pack(pady=5)

        cpu_var = tk.StringVar(value="Select CPU" if not self.cpu_options else self.cpu_options[0])
        tk.Label(root, text="CPU:").pack(pady=5)
        cpu_menu = ttk.OptionMenu(root, cpu_var, *self.cpu_options)
        cpu_menu.pack(pady=5)

        ram_var = tk.StringVar(value="Select RAM" if not self.ram_options else self.ram_options[0])
        tk.Label(root, text="RAM:").pack(pady=5)
        ram_menu = ttk.OptionMenu(root, ram_var, *self.ram_options)
        ram_menu.pack(pady=5)

        script_var = tk.StringVar(value="Select Script" if not self.script_options else self.script_options[0])
        tk.Label(root, text="Script:").pack(pady=5)
        script_menu = ttk.OptionMenu(root, script_var, *self.script_options)
        script_menu.pack(pady=5)

        # Folder is automatically taken from the loaded case (self.selected_directory)
        folder_path_var = tk.StringVar(value=self.selected_directory)

        def on_launch():
            self.api_key = api_key_var.get().strip()
            self.ssh_key = ssh_key_var.get().strip()

            if not self.api_key or not self.ssh_key:
                messagebox.showerror("Error", "API Key and SSH Key cannot be empty")
                return

            self.save_keys(self.api_key, self.ssh_key)

            # Run the simulation in a separate thread to keep the UI responsive
            def run_simulation():
                self.launch_simulation(folder_path_var.get(), cpu_var.get(), ram_var.get(), script_var.get())

            threading.Thread(target=run_simulation).start()
            root.destroy()  # Close the UI after launching the simulation

        tk.Button(root, text="Launch", command=on_launch).pack(pady=20)
        root.mainloop()

