import datetime
from datetime import timedelta
import pandas as pd
import random
from faker import Faker
from itertools import product
import csv

# the order of generation:
# 1. Car_types
# 2. Cars
# 3. Parts CSV
# 4. Clients
# 5. Agents, Assessors
# 6. Ownership
# 7. Insurances
# 8. Claims

# random seed, faker, and constants
random.seed(1)
f = Faker(['pl_PL'])
f.seed_instance(0)

NUMBER_OF_CARS = 100000
# NUMBER_OF_CLIENTS = 10; number of clients depends on the number of cars with unique VIN and Registration_ID
NUMBER_OF_AGENTS = 2500
NUMBER_OF_ASSESSORS = 2500
NUMBER_OF_INSURANCES = 500000
NUMBER_OF_CLAIMS = 1000000
PRODUCTION_YEAR_START = 1975
PRODUCTION_YEAR_END = 2020
MILEAGE_MIN = 0
MILEAGE_MAX = 65000
PRICE_MIN = 750
PRICE_MAX = 3640
GARAGE_FREQ = 1 / 3

BIRTHDAY_START = datetime.date(1963, 1, 1)
SALE_START = datetime.date(1993, 1, 1)
SUBMISSION_START = datetime.date(1993, 5, 1)
BIRTH_DELTA = 30
LICENSE_DELTA = 30
SALE_DELTA = 25
SUBMISSION_DELTA = 28
EVALUATION_DELTA = 14

# generate Car_types ###################################################################################################

# variables with all possible values
car_class = ['cheap', 'medium', 'premium']
car_size = ['small', 'medium', 'large', 'cargo']
car_production_year = list(range(PRODUCTION_YEAR_START, PRODUCTION_YEAR_END))

# create a data frame
# product() is responsible for generating all possible combinations
car_types = pd.DataFrame(list(product(car_class, car_size, car_production_year)),
                         columns=['Class', 'Size', 'Production_year'])

# shift indices so the first index equals 1 not 0
car_types.index += 1

# save the data frame to the csv file
car_types.to_csv('car_types.csv', index_label='ID')
print('car_types ready!')


# generate Cars ########################################################################################################

# define functions generating VIN, Registration_ID, Colour, Car_type, and Engine_capacity
def generate_vin():
    letters = 'ABCDEFGHJKLMNPRSTUVWXYZ'
    digits = '0123456789'
    letters_and_digits = 'ABCDEFGHJKLMNPRSTUVWXYZ0123456789'
    vin = ''

    for e in range(2):
        vin += random.choice(letters)

    vin += random.choice(digits)

    for e in range(5):
        vin += random.choice(letters_and_digits)

    vin += random.choice(digits)

    for e in range(2):
        vin += random.choice(letters)

    for e in range(6):
        vin += random.choice(digits)

    return vin


def generate_registration_id():
    letters_first = 'BCDEFGKLNOPRSTWZ'
    letters_second = 'ABCDEFGHIJKLMNOPRSTUVWXYZ'
    digits = '0123456789'
    plate = ''

    plate += random.choice(letters_first)
    plate += random.choice(letters_second)

    for d in range(5):
        plate += random.choice(digits)

    return plate


def generate_colour():
    colours = ['black', 'silver', 'gray', 'white', 'red' 'green', 'blue', 'yellow', 'navy', 'lime', 'purple', 'maroon']

    colour = random.choice(colours)

    return colour


def generate_car_type(number_of_car_types):
    return random.randrange(1, number_of_car_types)


def generate_engine_capacity():
    return random.randrange(10, 40) / 10


# create a list
cars_columns = ['ID', 'VIN', 'Registration_ID', 'Car_type_ID', 'Colour', 'Engine_capacity']
ids = []
vin = []
reg = []
car_type_id = []
colours = []
eng = []

# populate the data frame
for i in range(NUMBER_OF_CARS):
    ids.append(i + 1)
    vin.append(generate_vin())
    reg.append(generate_registration_id())
    car_type_id.append(generate_car_type(len(car_types.index) + 1))
    colours.append(generate_colour())
    eng.append(generate_engine_capacity())

print("Lists ready")

# keep only the rows with unique VIN and Registration_ID
#vin = list(dict.fromkeys(vin))
#reg = list(dict.fromkeys(reg))
print("Duplicates dropped")

