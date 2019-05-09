from card_tracker import CardTracker

import scipy.stats as ss
import pandas as pd
import numpy as np


def extract_feature(row, _hash):

  key = row['card_id']

  if key in _hash:
    card_tracker = _hash[key]
  else:
    card_tracker = CardTracker(key)
    _hash[key] = card_tracker

  return card_tracker.feed(row)


def extract_features_from_data(df):

  _hash = {}
  features = df.apply(lambda e: extract_feature(e, _hash), axis=1)

  features_df = pd.DataFrame(features.to_list(), columns = CardTracker.colnames)

  return features_df


def cramers_v(x, y):

  confusion_matrix = pd.crosstab(x,y)
  chi2 = ss.chi2_contingency(confusion_matrix)[0]
  n = confusion_matrix.sum().sum()
  phi2 = chi2/n
  r,k = confusion_matrix.shape
  phi2corr = max(0, phi2-((k-1)*(r-1))/(n-1))
  rcorr = r-((r-1)**2)/(n-1)
  kcorr = k-((k-1)**2)/(n-1)

  return np.sqrt(phi2corr/min((kcorr-1),(rcorr-1)))


def get_corr_for_categorical(df):

  columns = df.columns
  corr = pd.DataFrame(index=columns, columns=columns)

  for i in range(0, len(columns)):
    for j in range(0, len(columns)):

      if i == j:
        corr[columns[i]][columns[j]] = 1.0

      coef = cramers_v(df[columns[i]], df[columns[j]])
      corr[columns[i]][columns[j]] = coef
      corr[columns[j]][columns[i]] = coef

  corr.fillna(value = np.nan, inplace = True)

  return corr