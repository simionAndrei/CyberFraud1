import seaborn as sns
import numpy as np

import matplotlib.pyplot as plt

def create_heat_map(plt_title, data_df, filename, logger):

  #fig = plt.figure(figsize=(7, 7))

  colormap = sns.diverging_palette(220, 10, as_cmap=True)
  sns.heatmap(data_df.corr(), cmap = colormap, annot = True, fmt = ".2f")

  x = np.array(range(data_df.shape[0]))
  plt.xticks(x, data_df.columns)
  plt.yticks(x, data_df.columns)

  '''
  plt.savefig(logger.get_output_file(filename), dpi = 120, 
    bbox_inches='tight')
  plt.close()
  '''

  plt.show()


