import numpy as np
import pandas as pd
import re
import os
from bs4 import BeautifulSoup
import sys
from decimal import getcontext, Decimal

steplen = 5
maxlen = 100


data_result = pd.read_csv('./predictresult/predict_result.tsv', encoding='ISO-8859-1', sep='\t', delimiter="\t")
data_plot = open("LSTM_plot.tsv", 'w', encoding="utf-8")
data_plot.writelines("len\tF\n")

for step in range(int(maxlen/steplen)):
    labelpredict = []
    labelreal = []
    DataOfThisStep = 0
    predictnum = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]  # 11
    predictandrealnum = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]  # 11
    realnum = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]  # 11

    print()
    for idx in range(data_result.labelpredict.shape[0]):
        if len(data_result.review[idx].split()) > step*steplen and len(data_result.review[idx].split()) <= (step+1)*steplen:
            labelpredict.append(data_result.labelpredict[idx])
            labelreal.append(data_result.labelreal[idx])
            DataOfThisStep += 1

    allpredictandrealnum = Decimal(0)
    allpredictnum = Decimal(0)
    allrealnum = Decimal(0)
    # allprecision = Decimal(0)
    # allrecall = Decimal(0)
    for labelnum in range(0, 11):
        for num in range(0, len(labelpredict)):
            if str(labelpredict[num]) == str(labelnum):
                predictnum[labelnum] = predictnum[labelnum] + 1
                if str(labelreal[num]) == str(labelnum):  # two label equal simultaneously
                    predictandrealnum[labelnum] = predictandrealnum[labelnum] + 1
        for num in range(0, len(labelpredict)):
            if str(labelreal[num]) == str(labelnum):
                realnum[labelnum] = realnum[labelnum] + 1

        allpredictandrealnum += predictandrealnum[labelnum]
        allpredictnum += predictnum[labelnum]
        allrealnum += realnum[labelnum]

    if allpredictnum != 0 and allrealnum != 0:
        p = Decimal(allpredictandrealnum / allpredictnum)
        r = Decimal(allpredictandrealnum / allrealnum)
        if p != 0 and r != 0:
            micro_f = (Decimal(Decimal(2) * (p * r) / (p + r)) * Decimal(100)).quantize(Decimal('0.00'))
        else:
            micro_f = 0
    else:
        p = 0
        r = 0
        micro_f = 0


    data_plot.writelines(str(step*steplen) + "\t" + str(micro_f) + "\n")
    # data_plot.writelines(str(step*steplen) + "\t" + str(micro_f) + "\t" + str(DataOfThisStep) + "\n")
