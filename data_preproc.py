from feats_utils import extract_features_from_data
from sklearn import preprocessing

from random import randint
import pandas as pd
import math
import os


class DataPreprocessor():

  def __init__(self, logger):

    self.logger = logger
    self._read_data()


  def _read_data(self):

    self.logger.log("Reading transactions file...")
    self.df = pd.read_csv(self.logger.get_data_file(self.logger.config_dict['DATA_FILE']))
    self.logger.log("Finish reading {} rows".format(self.df.shape[0]), show_time = True)


  def _drop_nans(self):

    crt_size = self.df.shape[0]
    self.df['mail_id'] = self.df['mail_id'].str.replace('email','')
    self.df.drop(self.df[self.df.mail_id == "NA"].index, inplace=True)
    self.df['mail_id'] = pd.to_numeric(self.df['mail_id'])

    self.df['ip_id']   = self.df['ip_id'].str.replace('ip','')
    self.df.drop(self.df[self.df.ip_id == "NA"].index, inplace=True)
    self.df['ip_id'] = pd.to_numeric(self.df['ip_id'])

    self.df['card_id'] = self.df['card_id'].str.replace('card','')
    self.df.drop(self.df[self.df.card_id == "NA"].index, inplace=True)
    self.df['card_id'] = pd.to_numeric(self.df['card_id'])

    self.df.dropna(axis = 0, inplace = True)
    self.logger.log("Dropping NaNs {}".format(crt_size - self.df.shape[0]))


  def _drop_refused_transactions(self):

    crt_size = self.df.shape[0]
    self.df.drop(self.df[self.df.simple_journal == "Refused"].index, inplace=True)
    self.logger.log("Dropping REFUSED transaction {}".format(crt_size - self.df.shape[0]))


  def _drop_and_fix_columns(self):

    self.logger.log("Drop txid and bookingdate")
    self.df.drop(["txid", "bookingdate"], inplace = True, axis = 1)

    self.logger.log("Replace cvcresponsecode > 3 with 3")
    self.df.loc[self.df['cvcresponsecode'] > 3, 'cvcresponsecode'] = 3


  def _convert_dtypes(self):

    self.logger.log("Convert datatypes for numeric, timestamps and categorical")
    self.df['creationdate'] = pd.to_datetime(self.df['creationdate'])
    self.df = self.df.infer_objects()

    self.df['bin'] = pd.Categorical(self.df.bin).codes
    self.df['mail_id'] = pd.Categorical(self.df.mail_id).codes
    self.df['card_id'] = pd.Categorical(self.df.card_id).codes
    self.df['ip_id'] = pd.Categorical(self.df.ip_id).codes
    self.df['accountcode'] = pd.Categorical(self.df.accountcode).codes
    self.df['cardverificationcodesupplied'] = self.df['cardverificationcodesupplied'].astype(int)
    self.df['shopperinteraction'] = pd.Categorical(self.df.shopperinteraction).codes
    self.df['shoppercountrycode'] = pd.Categorical(self.df.shoppercountrycode).codes
    self.df['currencycode'] = pd.Categorical(self.df.currencycode).codes
    self.df['txvariantcode'] = pd.Categorical(self.df.txvariantcode).codes
    self.df['issuercountrycode'] = pd.Categorical(self.df.txvariantcode).codes

    self.logger.log("Change simple_journal to label and binarize column")
    self.df.replace({'simple_journal': {"Settled": 0, "Chargeback": 1}}, inplace = True)
    self.df.rename(columns = {'simple_journal': 'label'}, inplace = True)


  def _sort_after_timestamp(self):
    
    self.logger.log("Sort after creationdate")
    self.df.sort_values('creationdate', inplace = True)
    self.df.reset_index(drop = True, inplace = True)


  def _convert_to_unique_currency(self):

    self.conversion = {'AUD': 0.699165, 'GBP': 1.31061, 'MXN': 0.222776586,
                       'NZD': 0.66152, 'SEK': 0.104405}
    self.logger.log("Convert all amounts in USD using rates: {}".format(self.conversion))
    self.df['amount'] = self.df.apply(
      lambda e: int(math.floor(e['amount'] * self.conversion[e['currencycode']])) , axis=1)
    self.logger.log("Done converting", show_time = True)


  def _rearrange_columns(self):

    self.columns = ["creationdate", "card_id", "mail_id", "ip_id", "issuercountrycode", 
                    "txvariantcode", "bin", "shoppercountrycode", "shopperinteraction",
                    "cardverificationcodesupplied", "cvcresponsecode", "accountcode", "amount",
                    "currencycode", "label"]
    self.logger.log("Rearrange columns to order {}".format(self.columns))
    self.df = self.df[self.columns]


  def _extract_additional_features(self):

    self.logger.log("Start extracting additional features")
    self.additional_feats_df = extract_features_from_data(self.df)
    self.logger.log("Finished extracting additional features", show_time = True)


  def _create_full_dataset(self):

    return pd.concat([self.df, self.additional_feats_df], axis = 1)


  def get_preprocessed_data(self, normalize = False):
    
    self._drop_nans()
    self._drop_refused_transactions()
    self._drop_and_fix_columns()
    self._convert_to_unique_currency()
    self._convert_dtypes()
    self._sort_after_timestamp()
    self._rearrange_columns()
    self._extract_additional_features()

    self.full_df = self._create_full_dataset()

    rand_idx = randint(0, self.full_df.shape[0])
    self.logger.log("Dataset after preproc and adding additional feats" + os.linesep + "{}".format(
      self.full_df.iloc[rand_idx : rand_idx + 5, :]))

    self.logger.log("Drop timestamp columns")
    self.full_df.drop(["creationdate"], inplace = True, axis = 1)

    X = self.full_df.loc[:, self.full_df.columns != 'label'].values
    y = self.full_df['label'].values

    if normalize:
      self.min_max_scaler = preprocessing.MinMaxScaler()
      X = min_max_scaler.fit_transform(X)

    return X, y