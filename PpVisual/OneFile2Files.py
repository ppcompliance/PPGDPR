import pandas as pd
import os
from sklearn.metrics import f1_score
from decimal import getcontext, Decimal

Alldatapath = "./predictresult/predict_result.tsv"


OldMinfilename = "OldOld"
Alldata = pd.read_csv(Alldatapath, sep='\t', encoding='ISO-8859-1')
num = 0
# minfile = open('./testfiles/' + Minfilename.replace(".txt", "") + ".tsv", 'w', encoding="utf-8")
for index in range(0, len(Alldata.review)):
    Minfilename = Alldata.document[index]

    if Minfilename != OldMinfilename:       #a new file
        minfile = open('./resultfiles/' + Minfilename.replace(".txt", "") + ".tsv", 'w', encoding="utf-8")
        minfile.writelines("labelpredict\tlabelreal\treview\n")
        num = 0
    minfile.writelines(str(Alldata.labelpredict[index]) + "\t" + str(Alldata.labelreal[index]) + "\t" + Alldata.review[index] + "\n" )
    num += 1
    OldMinfilename = Minfilename

for resuroot, resudirs, resufiles in os.walk("./resultfiles/"):
    for file_j in resufiles:
        resultfile = pd.read_csv("./resultfiles/" + file_j, sep='\t', encoding='ISO-8859-1')
        test_report_macro_f1 = f1_score(resultfile.labelreal, resultfile.labelpredict, average='micro')
        f1dec = Decimal(test_report_macro_f1)
        print((f1dec*Decimal(100)).quantize(Decimal('0.00')))