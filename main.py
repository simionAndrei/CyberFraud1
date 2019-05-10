from data_preproc import DataPreprocessor
from cross_valid import CrossValidation
from logger import Logger

from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

import numpy as np

def test_xgboost(cross_validator, use_smote):
  
  model = XGBClassifier(n_jobs = -1)

  learning_rate = [0.0001, 0.001, 0.01, 0.05, 0.1, 0.3, 1]
  n_estimators = list(range(100, 150, 10))
  max_depth = list(range(5, 12))
  min_child_weight = list(range(1, 7))
  gamma = [i/10.0 for i in range(0, 7)]
  subsample = [i/10.0 for i in range(6, 11)]
  colsample_bytree = [i/10.0 for i in range(6, 11)]
  reg_alpha = [1e-5, 1e-2, 0.1, 1, 100]
  random_state = [13]

  xgb_hyperparams_grid = {'learning_rate': learning_rate,
                          'n_estimators': n_estimators,
                          'max_depth': max_depth,
                          'min_child_weight': min_child_weight,
                          'gamma': gamma,
                          'subsample': subsample,
                          'colsample_bytree': colsample_bytree,
                          'reg_alpha': reg_alpha,
                          'random_state': random_state}

  cross_validator.evaluate_model(model, model_hyperparams_grid = xgb_hyperparams_grid, 
    use_smote = use_smote)


def test_rand_forest(cross_validator, use_smote):

  model = RandomForestClassifier(n_jobs = -1)

  n_estimators = list(range(10,150,10))
  max_features = ['log2', 'sqrt', None]
  max_depth = list(range(5, 12))
  max_depth.append(None)
  min_samples_split = [2, 5, 10]
  min_samples_leaf = [1, 2, 4, 8]
  bootstrap = [True, False]
  criterion = ["gini", "entropy"]
  random_state = [13]

  randf_hyperparams_grid = {'n_estimators': n_estimators,
                            'max_features': max_features,
                            'max_depth': max_depth,
                            'min_samples_split': min_samples_split,
                            'min_samples_leaf': min_samples_leaf,
                            'bootstrap': bootstrap,
                            'criterion': criterion,
                            'random_state': random_state}

  model_hyperparams_file = 'RandomForestClassifier_params_2019-05-10_19_05_57.json'
  cross_validator.evaluate_model(model, model_hyperparams_file = model_hyperparams_file, 
    use_smote = use_smote)


def test_logistic_regression(cross_validator, use_smote):

  model = LogisticRegression()

  logreg_hyperparams_grid  = {'C' : np.linspace(1, 10, 10)}
  cross_validator.evaluate_model(model, model_hyperparams_grid = logreg_hyperparams_grid, 
    use_smote = use_smote)

if __name__ == '__main__':


  logger = Logger(show = True, html_output = True, config_file = "config.txt")
  transact_preprocessor = DataPreprocessor(logger)

  X, y = transact_preprocessor.get_preprocessed_data(normalize = True)
  data = {'X': X, 'y': y}

  cross_validator = CrossValidation(data = data, k_folds = 10, random_seed = 13,
   logger = logger)

  #test_logistic_regression(cross_validator, use_smote = False)
  #test_randf_forest(cross_validator, use_smote = False)
  test_xgboost(cross_validator, use_smote = True)