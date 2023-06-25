from faker import Faker
import pandas as pd
from datetime import timedelta
import random

# ten Faker rozwiązuje prawie całą rzecz!
f = Faker(["pl_PL"]) # "en-GB"

ids = []
names1 = []
names2 = []
surnames = []
sexes = []
birthds = []
pesels = []
vois = []
cities = []
streets = []
accs = []
lics = []

# https://gist.github.com/anonymous/cade4cca984b733d5c30
def pesel(bd, sex):
    year = bd.year
    month = bd.month
    day = bd.day

    if year >= 2000:
        month = month + 20 # to distinguish between centuries
        
    four_random = random.randint(1000,9999)
    four_random = str(four_random)
    if sex == 'M': #1
        four_random = four_random[:-1] + '1'
    else: #F - 0
        four_random = four_random[:-1] + '0'

    # here comes the equation part, it calculates the last digit
    y = '%02d' % (year % 100)
    m = '%02d' % month
    dd = '%02d' % day
        
    a = y[0]
    a = int(a)

    b = y[1]
    b = int(b)

    c = m[0]
    c = int(c)

    d = m[1]
    d = int(d)

    e = dd[0]
    e = int(e)

    f = dd[1]
    f = int(f)

    g = four_random[0]
    g = int(g)

    h = four_random[1]
    h = int(h)

    i = four_random[2]
    i = int(i)

    j = four_random[3]
    j = int(j)

    check = a + 3 * b + 7 * c + 9 * d + e + 3 * f + 7 * g + 9 * h + i + 3 * j

    if check % 10 == 0:
        last_digit = 0
    else:
        last_digit = 10 - (check % 10)

    out = str(year%100)
    out += str(month)
    out += str(day)
    out += four_random
    out += str(last_digit)
    return out

id = 0
for _ in range(50000): # 50000
    # male
    id = id + 1
    name1 = f.first_name_male()
    name2 = f.first_name_male()
    name3 = f.last_name_male()
    sex = 'M'
    birthdate = f.date_of_birth(minimum_age = 18, maximum_age = 90)
    peselq = pesel(birthdate, sex)
    voivodship = f.administrative_unit()
    city = f.city()
    street = f.street_address()
    account = f.iban()
    license = f.date_of_birth(minimum_age = 18, maximum_age = 90)
    while(license - birthdate < timedelta(weeks = 52*18)):
        license = birthdate + timedelta(weeks = 52*18) #f.date_of_birth(minimum_age = 2*18, maximum_age = 90)
    ids.append(id)
    names1.append(name1)
    names2.append(name2)
    surnames.append(name3)
    sexes.append(sex)
    birthds.append(birthdate.isoformat())
    pesels.append(peselq)
    vois.append(voivodship)
    cities.append(city)
    streets.append(street)
    accs.append(account)
    lics.append(license.isoformat())
    # female
    id = id + 1
    name1 = f.first_name_female()
    name2 = f.first_name_female()
    name3 = f.last_name_female()
    sex = 'F'
    birthdate = f.date_of_birth(minimum_age = 18, maximum_age = 90)
    peselq = pesel(birthdate, sex)
    voivodship = f.administrative_unit()
    city = f.city()
    street = f.street_address()
    account = f.iban()
    license = f.date_of_birth(minimum_age = 18, maximum_age = 90)
    while(license - birthdate < timedelta(weeks = 52*18)):
        license = birthdate + timedelta(weeks = 52*18) #f.date_of_birth(minimum_age = 2*18, maximum_age = 90)
    ids.append(id)
    names1.append(name1)
    names2.append(name2)
    surnames.append(name3)
    sexes.append(sex)
    birthds.append(birthdate.isoformat())
    pesels.append(peselq)
    vois.append(voivodship)
    cities.append(city)
    streets.append(street)
    accs.append(account)
    lics.append(license.isoformat())

client = {
    'ID':ids,
    'PESEL':pesels,
    'Name1':names1,
    'Name2':names2,
    'Surname':surnames,
    'Sex':sexes,
    'Date_of_birth':birthds,
    'Voivodeship':vois,
    'City':cities,
    'Street_and_number':streets,
    'Account_nb':accs,
    'License_issuing_date':lics
}

p = 'C:/Users/laptop/Desktop/fakedata.csv'
df = (pd.DataFrame(client, columns = ['ID', 'PESEL', 'Name1', 'Name2', 'Surname', 'Sex', 'Date_of_birth', 'Voivodeship', 'City', 'Street_and_number', 'Account_nb', 'License_issuing_date']))
df.to_csv(p, encoding = 'utf-8', index = False)