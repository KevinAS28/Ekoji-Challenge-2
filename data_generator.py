import pandas as pd
import random
import datetime as dt
import copy
import pandas as pd

name_list = list(pd.read_csv("name_list.csv")["Name"])

hours_per_day = 8
days_in_week = 6

#jumlah dari late, over_hours, benar
profile0 = [3, 4, 5]
profile1 = [0, 0, 100]

profile = profile1

mulai_pengajaran = dt.datetime(year=2020, month=9, day=21) #senin
file_name = "tbl0.csv"

#create db structure
data_dict = {"nama": [], "waktu_dftr": [], "jam": []}
semua_hari = "senin selasa rabu kamis jumat sabtu".split(" ")
for hari in semua_hari:
    data_dict[hari] = []
print(data_dict)

print("\nlate:")
#generate late data
for i in range(0, profile[0]):
    name = random.choice(name_list)+str(i)
    data_dict["nama"].append(name)

    hour = random.randrange(1, 4)
    data_dict["jam"].append(hour)

    daftar = dt.datetime(year=mulai_pengajaran.year, month=mulai_pengajaran.month, day=mulai_pengajaran.day+i)
    data_dict["waktu_dftr"].append(daftar)

    jumlah_hari = random.randrange(0, 7)
    days = copy.deepcopy(semua_hari)
    hari_terpilih = []
    for a in range(jumlah_hari):
        hari_index = random.randrange(1, len(days))
        hari = days[hari_index]
        data_dict[hari].append(1)
        hari_terpilih.append(hari)
        del days[hari_index]

    for day in days:
        data_dict[day].append(0)

    print("nama:", name, "jam:", hour, "waktu:", daftar, "hari:", hari_terpilih)
print("\n\n")


#overhours
print("overhours:")
for i in range(profile[0], profile[1]):
    name = random.choice(name_list)+str(i)
    data_dict["nama"].append(name)

    hour = 3+i
    data_dict["jam"].append(hour)

    daftar = dt.datetime(year=mulai_pengajaran.year, month=mulai_pengajaran.month, day=mulai_pengajaran.day-i-1)
    data_dict["waktu_dftr"].append(daftar)

    jumlah_hari = random.randrange(1, 7)
    days = copy.deepcopy(semua_hari)
    hari_terpilih = []
    for a in range(jumlah_hari):
        hari_index = random.randrange(0, len(days))
        hari = days[hari_index]
        data_dict[hari].append(1)
        hari_terpilih.append(hari)
        del days[hari_index]

    for day in days:
        data_dict[day].append(0)

    print("nama:", name, "jam:", hour, "waktu:", daftar, "hari:", hari_terpilih)
print("\n\n")

#right
print("right:")
for i in range(profile[1], profile[2]):
    name = random.choice(name_list)+str(i)
    data_dict["nama"].append(name)

    hour = random.randrange(1,4)
    data_dict["jam"].append(hour)

    daftar = dt.datetime(year=mulai_pengajaran.year, month=mulai_pengajaran.month, day=mulai_pengajaran.day- (random.randrange(0, 10)))
    data_dict["waktu_dftr"].append(daftar)

    jumlah_hari = random.randrange(1, 7)
    days = copy.deepcopy(semua_hari)
    hari_terpilih = []
    for a in range(jumlah_hari):
        hari_index = random.randrange(0, len(days))
        hari = days[hari_index]
        data_dict[hari].append(1)
        hari_terpilih.append(hari)
        del days[hari_index]
    
    for day in days:
        data_dict[day].append(0)
    
    print("nama:", name, "jam:", hour, "waktu:", daftar, "hari:", hari_terpilih)
print("\n\n")




# for key in list(data_dict.keys()):
#     print(key, len(data_dict[key]))

df_data = pd.DataFrame(data_dict)
df_data.to_csv(file_name)