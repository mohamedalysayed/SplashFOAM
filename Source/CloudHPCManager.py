import os
import tarfile
import shutil
import requests
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading

class CloudHPCManager:
    def __init__(self):
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
        # Load the API key from a file, ensuring the file exists
        dotenv_file = os.path.join(str(Path.home()), '.cfscloudhpc', 'apikey')
        print(f"Looking for API key at {dotenv_file}...")  # Debugging info
        if os.path.exists(dotenv_file):
            with open(dotenv_file, 'r') as file:
                api_key = file.readline().strip()
                if api_key:
                    print(f"API key found: '{api_key}'")  # Debugging info
                    return api_key
                else:
                    print("API key file exists but is empty.")  # Debugging info
        else:
            print(f"API key file not found. File will be created.")  # Debugging info
        return ""  # Return empty string if no key found

    def load_ssh_key(self):
        # Load the SSH key from a file, ensuring the file exists
        ssh_key_file = os.path.join(str(Path.home()), '.cfscloudhpc', 'sshkey')
        print(f"Looking for SSH key at {ssh_key_file}...")  # Debugging info
        if os.path.exists(ssh_key_file):
            with open(ssh_key_file, 'r') as file:
                ssh_key = file.readline().strip()
                if ssh_key:
                    print(f"SSH key found: '{ssh_key[:30]}...'")  # Debugging info (print first 30 chars)
                    return ssh_key
                else:
                    print("SSH key file exists but is empty.")  # Debugging info
        else:
            print(f"SSH key file not found. File will be created.")  # Debugging info
        return ""  # Return empty string if no SSH key found

    def save_keys(self, api_key, ssh_key):
        # Save the API key and SSH key to separate files, creating the directory if needed
        config_dir = os.path.join(str(Path.home()), '.cfscloudhpc')
        os.makedirs(config_dir, exist_ok=True)

        # Save API key
        with open(os.path.join(config_dir, 'apikey'), 'w') as api_file:
            api_file.write(api_key)
        print(f"API key successfully saved to {os.path.join(config_dir, 'apikey')}")  # Debugging info

        # Save SSH key
        with open(os.path.join(config_dir, 'sshkey'), 'w') as ssh_file:
            ssh_file.write(ssh_key)
        print(f"SSH key successfully saved to {os.path.join(config_dir, 'sshkey')}")  # Debugging info

    def prompt_for_keys(self):
        # Create a popup window to prompt the user for both API key and SSH key
        root = tk.Tk()
        root.title("Enter API and SSH Keys")
        root.geometry("500x250")

        api_key_var = tk.StringVar()
        ssh_key_var = tk.StringVar()

        # API Key entry
        tk.Label(root, text="Please enter your API Key:").pack(pady=10)
        api_key_entry = tk.Entry(root, textvariable=api_key_var, width=60)
        api_key_entry.pack(pady=5)
        api_key_entry.bind("<Control-v>", lambda event: api_key_entry.event_generate('<<Paste>>'))

        # SSH Key entry
        tk.Label(root, text="Please enter your SSH Key:").pack(pady=10)
        ssh_key_entry = tk.Entry(root, textvariable=ssh_key_var, width=60)
        ssh_key_entry.pack(pady=5)
        ssh_key_entry.bind("<Control-v>", lambda event: ssh_key_entry.event_generate('<<Paste>>'))

        def save_keys_and_proceed():
            api_key = api_key_var.get().strip()  # Trim any whitespace from API key
            ssh_key = ssh_key_var.get().strip()  # Trim any whitespace from SSH key
            print(f"API key entered: '{api_key}'")  # Debugging info
            print(f"SSH key entered: '{ssh_key[:30]}...'")  # Debugging info (first 30 chars)

            if api_key and ssh_key:  # If both keys are not empty
                self.api_key = api_key
                self.ssh_key = ssh_key
                self.save_keys(api_key, ssh_key)  # Save the API and SSH keys
                root.destroy()
                # After getting the keys, load the cloud options
                self.load_cloud_options()
            else:
                # Show an error message if either key is empty
                messagebox.showerror("Error", "Both API Key and SSH Key cannot be empty")
                print("Error: Either API key or SSH key is empty")  # Debugging info

        tk.Button(root, text="Save", command=save_keys_and_proceed).pack(pady=20)
        root.mainloop()

    def load_cloud_options(self):
        headers = {"X-API-key": self.api_key, "accept": "application/json"}

        # Load CPU options
        cpu_response = requests.get('https://cloud.cfdfeaservice.it/api/v2/simulation/view-cpu', headers=headers)
        self.cpu_options = cpu_response.json().get('response', [])

        # Load RAM options
        ram_response = requests.get('https://cloud.cfdfeaservice.it/api/v2/simulation/view-ram', headers=headers)
        self.ram_options = ram_response.json().get('response', [])

        # Load script options
        script_response = requests.get('https://cloud.cfdfeaservice.it/api/v2/simulation/view-scripts', headers=headers)
        self.script_options = script_response.json().get('response', [])

    def launch_simulation(self, folder_path, cpu, ram, script):
        # Compress the folder and upload it
        shutil.make_archive(os.path.join(os.path.join(folder_path, os.pardir), "simulation"), 'zip', folder_path)

        # Upload the file
        data = {
            "dirname": os.path.basename(folder_path),
            "filename": "simulation.zip",
            "contentType": "application/gzip"
        }
        headers = {'X-API-key': self.api_key, 'accept': 'application/json', 'Content-Type': 'application/json'}
        url_upload_response = requests.post('https://cloud.cfdfeaservice.it/api/v2/storage/upload-url', headers=headers, json=data)

        # Put request for uploading the file
        upload_file = requests.put(url_upload_response.json()['response']['url'], files={'file': open(os.path.join(folder_path, os.pardir, "simulation.zip"), 'rb')})

        # Launch the simulation
        data = {"cpu": int(cpu), "ram": ram, "folder": os.path.basename(folder_path), "script": script}
        simulation_exec = requests.post('https://cloud.cfdfeaservice.it/api/v2/simulation/add', headers=headers, json=data)

        print(f"Execution ID: {simulation_exec.json()['response']}")

    def open_ui(self):
        # Function to create the UI for Cloud HPC selection
        root = tk.Tk()
        root.title("Cloud HPC - Run")
        root.geometry("400x300")

        # API Key Entry (hidden by default, but we show it if no key is found)
        api_key_var = tk.StringVar(value=self.api_key)
        ssh_key_var = tk.StringVar(value=self.ssh_key)
        
        tk.Label(root, text="API Key:").pack(pady=5)
        api_key_entry = tk.Entry(root, textvariable=api_key_var, width=50)
        api_key_entry.pack(pady=5)
        api_key_entry.bind("<Control-v>", lambda event: api_key_entry.event_generate('<<Paste>>'))

        tk.Label(root, text="SSH Key:").pack(pady=5)
        ssh_key_entry = tk.Entry(root, textvariable=ssh_key_var, width=50)
        ssh_key_entry.pack(pady=5)
        ssh_key_entry.bind("<Control-v>", lambda event: ssh_key_entry.event_generate('<<Paste>>'))

        # CPU options dropdown
        cpu_var = tk.StringVar()
        cpu_var.set(self.cpu_options[0] if self.cpu_options else "Loading...")
        tk.Label(root, text="CPU:").pack(pady=5)
        tk.OptionMenu(root, cpu_var, *self.cpu_options).pack(pady=5)

        # RAM options dropdown
        ram_var = tk.StringVar()
        ram_var.set(self.ram_options[0] if self.ram_options else "Loading...")
        tk.Label(root, text="RAM:").pack(pady=5)
        tk.OptionMenu(root, ram_var, *self.ram_options).pack(pady=5)

        # Script options dropdown
        script_var = tk.StringVar()
        script_var.set(self.script_options[0] if self.script_options else "Loading...")
        tk.Label(root, text="Script:").pack(pady=5)
        tk.OptionMenu(root, script_var, *self.script_options).pack(pady=5)

        # Folder selection
        folder_path_var = tk.StringVar()
        tk.Label(root, text="Simulation Folder:").pack(pady=5)
        tk.Entry(root, textvariable=folder_path_var, width=50).pack(pady=5)
        tk.Button(root, text="Browse", command=lambda: folder_path_var.set(filedialog.askdirectory())).pack(pady=5)

        # Save API Key and Launch Simulation button
        def on_launch():
            self.api_key = api_key_var.get().strip()
            self.ssh_key = ssh_key_var.get().strip()
            print(f"API key being used: '{self.api_key}'")  # Debugging info
            print(f"SSH key being used: '{self.ssh_key[:30]}...'")  # Debugging info

            if not self.api_key or not self.ssh_key:
                messagebox.showerror("Error", "API Key and SSH Key cannot be empty")
                print("Error: Either API key or SSH key is empty")  # Debugging info
                return
            self.save_keys(self.api_key, self.ssh_key)
            self.launch_simulation(folder_path_var.get(), cpu_var.get(), ram_var.get(), script_var.get())
            root.destroy()

        tk.Button(root, text="Launch", command=on_launch).pack(pady=20)
        root.mainloop()
    
