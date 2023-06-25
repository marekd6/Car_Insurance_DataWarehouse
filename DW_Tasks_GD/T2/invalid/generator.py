import datetime
from datetime import timedelta
import pandas as pd
import random
from faker import Faker
from itertools import product

# the order of generation:
# 1. Car_types
# 2. Cars
# 3. Parts
# 4. Clients
# 5. Employees
# 6. Insurances
# 7. Claims here

# random seed, faker, and constants
random.seed(1)
f = Faker(['pl_PL'])

NUMBER_OF_CARS = 100000
# NUMBER_OF_CLIENTS = 10; number of clients depends on the number of cars with unique VIN and Registration_ID
NUMBER_OF_EMPLOYEES = 5000
NUMBER_OF_INSURANCES = 100000
NUMBER_OF_CLAIMS = 1000000
PRODUCTION_YEAR_START = 1975
PRODUCTION_YEAR_END = 2023
CLIENT_AGE_MIN = 18
CLIENT_AGE_MAX = 90
LICENSE_MIN = CLIENT_AGE_MIN
LICENSE_MAX = CLIENT_AGE_MAX # for quick fix, remove - CLIENT_AGE_MIN
SALE_MIN_AGE = 0
SALE_MAX_AGE = 35
MILEAGE_MIN = 0
MILEAGE_MAX = 65000
PRICE_MIN = 750
PRICE_MAX = 3640
GARAGE_FREQ = 1 / 3

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


# create a data frame
cars = pd.DataFrame(columns=['VIN', 'Registration_ID', 'Car_type_ID', 'Colour', 'Engine_capacity'])

# populate the data frame
for i in range(NUMBER_OF_CARS):
    cars.loc[i] = [generate_vin(), generate_registration_id(), generate_car_type(len(car_types.index) + 1),
                   generate_colour(), generate_engine_capacity()]

# keep only the rows with unique VIN and Registration_ID
cars = cars.drop_duplicates('VIN')
cars = cars.drop_duplicates('Registration_ID')

NUMBER_OF_CLIENTS = len(cars)

# save the data frame to the csv file
cars.to_csv('cars.csv', index=False)
print('cars ready!')

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


# create a data frame
clients = pd.DataFrame(columns=['PESEL', 'Name1', 'Name2', 'Surname', 'Sex',
                                'Date_of_birth', 'Voivodeship', 'City', 'Street_and_number',
                                'Account_nb', 'License_issuing_date'])

# populate the data frame
for i in range(NUMBER_OF_CLIENTS):
    # dates - birth, license issuing
    birth = f.date_of_birth(minimum_age=CLIENT_AGE_MIN, maximum_age=CLIENT_AGE_MAX)
    # quick fix
    license_max = (2023 - birth.year - LICENSE_MIN)
    license = f.date_of_birth(minimum_age=0, maximum_age=license_max)

    # creates infinite loops in old cases, to be fixed in the future
    # while (license - birth >= timedelta(weeks=52 * CLIENT_AGE_MIN)):
    #    license = f.date_of_birth(minimum_age=LICENSE_MIN, maximum_age=LICENSE_MAX)

    # insert
    if i % 2 == 0:
        # a male
        clients.loc[i] = [pesel(birth, 'M'), f.first_name_male(), f.first_name_male(), f.last_name_male(),
                          'M', birth.isoformat(), f.administrative_unit(), f.city(), f.street_address(),
                          f.iban(), license.isoformat()]
    else:
        # a female
        clients.loc[i] = [pesel(birth, 'F'), f.first_name_female(), f.first_name_female(), f.last_name_female(),
                          'F', birth.isoformat(), f.administrative_unit(), f.city(), f.street_address(),
                          f.iban(), license.isoformat()]

# shift indices so the first index equals 1 not 0
clients.index += 1

# save the data frame to the csv file
clients.to_csv('clients.csv', index_label='ID')
print('clients ready!')

# generate Employees ###################################################################################################

# create a data frame
employees = pd.DataFrame(columns=['ID', 'Name', 'Surname', 'Function'])

# populate the data frame
for i in range(NUMBER_OF_EMPLOYEES):
    position = random.choice(['agent', 'assessor'])
    employees.loc[i] = [i + 1, f.first_name(), f.last_name(), position]

# save the data frame to the csv file
employees.to_csv('employees.csv', index=False)
print('employees ready!')


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


def choose_employee(fu):
    agent_id = random.randint(0, NUMBER_OF_EMPLOYEES - 1)
    while employees.iloc[agent_id]['Function'] != fu:
        agent_id = random.randint(0, NUMBER_OF_EMPLOYEES - 1)
    return agent_id


# create a data frame
insurances = pd.DataFrame(columns=['Sale_date', 'Car', 'Mileage', 'Garage', 'Agent_ID', 'Price', 'Client_ID'])

