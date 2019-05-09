import seaborn as sns
import numpy as np

import matplotlib.pyplot as plt

def create_correlation_heatmap(plt_title, corr_df, feats_names, filename, logger):

  fig = plt.figure(figsize=(8, 8))

  colormap = sns.diverging_palette(220, 10, as_cmap=True)
  ax = sns.heatmap(corr_df, cmap = colormap, annot = True, fmt = ".2f")
  ax.set_title(plt_title)

  x = np.array(range(len(feats_names)))
  plt.xticks(x, feats_names)
  plt.yticks(x, feats_names)

  plt.savefig(logger.get_output_file(filename), dpi = 120, 
    bbox_inches='tight')



def create_categories_heatmap(data_df, feats_pair, filename, logger):

  crt_df = data_df[feats_pair + ["label"]]
  crt_fraud_df = crt_df[crt_df.label == 1]
  crt_non_fraud_df = crt_df[crt_df.label == 0]

  feats_pair_fraud = crt_fraud_df.groupby(feats_pair).agg('count')
  feats_pair_fraud.reset_index(inplace = True)
  feats_pair_fraud = feats_pair_fraud.pivot(index = 'txvariantcode', columns='currencycode',
    values = 'label')
  feats_pair_fraud.fillna(0, inplace = True)
  feats_pair_fraud = feats_pair_fraud.apply(lambda x: np.log(x + 1), axis = 1)

  feats_pair_non_fraud = crt_non_fraud_df.groupby(feats_pair).agg('count')
  feats_pair_non_fraud.reset_index(inplace = True)
  feats_pair_non_fraud = feats_pair_non_fraud.pivot(index = 'txvariantcode', columns='currencycode',
    values = 'label')
  feats_pair_non_fraud.fillna(0, inplace = True)
  feats_pair_non_fraud = feats_pair_non_fraud.apply(lambda x: np.log(x + 1), axis = 1)

  fig, ax = plt.subplots(1,2, figsize=(16,5))
  
  ax[0].title.set_text("Fraud")
  sns.heatmap(feats_pair_fraud, cmap = colormap, ax = ax[0])

  sns.heatmap(feats_pair_non_fraud, cmap = colormap, ax = ax[1])
  ax[1].title.set_text("Non Fraud")

  plt.savefig(logger.get_output_file(filename), dpi = 120, bbox_inches='tight')