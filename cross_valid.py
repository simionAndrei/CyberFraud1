from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import StratifiedKFold

from imblearn.over_sampling import SMOTE

import numpy as np

class CrossValidation():

  def __init__(self, data, k_folds, random_seed, logger):
    self.logger = logger
    self.data = data
    self.X, self.y = self.data['X'], self.data['y']
    self.k_folds = k_folds
    self.random_seed = random_seed

  def evaluate_model(self, model, use_smote = True):

    self.logger.log("Start {}-fold cross validation on {} entries".format(
      self.k_folds, self.data['y'].shape[0]))

    strat_kfold = StratifiedKFold(n_splits= self.k_folds, shuffle=False, 
      random_state = self.random_seed)

    acc_list, prec_list, rec_list, confmat_list = [[] for _ in range(4)]
    for fold_idx, (train_idx, test_idx) in enumerate(strat_kfold.split(self.X, self.y)):
      crt_X_train, crt_X_test = self.X[train_idx], self.X[test_idx]
      crt_y_train, crt_y_test = self.y[train_idx], self.y[test_idx]

      if use_smote:
        print("SMOTE")
        sm = SMOTE(random_state = 13)
        crt_X_train, crt_y_train = sm.fit_sample(crt_X_train, crt_y_train.ravel())

      model.fit(crt_X_train, crt_y_train)

      y_pred = model.predict(crt_X_test)

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
