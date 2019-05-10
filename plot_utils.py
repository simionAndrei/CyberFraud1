import seaborn as sns
import numpy as np

import matplotlib.pyplot as plt
import sklearn.metrics as metrics

def create_roc_plot(plt_title, y_pred_prob, y_test, filename., logger):

  preds = y_pred_prob[:, 1]
  fpr, tpr, threshold = metrics.roc_curve(y_test, preds)
  roc_auc = metrics.auc(fpr, tpr)

  fig = plt.figure(figsize=(5, 5))
  sns.set()

  plt.title(plt_title)
  plt.plot(fpr, tpr, 'b', label = "{:.2f}".format(roc_auc))
  plt.plot([0 1], [0 1], 'r--')
  plt.xlabel("True positive rate")
  plt.ylabel("False positive rate")

  plt.xlim([0, 1])
  plt.ylim([0, 1])

  plt.legend(loc = 'lower right')

  plt.savefig(logger.get_output_file(filename), dpi = 120, 
    bbox_inches='tight')


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
  
  colormap = sns.diverging_palette(220, 10, as_cmap=True)

  ax[0].title.set_text("Fraud")
  sns.heatmap(feats_pair_fraud, cmap = colormap, ax = ax[0])

  sns.heatmap(feats_pair_non_fraud, cmap = colormap, ax = ax[1])
  ax[1].title.set_text("Non Fraud")

  plt.savefig(logger.get_output_file(filename), dpi = 120, bbox_inches='tight')


def create_barplot(data_df, filename, logger):

  ecomm_df = data_df[data_df.shopperinteraction == "Ecommerce"]
  ecomm_df = ecomm_df[['currencycode', 'amount', 'label']]
  ecomm_df = ecomm_df.groupby(['currencycode', 'label']).agg('sum')
  ecomm_df.reset_index(inplace = True)
  ecomm_df = ecomm_df.pivot(index = 'currencycode', columns='label',
    values = 'amount')
  ecomm_df.fillna(0, inplace = True)

  conta_df = data_df[data_df.shopperinteraction == "ContAuth"]
  conta_df = conta_df[['currencycode', 'amount', 'label']]
  conta_df = conta_df.groupby(['currencycode', 'label']).agg('sum')
  conta_df.reset_index(inplace = True)
  conta_df = conta_df.pivot(index = 'currencycode', columns='label',
    values = 'amount')
  conta_df.fillna(0, inplace = True)
    
  fig = plt.figure(figsize=(16, 6))
  sns.set()

  x_range_ecomm = np.array(range(ecomm_df.shape[0]))
  fraud_ecomm = [ecomm_df.loc[currc].iloc[1] for currc in ecomm_df.index.values]
  non_fraud_ecomm = [ecomm_df.loc[currc].iloc[0] for currc in ecomm_df.index.values]

  x_range_conta = np.array(range(conta_df.shape[0]))
  fraud_conta = [conta_df.loc[currc].iloc[1] for currc in conta_df.index.values]
  non_fraud_conta = [conta_df.loc[currc].iloc[0] for currc in conta_df.index.values]

  plt.subplot(1, 2, 1)
  plt.yticks(fontsize = 15)
  plt.axis([-0.5, 5, 10**4, 10**9.5])
  plt.title("Ecommerce", fontsize = 16)
  plt.ylabel("Amount", fontsize = 15)
  plt.bar(x_range_ecomm, fraud_ecomm, width = 0.4, color = 'red', log = True)
  plt.xticks(x_range_ecomm, ecomm_df.index.values, fontsize = 15)
  plt.bar(x_range_ecomm + 0.4, non_fraud_ecomm, width = 0.4, color = 'blue', log = True)
  plt.legend(["Fraud", "Non Fraud"], fontsize = 15)

  plt.subplot(1, 2, 2)
  plt.yticks(fontsize = 15)
  plt.axis([-0.5, 4, 10**4, 10**8])
  plt.title("ContAuth", fontsize = 16)
  plt.ylabel("Amount", fontsize = 15)
  plt.bar(x_range_conta, fraud_conta, width = 0.4, color = 'red', log = True)
  plt.xticks(x_range_conta, conta_df.index.values, fontsize = 15)
  plt.bar(x_range_conta + 0.4, non_fraud_conta, width = 0.4, color = 'blue', log = True)
  plt.legend(["Fraud", "Non Fraud"], fontsize = 15)

  
  plt.savefig(logger.get_output_file(filename), dpi = 120, fontsize = 16, bbox_inches='tight')