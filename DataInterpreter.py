import os
import pandas as pd

INPUT_FOLDER = 'input'

## Put all your CSVs into INPUT_FOLDER then run this script! :^)
for filename in os.listdir(INPUT_FOLDER):
    labels = ["TEMPURA", "SASHIMI", "DUMPLING", "MAKI_1", "MAKI_2", "MAKI_3", "SALMON_N", "SQUID_N", "EGG_N", "WASABI", "points_per_card", "placement"]
    data = pd.read_csv(INPUT_FOLDER + '/' + filename, names=labels)
    print('---------------------------------------')
    print(filename)
    for column in data:
        print(column)
        print(data[column].sum())