NUMBER_OF_CLIENTS = len(vin)

# save the list to the csv file
output = list(zip(ids, vin, reg, car_type_id, colours, eng))
print('Final list ready')

# opening the csv file in 'w' mode
file = open('../cars.csv', 'w', encoding='utf-8-sig', newline='')

with file:
    writer = csv.DictWriter(file, fieldnames=cars_columns)

    # writing data row-wise into the csv file
    writer.writeheader()
    write = csv.writer(file)
    write.writerows(output)

# generate Parts #######################################################################################################

# variables with values known upfront
part_names = ['Engine', 'Front_doors', 'Rear_doors',
              'Left_mirror', 'Right_mirror', 'Front_headlights',
              'Rear_headlights', 'Front_bumper', 'Rear_bumper']
car_type_ids = list(range(1, len(car_types.index) + 1))

# create a data frame and add a column 'Value' with the default value = 0
parts = pd.DataFrame(list(product(part_names, car_type_ids)),
                     columns=['Part', 'Car_type_ID'])
parts['Value'] = 0


# define function for generating value of a part
def generate_value(part, car_type_id):
    # the value is estimated with a function:
    # value = initial_value * class_parameter * size_parameter * (1 - (car_age / 50))
    # where:
    #   initial_values are:
    #        30 000 engine
    #        10 000 front doors
    #         8 000 rear doors
    #         1 000 left/right mirror
    #           500 front headlights
    #           700 rear headlights
    #         1 500 front bumper
    #         2 000 rear bumper
    #   class_parameters are:
    #        1.0 cheap
    #        1.5 medium
    #        2.5 premium
    #   size_parameters are:
    #        1.0 small
    #        1.2 medium
    #        1.7 large
    #        2.0 cargo
    #   car_age = 2023 - production_years

    # set initial_value
    initial_value = 0

    if part == 'Engine':
        initial_value = 30000
    elif part == 'Front_doors':
        initial_value = 10000
    elif part == 'Rear_doors':
        initial_value = 8000
    elif part == 'Left_mirror':
        initial_value = 1000
    elif part == 'Right_mirror':
        initial_value = 1000
    elif part == 'Front_headlights':
        initial_value = 500
    elif part == 'Rear_headlights':
        initial_value = 700
    elif part == 'Front_bumper':
        initial_value = 1500
    elif part == 'Rear_bumper':
        initial_value = 2000

    # the car_type_id is decreased as index of data frame starts from 0 and index of car types start from 1
    car_type_id = car_type_id - 1

    # default parameters for cheap and small cars
    class_parameter = 1
    size_parameter = 1

    # calculate age parameter
    car_age = 2023 - car_types.iloc[car_type_id]['Production_year']
    age_parameter = (1 - (car_age / 50))

    # adjust class and size parameters if needed
    if car_types.iloc[car_type_id]['Class'] == 'medium':
        class_parameter = 1.5
    elif car_types.iloc[car_type_id]['Class'] == 'premium':
        class_parameter = 2.5

    if car_types.iloc[car_type_id]['Size'] == 'medium':
        class_parameter = 1.2
    elif car_types.iloc[car_type_id]['Size'] == 'large':
        class_parameter = 1.7
    elif car_types.iloc[car_type_id]['Size'] == 'cargo':
        class_parameter = 2

    # calculate part value
    value = initial_value * class_parameter * size_parameter * age_parameter
    return round(value, 2)


# calculate a value of a given part; Parts (0: Part, 1: Car_type_ID, 2: Value)
for i in range(0, len(parts)):
    parts.iloc[i, 2] = generate_value(parts.iloc[i, 0], parts.iloc[i, 1])

# save the data frame to the csv file
parts.to_csv('parts.csv', index=False)
print('parts ready!')


# generate Clients #####################################################################################################

# a proper PESESL based on date and sex, https://gist.github.com/anonymous/cade4cca984b733d5c30
def pesel(bd, sex):
    year = bd.year
    month = bd.month
    day = bd.day

    if year >= 2000:
        month = month + 20  # to distinguish between centuries

    four_random = str(random.randint(1000, 9999))
    if sex == 'M':  # 1
        four_random = four_random[:-1] + '1'
    else:  # F - 0
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

    # quick fix of lack of zeros in year, month, and day; can be improved later
    year_s = str(year % 100)
    if year >= 2000:
        year_s = '0' + year_s

    month_s = str(month)
    if month < 10:
        month_s = '0' + month_s

    day_s = str(day)
    if day < 10:
        day_s = '0' + day_s

    return (year_s + month_s + day_s + four_random + str(last_digit))


