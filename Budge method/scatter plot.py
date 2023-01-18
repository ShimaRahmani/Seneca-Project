def ScatterPlot_AllVehicles(joint_path , regression_file):
    scatter_points = pd.read_csv(joint_path + regression_file)
    plt.scatter(scatter_points['Length_m'],scatter_points['Duration'])
    plt.xlabel('Distance (meter)')
    plt.ylabel('Travel Time (min)')
    plt.savefig('plot.png', dpi=300, bbox_inches='tight')
#     plt.show(block=False)
#     plt.show()
#     plt.savefig('file_name.png')

import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas as pd