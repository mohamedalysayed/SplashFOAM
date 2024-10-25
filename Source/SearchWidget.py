import tkinter as tk
from tkinter import ttk

class SearchWidget:
    def __init__(self, root, text_widget):
        self.text_widget = text_widget
        
        # Create an entry field for entering the commands by the user
        default_sentence = "Search here!" 
        self.search_entry = ttk.Entry(root, style='Professional.TEntry', width=18, foreground="lightblue", font=("Arial", 12, "bold"))
        self.search_entry.grid(row=9, column=4, pady=3, padx=1, sticky="sew")
        self.search_entry.insert(0, default_sentence)
        
        # Create a find a keyword
        search_button = tk.Button(root, text="Find", command=self.search_text)
        search_button.configure(relief="flat", background="lightblue", foreground="black", font=("Arial", 12, "bold"))
        search_button.grid(row=10, column=4, pady=3, padx=1, sticky="new")
        
        self.result_label = tk.Label(root, text="")
        self.result_label.grid(row=11, column=4, pady=3, padx=1, sticky="new")
        self.result_label.configure(background="white", foreground="black")

        # Bind the <Return> key event to the search function
        self.search_entry.bind("<Return>", lambda event: self.search_text())
        
        # Bind the <Up> and <Down> arrow keys
        root.bind("<Up>", lambda event: self.prev_occurrence())
        root.bind("<Down>", lambda event: self.next_occurrence())

        # Keep track of search results
        self.search_results = []
        self.current_result_index = 0

    def search_text(self):
        # Get the search term from the entry widget
        search_term = self.search_entry.get()

        # Clear previous tags
        self.text_widget.tag_remove("highlight", "1.0", tk.END)

        # Perform the search and highlight occurrences
        start_pos = "1.0"
        occurrences = 0
        self.search_results = []  # Clear previous search results

        while True:
            start_pos = self.text_widget.search(search_term, start_pos, stopindex=tk.END, nocase=True, exact=True)
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(search_term)}c"
            self.text_widget.tag_add("highlight", start_pos, end_pos)
            self.search_results.append((start_pos, end_pos))
            occurrences += 1
            start_pos = end_pos

        # Apply the highlighting tag
        self.text_widget.tag_config("highlight", background="yellow", foreground="black")

        # Update result label
        self.result_label.config(text=f"{occurrences} occurrences found!", background="white", foreground="darkblue", font=("Arial", 11, "bold"))
        self.current_result_index = 0

    def next_occurrence(self):
        if self.search_results:
            # Move to the next occurrence
            self.current_result_index = (self.current_result_index + 1) % len(self.search_results)
            start_pos, end_pos = self.search_results[self.current_result_index]

            # Highlight the current occurrence
            self.text_widget.tag_remove("highlight", "1.0", tk.END)
            self.text_widget.tag_add("highlight", start_pos, end_pos)
            self.text_widget.tag_config("highlight", background="yellow", foreground="black")

            # Scroll to the line of the current occurrence
            line_number = int(start_pos.split(".")[0])
            self.text_widget.yview_moveto((line_number - 1) / self.get_total_lines())

    def prev_occurrence(self):
        if self.search_results:
            # Move to the previous occurrence
            self.current_result_index = (self.current_result_index - 1) % len(self.search_results)
            start_pos, end_pos = self.search_results[self.current_result_index]

            # Highlight the current occurrence
            self.text_widget.tag_remove("highlight", "1.0", tk.END)
            self.text_widget.tag_add("highlight", start_pos, end_pos)
            self.text_widget.tag_config("highlight", background="yellow", foreground="black")

            # Scroll to the line of the current occurrence
            line_number = int(start_pos.split(".")[0])
            self.text_widget.yview_moveto((line_number - 1) / self.get_total_lines())

    def get_total_lines(self):
        return int(self.text_widget.index(tk.END).split(".")[0])
