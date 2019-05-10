from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import StratifiedKFold

from imblearn.over_sampling import SMOTE

import numpy as np
import json

from hyperparam_tunning import HyperparamGridSearcher
from plot_utils import create_roc_plot

class CrossValidation():

  def __init__(self, data, k_folds, random_seed, logger):
    self.logger = logger
    self.data = data
    self.X, self.y = self.data['X'], self.data['y']
    self.k_folds = k_folds
    self.random_seed = random_seed

  def evaluate_model(self, model, model_hyperparams_grid = None, model_hyperparams_file = None,
    use_smote = True):

    self.logger.log("Start {}-fold cross validation on {} entries".format(
      self.k_folds, self.data['y'].shape[0]))

    strat_kfold = StratifiedKFold(n_splits= self.k_folds, shuffle=False, 
      random_state = self.random_seed)

    acc_list, prec_list, rec_list, confmat_list = [[] for _ in range(4)]
    for fold_idx, (train_idx, test_idx) in enumerate(strat_kfold.split(self.X, self.y)):
      crt_X_train, crt_X_test = self.X[train_idx], self.X[test_idx]
      crt_y_train, crt_y_test = self.y[train_idx], self.y[test_idx]

      if use_smote:
        self.logger.log("Using SMOTE")
        sm = SMOTE(random_state = 13)
        crt_X_train, crt_y_train = sm.fit_sample(crt_X_train, crt_y_train.ravel())

      if model_hyperparams_grid:
        valid_data = {'X': crt_X_train, 'y': crt_y_train}
        grid_searcher = HyperparamGridSearcher(valid_data, self.logger)
        hyperparams = grid_searcher.rand_grid_search(model, model_hyperparams_grid, 50)
      else:
        with open(self.logger.get_model_file(model_hyperparams_file)) as fp:
          hyperparams = json.load(fp)

      model.set_params(**hyperparams)

      model.fit(crt_X_train, crt_y_train)

      plt_title = type(model).__name__ + " " + ("with " if use_smote else "without ") + "SMOTE"
      plt_title += " fold {}".format(fold_idx)
      filename = "roc_" + ("withS_" if use_smote else "withoutS_") + str(fold_idx)
      filename += ".jpg"
      create_roc_plot(plt_title, model.predict_proba(crt_X_test), crt_y_test, filename, 
        self.logger)

      y_pred = model.predict_proba(crt_X_test)
      y_pred = y_pred[:, 1]
      y_pred = y_pred > 0.6

      tn, fp, fn, tp = confusion_matrix(crt_y_test, y_pred).ravel()
      acc_list.append(accuracy_score(crt_y_test, y_pred))
      prec_list.append(precision_score(crt_y_test, y_pred))
      rec_list.append(recall_score(crt_y_test, y_pred))
      confmat_list.append([tn, fp, fn, tp])

      self.logger.log("TN: {}, FP: {}, FN: {}, TP: {} at fold#{}".format(tn, fp, fn, tp, fold_idx))
      self.logger.log("Accuracy at fold#{}: {:.2f}".format(fold_idx, acc_list[-1]))
      self.logger.log("Precision at fold#{}: {:.2f}".format(fold_idx, prec_list[-1]))
      self.logger.log("Recall at fold#{}: {:.2f}".format(fold_idx, rec_list[-1]))
      #self.logger.log("False positives at fold#{}: {:.2f}".format(fold_idx, fp_list[-1]))

    self.logger.log("Finished cross validation", show_time = True)
    self.logger.log("Mean accuracy: {}".format(np.average(acc_list)))
    self.logger.log("Mean precision: {}".format(np.average(prec_list)))
    self.logger.log("Mean recall: {}".format(np.average(rec_list)))
    self.logger.log("Mean FP: {}".format(np.average([e[1] for e in confmat_list])))
    self.logger.log("Mean TP: {}".format(np.average([e[3] for e in confmat_list])))
    self.logger.log("Total FP: {}".format(sum([e[1] for e in confmat_list])))
    self.logger.log("Total TP: {}".format(sum([e[3] for e in confmat_list])))
