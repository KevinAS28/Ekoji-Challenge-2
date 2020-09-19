import pandas as pd
import random
import datetime as dt

mulai_pengajaran = dt.datetime(year=2020, month=9, day=21) #senin

df = pd.read_csv("tbl0.csv")


jam_unique = list(df["jam"].unique())

#pendaftaran ditutup saat total jam pengajar mencapai 60|61|62
#maka, sort database dengan waktu, ambil data dari awal hingga jam nya 60|61|62 sort
df.sort_values("waktu_dftr", inplace=True)
df["cumsum"] = df["jam"].cumsum()

limit_hours = [60, 61, 62]
from_limits = [df.where((df["cumsum"]==i)).dropna().to_dict() for i in limit_hours]


print(from_limits)

