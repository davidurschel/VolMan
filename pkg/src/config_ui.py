import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tools import get_asset_path
from constants import ICON_FILE

class RailTab(ttk.Frame):
    def __init__(self, parent, rail_id):
        super().__init__(parent)
        self.rail_id = rail_id

        # Main layout
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Listbox
        self.listbox = tk.Listbox(self.main_frame, selectmode=tk.SINGLE)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Buttons
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.remove_button = ttk.Button(self.button_frame, text="Remove Selected", command=self.remove_selected)
        self.remove_button.pack(fill=tk.X)

        self.clear_button = ttk.Button(self.button_frame, text="Remove All", command=self.clear_list)
        self.clear_button.pack(fill=tk.X)

        self.master_button = ttk.Button(self.button_frame, text="Add Master", command=lambda: self.add_to_list("MASTER"))
        self.master_button.pack(fill=tk.X)

        self.others_button = ttk.Button(self.button_frame, text="Add Other", command=lambda: self.add_to_list("OTHER"))
        self.others_button.pack(fill=tk.X)

        # Text Input and Add Button
        self.input_frame = ttk.Frame(self)
        self.input_frame.pack(fill=tk.X, padx=10, pady=5)

        self.input_box = ttk.Entry(self.input_frame)
        self.input_box.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.add_button = ttk.Button(self.input_frame, text="Add Application", command=self.add_from_input)
        self.add_button.pack(side=tk.RIGHT)

        # Adjust the input box width
        self.update_input_width()

    def update_input_width(self):
        # Adjust the width of the input box to match the width of the listbox
        self.input_box.config(width=self.listbox.winfo_width() // 10)

    def remove_selected(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            self.listbox.delete(selected_index)

    def clear_list(self):
        self.listbox.delete(0, tk.END)

    def add_to_list(self, item):
        if item not in self.listbox.get(0, tk.END):
            self.listbox.insert(tk.END, item)

    def add_from_input(self):
        text = self.input_box.get().strip()
        if text:
            self.add_to_list(text)
            self.input_box.delete(0, tk.END)

class ConfigWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.num_rails = 0
        self.title("VolMan Configuration")

        # Set window icon
        self.iconbitmap(get_asset_path(ICON_FILE))
        
        # Create a vertical frame for COM port, BAUD rate, and active rails
        self.top_frame = ttk.Frame(self)
        self.top_frame.pack(fill=tk.X, padx=10, pady=10)

        # COM Port and BAUD Rate setup
        self.com_port_label = ttk.Label(self.top_frame, text="COM Port")
        self.com_port_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.com_port_dropdown = ttk.Combobox(self.top_frame, values=[f"COM{i}" for i in range(1, 257)])
        self.com_port_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        self.baud_rate_label = ttk.Label(self.top_frame, text="BAUD Rate")
        self.baud_rate_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        baud_rates = ["300", "1200", "2400", "4800", "9600", "14400", "19200", "38400", "57600", "115200"]
        self.baud_rate_dropdown = ttk.Combobox(self.top_frame, values=baud_rates)
        self.baud_rate_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

        # Active Rails setup
        self.rail_count_frame = ttk.Frame(self.top_frame)
        self.rail_count_frame.grid(row=2, column=0, columnspan=2, pady=5, sticky=tk.EW)

        self.rail_count_label = ttk.Label(self.rail_count_frame, text="Active Rails:")
        self.rail_count_label.pack(side=tk.LEFT, padx=5)

        self.rail_count_display = ttk.Label(self.rail_count_frame, text=str(self.num_rails))
        self.rail_count_display.pack(side=tk.LEFT, padx=5)

        self.add_rail_button = ttk.Button(self.rail_count_frame, text="Add Rail", command=self.add_tab)
        self.add_rail_button.pack(side=tk.RIGHT, padx=5)

        self.remove_rail_button = ttk.Button(self.rail_count_frame, text="Remove Rail", command=self.remove_tab)
        self.remove_rail_button.pack(side=tk.RIGHT, padx=5)

        # Tabs
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Buttons for saving
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        # Configure grid columns
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)
        self.button_frame.grid_columnconfigure(2, weight=1)

        self.load_saved_button = ttk.Button(self.button_frame, text="Load Save", command=self.load_saved_config)
        self.load_saved_button.grid(row=0, column=0, padx=5, sticky="ew")

        self.save_button = ttk.Button(self.button_frame, text="Save and Apply", command=self.save_config)
        self.save_button.grid(row=0, column=1, padx=5, sticky="ew")

        self.save_apply_button = ttk.Button(self.button_frame, text="Save, Apply, and Close", command=self.save_and_exit)
        self.save_apply_button.grid(row=0, column=2, padx=5, sticky="ew")

        self.init_tabs()

    def add_tab(self):
        rail_tab = RailTab(self.tabs, self.num_rails)
        self.tabs.add(rail_tab, text=f'Rail {self.num_rails + 1}')
        self.num_rails += 1
        self.rail_count_display.config(text=str(self.num_rails))

    def init_tabs(self):
        # Initialize tabs with default colors
        for _ in range(4):  # As we have default colors, we use a fixed number of tabs here
            self.add_tab()

    def remove_tab(self):
        if self.num_rails > 0:
            self.num_rails -= 1
            self.rail_count_display.config(text=str(self.num_rails))
            self.tabs.forget(self.num_rails)

    def load_saved_config(self):
        print("Loading Saved Config")

    def save_config(self):
        messagebox.showinfo("VolMan: COM Port Issue",
                            "Unable to read selected COM port. Ensure that COM port is correct and not being used by any other applications.")
        print("Save Config button clicked")

    def save_and_exit(self):
        self.save_config()
        self.destroy()


if __name__ == "__main__":
    config_ui = ConfigWindow()
    config_ui.geometry("600x500")
    config_ui.mainloop()