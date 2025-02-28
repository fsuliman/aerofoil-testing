import matplotlib.pyplot as plt
import numpy as np

def box_plot_data(indep_var_values, data, x_label, y_label="lift force (Newtons)", title="Box plot of lift force as the independent variable changes"):
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.boxplot(data, patch_artist=True, tick_label = indep_var_values)
    # do color filling
    colors = ['cyan', 'lightblue', 'lightgreen', 'peachpuff', 'orange', 'tomato', 'lightcoral', 'pink', 'lightyellow', 'lightgrey']
    for patch, color in zip(ax['boxes'], colors):
        patch.set_facecolor(color)
    plt.show()