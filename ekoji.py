#!/usr/bin/env python
# coding: utf-8

# In[337]:


import pandas as pd
import random
import datetime as dt


# In[372]:


mulai_pengajaran = dt.datetime(year=2020, month=9, day=21) #senin
df = pd.read_csv("tbl0.csv")
df.index.name = "index"


# # Pendaftaran tutup setelah total jam 60|61|62

# In[373]:


#pendaftaran ditutup saat total jam pengajar mencapai 60|61|62
#maka, sort database dengan waktu, ambil data dari awal hingga jam nya 60|61|62 sort
df = df.sort_values("waktu_dftr")
df = df.reset_index()
df["cumsum"] = df["jam"].cumsum()
limit_hours = [60, 61, 62]
from_limits = [df.where((df["cumsum"]==i)).dropna() for i in limit_hours]

print(df)


# In[374]:


print(df.iloc[21])


# In[375]:


#hapus dari from_limits yang tidak ada datanya
from_limits = [i for i in from_limits if len(i["nama"])!=0]
print(from_limits)


# In[376]:


#ambil yang terbanyak
data_limit = from_limits[-1]
print(data_limit)


# In[377]:


#dapatkan indexnya
index_limit = int(data_limit.index.tolist()[0])
print(index_limit)


# In[378]:


#ambil data dengan slicing 
new_df = df.iloc[0:index_limit+1]
del new_df["index"]
del new_df["Unnamed: 0"]
print(new_df)

new_df.to_csv("temp0.csv")


# # Sedapat mungkin 48 jam dan Sebanyak-banyak mungkin instrukturnya

# In[379]:


all_days = "senin selasa rabu kamis jumat sabtu".split(" ")

df1 = new_df.copy()

#tambahkan kolom jumlah hari mengajar
df1["day_counts"] = df1[all_days].sum(axis=1)
#tambahkan kolom total_hours
df1["total_hours"] = df1["day_counts"]*df1["jam"]
print(df1)


# In[380]:


df2 = df1.sort_values(["total_hours", "day_counts"])
df2.reset_index(inplace=True)
del df2["cumsum"]
del df2["index"]
df2


# In[381]:


#peminat hari2 dengan di sort dari yang paling sedikit peminatnya
dict_peminat_hari = dict()
sum_peminat_hari = [sum(df2[i]) for i in all_days]
index = 0
for day in all_days:
    dict_peminat_hari[day] = sum_peminat_hari[index]
    index+=1
sorted_hari_peminat = sorted(dict_peminat_hari, key=dict_peminat_hari.get)
# print(sorted_hari_peminat)


hari_nama = dict()
for hari in sorted_hari_peminat:
    yg_bs_hari_x = df2[df2[hari]==1]
    yg_bs_hari_x["cumsum_hari_x"] = (yg_bs_hari_x[hari]*yg_bs_hari_x["jam"]).cumsum()
    approach_8 = yg_bs_hari_x.where((yg_bs_hari_x["cumsum_hari_x"]<=8)).dropna()
#     print(approach_8)
    hari_nama[hari] = [list(approach_8["nama"]), list(approach_8["jam"])]
    
print(hari_nama)


# In[382]:


#konfirmasi hasil -> harusnya tiap hari ada approach 8
dict_jamperhari = dict()
for hari in hari_nama:
    jam = 0
    nama_list = hari_nama[hari][0]
    for nama in nama_list:
        jam += (df2[df2["nama"]==nama]["jam"] * df2[df2["nama"]==nama][hari]).tolist()[0]
    dict_jamperhari[hari] = jam

total_jam = sum(list(dict_jamperhari.values()))
print(total_jam)
print(dict_jamperhari)


# # Finishing

# In[383]:


#yang akan kerja minggu depan
yg_kerja_mingdep = []
for hari in hari_nama:
    nama_list = hari_nama[hari][0]
    yg_kerja_mingdep += nama_list
yg_kerja_mingdep = list(set(yg_kerja_mingdep))
print(yg_kerja_mingdep)


# In[402]:


#yang ditunda
all_pendaftar = list(new_df["nama"])
list_tertunda = []
for n0 in all_pendaftar:
    if not (n0 in yg_kerja_mingdep):
        tertunda = new_df[new_df["nama"]==n0]
        list_tertunda.append([tertunda.nama.tolist()[0], tertunda.jam.tolist()[0]])
        
print(list_tertunda)  


# In[410]:


#hasilkan output yang di inginkan
import json
# instruktur_terpilih = json.dumps(hari_nama)
# instruktur_tertunda = json.dumps(list_tertunda)
jadwal = ["{}.00 - {}.00".format(i, i+1) for i in range(8, 16)]
tbl_out = {"Jadwal": jadwal}

for day in all_days:
    tbl_out[day] = []


for hari in hari_nama:
    for i in range(len(hari_nama[hari][0])):
        i = int(i)
        for a in range(int(hari_nama[hari][1][i])):
            a = int(a)
            tbl_out[hari].append(hari_nama[hari][0][i])

            
for hari in all_days:
    tbl_out[hari] += [0]*(len(jadwal)-len(tbl_out[hari]))
    
for key in tbl_out:
    print(key, len(tbl_out[key]))
    
df_out = pd.DataFrame(tbl_out)
json_struct = {"hasil": []}
json_struct["hasil"] = json.loads(df_out.to_json(orient="records"))
with open("hasil.json", "w+") as f:
    json.dump(json_struct, f)

print("\n\nhasil akhir: ")
print(df_out)

# index = 0
# for key in tbl_out:
#     json_struct["hasil"].append()


# In[ ]:




