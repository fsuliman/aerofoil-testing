import matplotlib as matplot
import matplotlib.pyplot as plt
import numpy as np

def box_plot_data(indep_var_values, data, x_label, y_label="Lift force (Newtons)", title="Box plot of lift force as the independent variable changes"):
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    bplot = ax.boxplot(data, patch_artist=True, labels = indep_var_values, showmeans=True, meanline=True, meanprops={"color":"green"})
    # do color filling
    colors = ['tomato', 'lightcoral', 'orange', 'peachpuff', 'pink', 'lightyellow', 'lightgrey']
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)

    plt.show()