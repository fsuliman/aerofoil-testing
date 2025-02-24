import tkinter as tk
from tkinter import Menu
from tkinter import ttk

class AerofoilTestingApp:

    def update_independent_variable(self):
        # Stub for update_independent_variable
        print("Update Independent Variable button clicked")

    def plot_file_data(self):
        # Stub for plot_file_data
        print("Plot File Data button clicked")

    def show_file_stats(self):
        # Stub for show_file_stats
        print("Show File Stats button clicked")

    def start_data_capture(self):
        # Stub for start_data_capture
        print("Start Data Capture button clicked")

    def end_data_capture(self):
        # Stub for end_data_capture
        print("End Data Capture button clicked")

    def recalibrate_guage(self):
        # Stub for recalibrate_guage
        print("Re-calibrate Guage button clicked")

    def __init__(self, root):
        self.root = root
        self.root.title("Aerofoil Testing")

        # Create the menubar
        menubar = Menu(root)
        root.config(menu=menubar)

        # Create the File menu
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="New")
        file_menu.add_command(label="Open")
        file_menu.add_command(label="Save")
        file_menu.add_command(label="Close")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Create the Help menu
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="About")
        menubar.add_cascade(label="Help", menu=help_menu)

        # Configure grid layout
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)

        # Create two independent frames using ttk
        frame1 = ttk.Frame(root, padding="3 3 12 12")
        frame1.grid(row=0, column=0, sticky="nsew")

        frame2 = ttk.Frame(root, padding="3 3 12 12")
        frame2.grid(row=0, column=1, sticky="nsew")

        # Variables
        self.csvDataFilename = tk.StringVar()
        self.aerofoilIndependentVariable = tk.StringVar()
        self.fileMode = tk.StringVar()
        self.independentVariable = tk.StringVar()
        self.strainGuageStatus = tk.StringVar()
        self.currentGuageReading = tk.StringVar()

        # Widgets in frame1
        ttk.Label(frame1, text="CSV Data Filename:").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame1, textvariable=self.csvDataFilename).grid(row=0, column=1, sticky="ew")

        ttk.Label(frame1, text="Aerofoil Independent Variable:").grid(row=1, column=0, sticky="w")
        ttk.Entry(frame1, textvariable=self.aerofoilIndependentVariable).grid(row=1, column=1, sticky="ew")

        ttk.Label(frame1, text="File mode:").grid(row=2, column=0, sticky="w")
        ttk.Combobox(frame1, textvariable=self.fileMode, values=["overwrite", "append"]).grid(row=2, column=1, sticky="ew")

        ttk.Button(frame1, text="Update Independent Variable", command=self.update_independent_variable).grid(row=3, column=0, sticky="ew")
        ttk.Combobox(frame1, textvariable=self.independentVariable, values=["airspeed", "angle of attack", "camber/shape ID"]).grid(row=3, column=1, sticky="ew")

        # frame1 buttons with callbacks
        ttk.Button(frame1, text="Plot File Data", command=self.plot_file_data).grid(row=4, column=0, sticky="ew")
        ttk.Button(frame1, text="Show File Stats", command=self.show_file_stats).grid(row=4, column=1, sticky="ew")
        ttk.Button(frame1, text="Start Data Capture", command=self.start_data_capture).grid(row=5, column=0, sticky="ew")
        ttk.Button(frame1, text="End Data Capture", command=self.end_data_capture).grid(row=5, column=1, sticky="ew")

        # Configure frame1 grid
        frame1.grid_columnconfigure(1, weight=1)

        # Widgets in frame2
        ttk.Label(frame2, text="Strain Guage Status:").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame2, textvariable=self.strainGuageStatus).grid(row=0, column=1, sticky="ew")

        ttk.Label(frame2, text="Current Reading:").grid(row=1, column=0, sticky="w")
        ttk.Entry(frame2, textvariable=self.currentGuageReading).grid(row=1, column=1, sticky="ew")
        
        # frame2 button with callback
        ttk.Button(frame2, text="Re-calibrate Guage", command=self.recalibrate_guage).grid(row=2, column=0, columnspan=2, sticky="ew")

        # Configure frame2 grid
        frame2.grid_columnconfigure(1, weight=1)

def main():
    root = tk.Tk()
    app = AerofoilTestingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()