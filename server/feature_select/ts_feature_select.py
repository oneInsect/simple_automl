"""
CreateTime    : 2019/6/3 19:43
Author        : X
Filename      : ts_feature_select.py
"""
from tsfresh.feature_selection import select_features


def feature_selector(X, y, ml_task='auto', n_jobs=0):
    """
    Calculate the relevance table for the features contained in feature matrix `X` with respect to target vector `y`.
    The relevance table is calculated for the intended machine learning task `ml_task`.

    To accomplish this for each feature from the input pandas.DataFrame an univariate feature significance test
    is conducted. Those tests generate p values that are then evaluated by the Benjamini Hochberg procedure to
    decide which features to keep and which to delete.
    :param X: Feature matrix in the format mentioned before which will be reduced to only the relevant features.
              It can contain both binary or real-valued features at the same time.
    :param y: Target vector which is needed to test which features are relevant. Can be binary or real-valued.
    :param ml_task: The intended machine learning task. Either `'classification'`, `'regression'` or `'auto'`.
                    Defaults to `'auto'`, meaning the intended task is inferred from `y`.
                    If `y` has a boolean, integer or object dtype, the task is assumend to be classification,
                    else regression.
    :param n_jobs: Number of processes to use during the p-value calculation
    :return:  A pandas.DataFrame with each column of the input DataFrame X as index with information on the significance
             of this particular feature. The DataFrame has the columns
             "Feature",
             "type" (binary, real or const),
             "p_value" (the significance of this feature as a p-value, lower means more significant)
             "relevant" (True if the Benjamini Hochberg procedure rejected the null hypothesis [the feature is
             not relevant] for this feature)
    """
    return select_features(X, y, ml_task=ml_task, n_jobs=n_jobs)
