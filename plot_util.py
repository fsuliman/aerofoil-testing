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
import numpy as np

def box_plot_data(indep_var_values, data, x_label, y_label="Lift force (Newtons)", title="Box plot of lift force as the independent variable changes", show_plot=True):
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    bplot = ax.boxplot(data, patch_artist=True, labels = indep_var_values, showmeans=True, meanline=True, meanprops={"color":"green"})
    # do color filling
    colors = ['tomato', 'lightcoral', 'orange', 'peachpuff', 'pink', 'lightyellow', 'lightgrey']
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
    iterator = iter(indep_var_values)
    stats_str = []
    for means in bplot['means']:
        stats_str.append(f"x-value: {next(iterator)} ; mean lift: {means.get_ydata(orig=False)[0]} N")
    if show_plot == True:
        plt.show()
    return stats_str 