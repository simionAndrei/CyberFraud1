from data_preproc import DataPreprocessor
from cross_valid import CrossValidation
from logger import Logger

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


if __name__ == '__main__':


  logger = Logger(show = True, html_output = True, config_file = "config.txt")
  transact_preprocessor = DataPreprocessor(logger)

  X, y = transact_preprocessor.get_preprocessed_data(normalize = True)
  data = {'X': X, 'y': y}

  cross_validator = CrossValidation(data = data, k_folds = 10, random_seed = 13,
   logger = logger)

  model = RandomForestClassifier(n_estimators = 250, max_depth = 11, random_state = 13, n_jobs = -1)
  #DecisionTreeClassifier(random_state=0)
  cross_validator.evaluate_model(model)  