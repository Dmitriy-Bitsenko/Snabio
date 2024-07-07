import pandas as pd


df = pd.read_csv(r"C:\Users\Dmitriy\YandexDisk\SNABIO\niipav\info_niipav.csv")

df.to_excel("info_niipav.xlsx", index=False)
