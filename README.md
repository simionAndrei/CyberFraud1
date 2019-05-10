# Cyber Fraud assignment 1

This is the repository containing the first assignment of the Cyber 
data analytics course.

## Project structure
The structure of the project is as follows:
* `main.py` - The main entry point in the project. This uses all the necessary components to run the pre-procesing, feature extraction, classificantion and optimization.
* `card_tracker.py` - Contains the class used to store the context associated with each card and calculates the additional features.
* `Exploratory_Analysis.ipynb` - The notebook used for analisys. A saved version of the output can be found under `Exploratory_Analysis.html`.
* `config.txt` - Used for configuration variables. For the moment only the path to the data set is used.
* `cross_valid.py` - Used for the cross-validation algorithm.
* `data_preproc.py` - Used for preprocessing of data(droping + conversions).
* `feats_utils.py` - Utilities. Mainly used for functions to run apply in pandas.
* `hyperparam_tunning.py` - The algorithm used perform random grid search.
* `logger.py` - Logger class.
* `plot_utils.py` - Utilities used to plot the results.
* `data/` - Folder containing the dataset `data_for_student_case.csv`.
* `logs/` - Folder where the logs are stored.
* `models/` - Folder where the parameters for the classifiers are stored.
* `output/` - Folder where the images output.

For a more detailed look check the code comments.
