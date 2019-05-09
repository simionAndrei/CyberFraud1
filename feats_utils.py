from card_tracker import CardTracker
import pandas as pd

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