# populate the data frame
# every car in th DB has to be insured; chociaz jesli jest wiecej samochodow niz klientow... a moze mniej niz ubezpieczen?
carID = 0
clientID = 0
for i in range(NUMBER_OF_INSURANCES):
    # choosing cars one by one
    carID += 1
    if carID >= NUMBER_OF_CARS:
        carID = 1

    # choosing clients one by one
    clientID += 1
    if clientID >= NUMBER_OF_CLIENTS:
        clientID = 1

    # dates: sale to be set, license from Clients, production from Car_Types via Cars, OK if S>=L && S>=P
    sale_date = f.date_of_birth(minimum_age=SALE_MIN_AGE, maximum_age=SALE_MAX_AGE)
    license_date = clients.iloc[clientID]['License_issuing_date']
    car_type = cars.iloc[carID]['Car_type_ID']
    production_date = car_types.iloc[car_type - 1]['Production_year']  # -1 due to indexing issues
    # OK if S>=L && S>=P; not OK if S<P or S<L
    while (sale_date.isoformat() < license_date) or (sale_date.isoformat()[:4] < str(production_date)):
        sale_date = f.date_of_birth(minimum_age=SALE_MIN_AGE, maximum_age=SALE_MAX_AGE)

    # insert
    insurances.loc[i] = [sale_date, cars.iloc[carID]['VIN'], generate_mileage(), generate_garage(),
                         choose_employee('agent'), generate_price(), clientID]

# shift indices so the first index equals 1 not 0
insurances.index += 1

# save the data frame to the csv file
insurances.to_csv('insurances.csv', index_label='ID')
print('insurances ready!')

# generate Claims ######################################################################################################

# generator a data frame
claims = pd.DataFrame(columns=['Submission_date', 'Parking_place',
                               'Assessor_ID', 'Indemnity', 'Evaluation_date',
                               'Engine', 'Front_doors', 'Rear_doors',
                               'Left_mirror', 'Right_mirror', 'Front_headlights',
                               'Rear_headlights', 'Front_bumper', 'Rear_bumper', 'Insurance_ID'])


# define a function generating damage
def generate_damage():
    probability = random.uniform(0, 1)

    # chances:
    # 70% - no damage (0); default
    # 20% - repair (1)
    # 10% - replacement (2)

    damage = 0

    if 0.70 < probability <= 0.90:
        damage = 1
    elif probability > 0.90:
        damage = 2

    return damage


# populate the data frame with generated damage
# The status of =Submission_date=, =Assessor_ID=, Indemnity, =Evaluation_date= is To Be Determined (TBD) and =insurance=
for i in range(NUMBER_OF_CLAIMS):
    # from which insurance
    insuranceID = random.randint(1, NUMBER_OF_INSURANCES - 1)

    # where
    parking = f.address()
    parking = parking.replace('\n', ' ')

    # dates, OK if sub < eval and sub > sale
    # submittion = f.date_between()
    # sale = insurances.iloc[insuranceID]['Sale_date']
    # while sale > submittion:
    #     submittion = f.date_between()  # today-30
    # NEW: changed method of generation
    sale = insurances.iloc[insuranceID]['Sale_date']
    submittion_delta = random.randint(1, 365)
    submittion = sale + datetime.timedelta(days=submittion_delta)

    # evaluation at most 14 days after submittion
    delta = random.randint(1, 14)
    evaluation = submittion + datetime.timedelta(days=delta)

    claims.loc[i] = [submittion, parking, choose_employee('assessor'), 0, evaluation,
                     generate_damage(), generate_damage(), generate_damage(),
                     generate_damage(), generate_damage(), generate_damage(),
                     generate_damage(), generate_damage(), generate_damage(), insuranceID]

    # # calculate indemnity for all damaged or replaced parts
    indemnity = 0
    car = insurances.iloc[insuranceID]['Car']
    car_type = cars.loc[cars['VIN'] == car]['Car_type_ID']
    car_type_id = car_type.iloc[0]
    parts = parts.loc[parts['Car_type_ID'] == car_type_id]

    factor = 0.5  # multiply by this factor to obtain value of repairs/replacements

    # !!! I will fix it in the future; it takes too much time and adds too little to the output

    engine_value = parts.loc[parts['Part'] == 'Engine']['Value'] * claims.iloc[i]['Engine'] * factor
    front_doors_value = parts.loc[parts['Part'] == 'Front_doors']['Value'] * claims.iloc[i]['Front_doors'] * factor
    rear_doors_value = parts.loc[parts['Part'] == 'Rear_doors']['Value'] * claims.iloc[i]['Rear_doors'] * factor
    left_mirror_value = parts.loc[parts['Part'] == 'Left_mirror']['Value'] * claims.iloc[i]['Left_mirror'] * factor
    right_mirror_value = parts.loc[parts['Part'] == 'Right_mirror']['Value'] * claims.iloc[i]['Right_mirror'] * factor
    front_headlight_value = parts.loc[parts['Part'] == 'Front_headlights']['Value'] * claims.iloc[i]['Front_headlights'] * factor
    rear_headlight_value = parts.loc[parts['Part'] == 'Rear_headlights']['Value'] * claims.iloc[i]['Rear_headlights'] * factor
    front_bumper_value = parts.loc[parts['Part'] == 'Front_bumper']['Value'] * claims.iloc[i]['Front_bumper'] * factor
    rear_bumper_value = parts.loc[parts['Part'] == 'Rear_bumper']['Value'] * claims.iloc[i]['Rear_bumper'] * factor

    indemnity = engine_value + front_doors_value + rear_doors_value \
                + left_mirror_value + right_mirror_value + front_headlight_value \
                + rear_headlight_value + front_bumper_value + rear_bumper_value


    #claims.iat[i, 4] = indemnity

# shift indices so the first index equals 1 not 0
claims.index += 1

claims.to_csv('claims.csv', index_label='ID')
print('claims ready!')
