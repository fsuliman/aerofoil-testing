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
import matplotlib as matplot
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import threading

class PlotUtility:
    
    def __init__(self, x_label="Real-time Samples", y_label="Lift force (Newtons)", title="Line plot of Real-Time data capture"):
        self._lock = threading.Lock()
        self.box_plot_fig = None
        self.bplot = None
        self.independent_var_name_in_header = None

        # Real time plot parameters
        self.x_len = 200 # Number of points to display
        self.y_range = [-0.005, 0.04] # Range of possible y values to display
        #self.real_time_fig = plt.subplots()
        self.real_time_plot_line = None
        self.y_values = [0] * self.x_len
        self.xs = list(range(0, 200))
        self.ani = None
        
        self.real_time_fig, self.ax = plt.subplots()
        self.ax.set_ylim(self.y_range)
        # Create a blank line. We will update the line in real_time_plot_animate
        self.real_time_plot_line, = self.ax.plot(self.xs, self.y_values)
        # Add axes and plot labels
        self.ax.set_title(title)
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        # Set up plot to call real_time_plot_animate() function periodically
        #self.ani = animation.FuncAnimation(self.real_time_fig,self.real_time_plot_animate,fargs=(self.y_values,),interval=1000,blit=False)
        self.ani = animation.FuncAnimation(self.real_time_fig,self.real_time_plot_animate,interval=1000,blit=True)


    def real_time_plot_animate(self, i):
        with self._lock:
            self.real_time_plot_line.set_ydata(self.y_values)
            return self.real_time_plot_line,

    def plot_show(self):
        plt.show()
        
    def plot_close(self):
        plt.close(fig="all")
        
    def real_time_plot_push_y_val(self, y_val):
        with self._lock:
            # Add y_val to list
            self.y_values.append(y_val)
            # Limit y list to set number of items
            self.y_values = self.y_values[-self.x_len:]
        
    def real_time_plot_zero(self):
        with self._lock:
            self.y_values = [0] * self.x_len
        
    def box_plot_clear(self):
        if (self.box_plot_fig != None):
            plt.close(fig =self.box_plot_fig) 
            self.box_plot_fig = None
        

    def box_plot_data(self, indep_var_values, data, x_label, y_label="Lift force (Newtons)", title="Box plot of lift force as the independent variable changes", show_plot=True):
        if self.box_plot_fig == None:
            self.box_plot_fig, ax = plt.subplots()
            ax.set_title(title)
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
            self.bplot = ax.boxplot(data, patch_artist=True, labels = indep_var_values, showmeans=True, meanline=True, meanprops={"color":"green"})
            # do color filling
            colors = ['tomato', 'lightcoral', 'orange', 'peachpuff', 'pink', 'lightyellow', 'lightgrey']
            for patch, color in zip(self.bplot['boxes'], colors):
                patch.set_facecolor(color)
        iterator = iter(indep_var_values)
        stats_str = []    
        for means in self.bplot['means']:
            stats_str.append(f"x-value: {next(iterator)} ; mean lift: {means.get_ydata(orig=False)[0]} N")
        if show_plot == True:
            plt.show()
        return stats_str 
