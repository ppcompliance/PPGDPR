import numpy as np
from sklearn.metrics import f1_score, precision_score, recall_score


def get_score(y_ture, y_pred):
    y_ture = np.array(y_ture)
    y_pred = np.array(y_pred)
    f1 = f1_score(y_ture, y_pred, average='macro') * 100
    p = precision_score(y_ture, y_pred, average='macro') * 100
    r = recall_score(y_ture, y_pred, average='macro') * 100

    y_ture_0 = np.where(y_ture == 0, 1, 0)
    y_pred_0 = np.where(y_pred == 0, 1, 0)
    p_0 = precision_score(y_ture_0, y_pred_0) * 100
    r_0 = recall_score(y_ture_0, y_pred_0) * 100
    f1_0 = f1_score(y_ture_0, y_pred_0) * 100

    p_no_0, r_no_0, f1_no_0 = get_no_0_score(p, p_0), get_no_0_score(r, r_0), get_no_0_score(f1, f1_0)

    return str((reformat(p, 2), reformat(r, 2), reformat(f1, 2))), str((p_no_0, r_no_0, f1_no_0)), f1_no_0


def get_no_0_score(score, score_0):
    return reformat((score * 11 - score_0) / 10, 2)


def reformat(num, n):
    return float(format(num, '0.' + str(n) + 'f'))
