import matplotlib.pyplot as plt
import numpy as np

def outliers_detection (variable):
  """
    Plot a variable distribution and graphically shows outliers.   
    Args:
        variable: vector of a dataframe
            Input variable.
    """
  fig, axes = plt.subplots(nrows=1, ncols=2)
  fig.suptitle(variable)
  axes[0].hist(df_subset[variable])
  axes[1].boxplot(x=variable, data=df)
  plt.show()
  percentile_25 = np.percentile(df_subset[variable], 25)
  percentile_50 = np.percentile(df_subset[variable], 50)
  percentile_75 = np.percentile(df_subset[variable], 75)
  print(f"mín = {df_subset[variable].min()}")
  print(f"Percentile 0.25 = {percentile_25}")
  print(f"Percentile 0.50 = {percentile_25}")
  print(f"Percentile 0.75 = {percentile_75}")
  print(f"max = {df_subset[variable].max()}")