# create lists
client_columns = ['ID', 'PESEL', 'Name1', 'Name2', 'Surname', 'Sex',
                  'Date_of_birth', 'Voivodeship', 'City', 'Street_and_number',
                  'Account_nb', 'License_issuing_date']
pesels = []
names1 = []
names2 = []
surnames = []
sexes = []
birth_dates = []
vois = []
cities = []
streets = []
accs = []
lics = []
ids = []
# populate the lists
for i in range(NUMBER_OF_CLIENTS):
    ids.append(i + 1)

    # date of birth
    birth = BIRTHDAY_START + datetime.timedelta(weeks=52 * random.randint(1, BIRTH_DELTA), days=random.randint(1, 30))

    # license issuing day
    license_delta = random.randint(52 * 18, 52 * LICENSE_DELTA)
    license_date = birth + datetime.timedelta(weeks=license_delta)

    birth_dates.append(birth.isoformat())
    lics.append(license_date.isoformat())
    vois.append(f.administrative_unit())
    cities.append(f.city())
    streets.append(f.street_address())
    accs.append(f.iban())
    # insert
    if i % 2 == 0:
        # a male
        pesels.append(pesel(birth, 'M'))
        names1.append(f.first_name_male())
        names2.append(f.first_name_male())
        surnames.append(f.last_name_male())
        sexes.append('M')
    else:
        # a female
        pesels.append(pesel(birth, 'F'))
        names1.append(f.first_name_female())
        names2.append(f.first_name_female())
        surnames.append(f.last_name_female())
        sexes.append('F')

# keep only the rows with unique PESEL; errare humanum est, ale tkwic w bledzie to rzecz diabelska
pesels = list(dict.fromkeys(pesels))
print("Clients Duplicates dropped")

# save the list to the csv file
output = list(zip(ids, pesels, names1, names2, surnames, sexes, birth_dates, vois, cities, streets, accs, lics))
print('Final list ready')

# opening the csv file in 'w' mode
file = open('../clients.csv', 'w', encoding='utf-8-sig', newline='')

with file:
    writer = csv.DictWriter(file, fieldnames=client_columns)

    # writing data row-wise into the csv file
    writer.writeheader()
    write = csv.writer(file)
    write.writerows(output)
print('clients ready!')

NUMBER_OF_CLIENTS = len(pesels)

# generate Agents ###################################################################################################

# create a data frame
agents = pd.DataFrame(columns=['ID', 'Name', 'Surname', 'Voivodeship'])

# populate the data frame
for i in range(NUMBER_OF_AGENTS):
    agents.loc[i] = [i + 1, f.first_name(), f.last_name(), f.administrative_unit()]

# save the data frame to the csv file
agents.to_csv('agents.csv', index=False)
print('agents ready!')


# generate Assessors ###################################################################################################

def generate_specialisation():
    return random.choice(["cargo", "casual", "premium"])


# create a data frame
assessors = pd.DataFrame(columns=['ID', 'Name', 'Surname', 'Specialisation'])

# populate the data frame
for i in range(NUMBER_OF_ASSESSORS):
    assessors.loc[i] = [i + 1, f.first_name(), f.last_name(), generate_specialisation()]

# save the data frame to the csv file
assessors.to_csv('assessors.csv', index=False)
print('assessors ready!')

# generate Ownership ###################################################################################################

client_ids = list(range(1, NUMBER_OF_CLIENTS))
car_ids = list(range(1, NUMBER_OF_CARS))

# save the list to the csv file
output = list(zip(client_ids, car_ids))
print('Final list ready')

# opening the csv file in 'w' mode
file = open('ownership.csv', 'w', encoding='utf-8-sig', newline='')

with file:
    writer = csv.DictWriter(file, fieldnames=['Client_ID', 'Car_ID'])

    # writing data row-wise into the csv file
    writer.writeheader()
    write = csv.writer(file)
    write.writerows(output)
print('ownership ready!')


# generate Insurances ##################################################################################################

