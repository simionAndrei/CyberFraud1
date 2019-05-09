import seaborn as sns
import numpy as np

import matplotlib.pyplot as plt

def create_heat_map(plt_title, corr_df, feats_names, filename, logger):

  fig = plt.figure(figsize=(8, 8))

  colormap = sns.diverging_palette(220, 10, as_cmap=True)
  sns.heatmap(corr_df, cmap = colormap, annot = True, fmt = ".2f")

  x = np.array(range(len(feats_names)))
  plt.xticks(x, feats_names)
  plt.yticks(x, feats_names)

  plt.savefig(logger.get_output_file(filename), dpi = 120, 
    bbox_inches='tight')


