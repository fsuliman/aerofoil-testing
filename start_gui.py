"""
MIT License

Copyright (c) 2025 Fareed Suliman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import tkinter as tk
import threading
import time
import board
from plot_util import PlotUtility
from tkinter import Menu, ttk, simpledialog, filedialog, messagebox
from cedargrove_nau7802 import NAU7802
from csv_file_manager import CSVFileManager

class AerofoilTestingApp:
    
    samplesPerReading = 5
    DIAGNOSTIC_LOGGING = False
    accelerationDueToGravity = 9.8 # m.s^-2
    gaugeReadingAtTwentyGrams = 40544

    # Straing guage functions
    def zero_channel(self):
        """Initiate internal calibration for current channel.Use when scale is started,
        a new channel is selected, or to adjust for measurement drift. Remove weight
        and tare from load cell before executing."""
        print(
            "channel %1d calibrate.INTERNAL: %5s"
            % (self.nau7802.channel, self.nau7802.calibrate("INTERNAL"))
        )
        print(
            "channel %1d calibrate.OFFSET:   %5s"
            % (self.nau7802.channel, self.nau7802.calibrate("OFFSET"))
        )
        print("...channel %1d zeroed" % self.nau7802.channel)
        

    def recalibrate_guage(self):
        # Stub for recalibrate_guage
        print("Re-calibrate Guage button clicked")
        print("*** Instantiate and calibrate load cells")
        # Enable NAU7802 digital and analog power
        enabled = self.nau7802.enable(True)
        print("Digital and analog power enabled:", enabled)

        print("REMOVE WEIGHTS FROM LOAD CELLS")
        self.strainGuageStatus.set('Recalibrating...')
        time.sleep(3)

        self.nau7802.channel = 1
        self.zero_channel()  # Calibrate and zero channel
        self.strainGuageStatus.set('Calibrated')

    def read_raw_value(self, samples=samplesPerReading):
        """Read and average consecutive raw sample values. Return average raw value."""
        sample_sum = 0
        sample_count = samples
        while sample_count > 0:
            while not self.nau7802.available():
                pass
            sample_sum = sample_sum + self.nau7802.read()
            sample_count -= 1
        raw_reading = int(sample_sum / samples)
        return float((raw_reading/AerofoilTestingApp.gaugeReadingAtTwentyGrams)*0.02*AerofoilTestingApp.accelerationDueToGravity)
 
    def start_data_capture(self):
        # Stub for start_data_capture
        print("Start Data Capture button clicked")
        if self.dataCaptureOn or self.csvFileManager.get_csv_file_object() == None:
            return
        if (self.independentVariable.get() == "" or self.aerofoilIndependentVariable.get() == ""):
            messagebox.showinfo(parent=self.root, title="Aerofoil Testing App", message="Please set independent variable fields before attempting data capture.")
            return
        # Enable NAU7802 digital and analog power
        self.nau7802.enable(True)
        self.dataCaptureOn=True
        """ Create a thread to capture data without blocking the event thread """
        self.dataCaptureThread = threading.Thread(target=self.data_capture_thread_run_method, args=())
        self.dataCaptureThread.start()
        # Show real time plot
        self.plotUtility.plot_show()
    
    def data_capture_thread_run_method(self):
        while(self.dataCaptureOn):
            currentGaugeReading = float(self.read_raw_value())
            if (AerofoilTestingApp.DIAGNOSTIC_LOGGING):
                print("channel %1.0f raw value: %7.0f" % (self.nau7802.channel, currentGaugeReading))
            self.csvFileManager.write_csv_file([self.aerofoilIndependentVariable.get(),currentGaugeReading])
            self.currentGuageReading.set(currentGaugeReading)
            #Send sample to real-time plot
            self.plotUtility.real_time_plot_push_y_val(currentGaugeReading)

    def real_time_plot_zero(self):
        self.plotUtility.real_time_plot_zero()
        
    def end_data_capture(self):
        # Stub for end_data_capture
        print("End Data Capture button clicked")
        # Disable NAU7802 digital and analog power
        enabled = self.nau7802.enable(False)
        print("Digital and analog power enabled:", enabled)
        self.dataCaptureOn=False
        
    # Event handlers for UI
    def update_independent_variable(self):
        # Stub for update_independent_variable
        print("Update Independent Variable button clicked")

    def plot_file_data(self, showPlot=True):
        # Stub for plot_file_data
        print("Plot File Data button clicked")
        filename = self.csvDataFilename.get()
        if filename == "":
            messagebox.showerror(parent=self.root, title="Error", message="No data file open for read-only. Please open a data file for read-only.", detail="")
            if showPlot == False:
                return []
            else:
                return
        indep_var_name, indep_var_values, data = self.csvFileManager.extract_csv_file_data_for_plotting(filename)
        if data == [[]]:
            messagebox.showerror(parent=self.root, title="Error", message="Data file is open. Please close it before performing plot.", detail="")
            if showPlot == False:
                return []
            else:
                return
        else:
            return self.plotUtility.box_plot_data(indep_var_values, data, indep_var_name, show_plot=showPlot)
            
    def show_file_stats(self):
        # Stub for show_file_stats
        print("Show File Stats button clicked")
        file_stats_list = self.plot_file_data(showPlot=False)
        if file_stats_list == []:
            return
        stats_info_msg = ''
        for str in file_stats_list:
            stats_info_msg=stats_info_msg+str+'\n'
        messagebox.showinfo(parent=self.root, title="Current file statistics", message=f"{stats_info_msg}", detail="")

        
    """ File menu command handlers"""
    def new_file(self):
        file_name = simpledialog.askstring("New File", "Enter filename:", parent=self.root)
        if file_name != None:
            self.csvFileManager.new_csv_file(file_name, self.independentVariable.get())
            self.csvDataFilename.set(file_name)
        self.plotUtility.box_plot_clear()

    def open_file(self):
        file_name = filedialog.askopenfilename(parent=self.root, filetypes=[("CSV Files","*.csv")],title="Open CSV File")
        if (file_name != ()):
            self.csvFileManager.open_csv_file_for_append(file_name)
            self.csvDataFilename.set(file_name)
        self.plotUtility.box_plot_clear()

    def close_file(self):
        self.csvFileManager.close_csv_file()
    
    def show_about(self):
        messagebox.showinfo(parent=self.root, title="Aerofoil Testing App", message="About Aerofiol Testing Project", detail="This is Mikail Suliman's 5th Grade Science Project\nhttps://github.com/fsuliman/aerofoil-testing")
        
    def exit(self):
        self.csvFileManager.close_csv_file()
        self.plotUtility.plot_close()
        self.root.destroy()

    def __init__(self, root, fileManager, plotUtility):
        self.root = root
        self.root.title("Aerofoil Testing")
        self.csvFileManager = fileManager
        self.plotUtility = plotUtility
        
        # Create the menubar
        menubar = Menu(root)
        root.config(menu=menubar)

        # Create the File menu
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command = self.new_file)
        file_menu.add_command(label="Open", command = self.open_file)
        file_menu.add_command(label="Close", command = self.close_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command = self.exit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Create the Help menu
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command = self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        # Configure grid layout
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)

        # Create two independent side-by-side frames
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
        
        ttk.Label(frame1, text="Independent Variable for CSV File Header:").grid(row=1, column=0, sticky="ew")
        ttk.Combobox(frame1, textvariable=self.independentVariable, values=["Airspeed", "Angle of attack", "Camber/NACA ID"]).grid(row=1, column=1, sticky="ew")

        ttk.Label(frame1, text="        Enter independent variable value:").grid(row=2, column=0, sticky="w")
        ttk.Entry(frame1, textvariable=self.aerofoilIndependentVariable).grid(row=2, column=1, sticky="ew")

        # Separator space
        ttk.Label(frame1, text="                   ").grid(row=3, column=0, columnspan=2, sticky="ew")
        
        # frame1 buttons with callbacks
        ttk.Label(frame1, text="                   ").grid(row=3, column=0, columnspan=2, sticky="ew")
        ttk.Button(frame1, text="Start Data Capture", command=self.start_data_capture).grid(row=4, column=0, sticky="ew")
        ttk.Button(frame1, text="Stop Data Capture", command=self.end_data_capture).grid(row=4, column=1, sticky="ew")
        ttk.Label(frame1, text="                   ").grid(row=5, column=0, columnspan=2, sticky="ew")
        ttk.Button(frame1, text="Plot File Data", command=self.plot_file_data).grid(row=6, column=0, sticky="ew")
        ttk.Button(frame1, text="Show File Stats", command=self.show_file_stats).grid(row=6, column=1, sticky="ew")
        ttk.Label(frame1, text="                   ").grid(row=7, column=0, columnspan=2, sticky="ew")
        ttk.Button(frame1, text="Zero Real-time Plot", command=self.real_time_plot_zero).grid(row=8, column=0, sticky="ew")

        # Configure frame1 grid
        frame1.grid_columnconfigure(1, weight=1)

        # Widgets in frame2
        ttk.Label(frame2, text="Strain Guage Status:").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame2, textvariable=self.strainGuageStatus).grid(row=0, column=1, sticky="ew")
        # frame2 button with callback
        ttk.Button(frame2, text="Re-calibrate Guage", command=self.recalibrate_guage).grid(row=1, column=0, columnspan=2, sticky="ew")

        ttk.Label(frame2, text="                   ").grid(row=2, column=0, columnspan=2, sticky="ew")
        ttk.Label(frame2, text="Current Reading(N):").grid(row=3, column=0, sticky="w")
        ttk.Entry(frame2, textvariable=self.currentGuageReading).grid(row=3, column=1, sticky="ew")
        

        # frame 2 image of Mikail
        self.photo_image = tk.PhotoImage(file="airbus-a380.gif")
        ttk.Label(frame2, image=self.photo_image).grid(row=4, column=1, sticky="w")
                           
        # Configure frame2 grid
        frame2.grid_columnconfigure(1, weight=1)
        
        # Strain guage initialization
        # Instantiate 24-bit load sensor ADC; two channels, default gain of 128
        self.nau7802 = NAU7802(board.I2C(), address=0x2A, active_channels=2)
        self.dataCaptureOn=False
        self.strainGuageStatus.set('Ready/Uncalibrated')

def main():
    root = tk.Tk()
    csvFileManager = CSVFileManager()
    plotUtility = PlotUtility()
    app = AerofoilTestingApp(root, csvFileManager, plotUtility)
    root.mainloop()

if __name__ == "__main__":
    main()