def generate_garage():
    if GARAGE_FREQ > random.uniform(0, 1):
        # kept in a garage
        garage = 1
    else:
        garage = 0
    return garage


def generate_mileage():
    return random.randint(MILEAGE_MIN, MILEAGE_MAX)


def generate_price():
    return random.randint(PRICE_MIN, PRICE_MAX)


def generate_agent():
    return random.randint(1, NUMBER_OF_AGENTS)


# create lists
insurance_columns = ['ID', 'Sale_date', 'Mileage', 'Garage', 'Price', 'Client_ID', 'Car_ID', 'Agent_ID']
ids = []
sales = []
mileages = []
garages = []
prices = []
car_ids = []
client_ids = []
agent_ids = []
carID = 0
clientID = 0

for i in range(NUMBER_OF_INSURANCES):
    ids.append(i + 1)

    carID = carID + 1
    if (carID > NUMBER_OF_CARS):
        carID = random.randint(1, NUMBER_OF_CARS)

    clientID = clientID + 1
    if (clientID > NUMBER_OF_CLIENTS):
        clientID = random.randint(1, NUMBER_OF_CLIENTS)

    # insurance sale date
    sale_date = SALE_START + datetime.timedelta(weeks=52 * random.randint(1, SALE_DELTA), days=random.randint(1, 30))

    # insert
    sales.append(sale_date)
    mileages.append(generate_mileage())
    garages.append(generate_garage())
    prices.append(generate_price())
    client_ids.append(clientID)
    car_ids.append(carID)
    agent_ids.append(generate_agent())

# save the list to the csv file
output = list(zip(ids, sales, mileages, garages, prices, client_ids, car_ids, agent_ids))
print('Final list ready')

# opening the csv file in 'w' mode
file = open('../insurances.csv', 'w', encoding='utf-8-sig', newline='')

with file:
    writer = csv.DictWriter(file, fieldnames=insurance_columns)

    # writing data row-wise into the csv file
    writer.writeheader()
    write = csv.writer(file)
    write.writerows(output)
print('insurances ready!')

# generate Claims ##################################################################################################

submission = []
parking = []
assessor = []
delta = []
evaluation = []
engine = []
fd = []
rd = []
lm = []
rm = []
fh = []
rh = []
fb = []
rb = []
ids = []
insurance = list(range(1, NUMBER_OF_INSURANCES + 1))

for i in range(NUMBER_OF_CLAIMS):
    ids.append(i + 1)

    # submission date
    sub = SUBMISSION_START + datetime.timedelta(weeks=52 * random.randint(0, SUBMISSION_DELTA),
                                                days=random.randint(1, 30))
    submission.append(sub)

    # evaluation date
    eval_delta = random.randint(1, 14)
    eval = sub + datetime.timedelta(days=eval_delta)
    evaluation.append(eval)

    parking.append(random.choice([0, 1]))
    assessor.append(random.randint(1, NUMBER_OF_ASSESSORS))
    engine.append(random.choice([0, 1, 2]))
    fd.append(random.choice([0, 1, 2]))
    rd.append(random.choice([0, 1, 2]))
    lm.append(random.choice([0, 1, 2]))
    rm.append(random.choice([0, 1, 2]))
    fh.append(random.choice([0, 1, 2]))
    rh.append(random.choice([0, 1, 2]))
    fb.append(random.choice([0, 1, 2]))
    rb.append(random.choice([0, 1, 2]))

    if (i >= NUMBER_OF_INSURANCES):
        insurance.append(random.randint(1, NUMBER_OF_INSURANCES))

output = list(zip(ids, submission, parking, assessor, evaluation,
                  engine, fd, rd, lm, rm, fh, rh, fb, rb, insurance))
print('List ready')
# opening the csv file in 'w' mode
file = open('../claims.csv', 'w', encoding='utf-8-sig', newline='')

with file:
    # identifying header
    header = ['ID', 'Submission_date', 'Parking_place',
              'Assessor_ID', 'Evaluation_date',
              'Engine', 'Front_doors', 'Rear_doors',
              'Left_mirror', 'Right_mirror', 'Front_headlights',
              'Rear_headlights', 'Front_bumper', 'Rear_bumper', 'Insurance_ID']
    writer = csv.DictWriter(file, fieldnames=header)

    # writing data row-wise into the csv file
    writer.writeheader()
    write = csv.writer(file)
    write.writerows(output)