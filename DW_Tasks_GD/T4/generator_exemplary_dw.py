import datetime
import random
from faker import Faker

# the order of generation:
# 1. Cars done
# 2. Clients done
# 3. Assessors done
# 4. Dates done
# 5. Claims decimal places

# random seed, faker, and constants
random.seed(1)
f = Faker(['pl_PL'])
f.seed_instance(0)

NUMBER_OF_CARS = 5000
NUMBER_OF_CLIENTS = 5000
NUMBER_OF_ASSESSORS = 250
NUMBER_OF_CLAIMS = 2000
NUMBER_OF_DATES = 1000

MAX_COST = 90000
SUBMISSION_START = datetime.date(1993, 5, 1)
SUBMISSION_DELTA = 29
AGE_MIN = 18
AGE_MAX = 60

INSERT_INTO = 'insert into '
VALUES = 'values ('
APOSTROPHE = "'"
COMMA = ", "
END_OF_Q = ');'
CAR_HEADERS = 'DT_Car ("VIN", "Class", "Size", "Colour") '
CLIENT_HEADERS = 'DT_Client ("PESEL", "Sex", "Age", "Driving_experience", "Voivodeship", "Insertion_date", "Is_Current") '
ASSESSOR_HEADERS = 'DT_Assessor ("Name_and_Surname", "Specialisation") '
DATES_HEADERS = 'DT_Date ("Date", "Year", "Month", "MonthNo", "Day") '

# generate Cars ########################################################################################################
queries = []

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

def generate_colour():
    colours = ['black', 'silver', 'gray', 'white', 'red' 'green', 'blue', 'yellow', 'navy', 'lime', 'purple', 'maroon']

    colour = random.choice(colours)

    return colour

def generate_class():
    car_class = ['cheap', 'medium', 'premium']

    classs = random.choice(car_class)

    return classs

def generate_size():
    car_size = ['small', 'medium', 'large', 'cargo']

    size = random.choice(car_size)

    return size

# populate the data frame
for i in range(NUMBER_OF_CARS):
    entry = INSERT_INTO + CAR_HEADERS + VALUES + APOSTROPHE + generate_vin() + APOSTROPHE + COMMA
    entry = entry + APOSTROPHE + generate_class() + APOSTROPHE + COMMA
    entry = entry + APOSTROPHE + generate_size() + APOSTROPHE + COMMA
    entry = entry + APOSTROPHE + generate_colour() + APOSTROPHE + END_OF_Q
    queries.append(entry)

# keep only the rows with unique VIN and Registration_ID
# vin = list(dict.fromkeys(vin))
# print("Duplicates dropped")

with open('exemplary1.sql', 'w') as file:
    for line in queries:
        file.write(f"{line}\n")

print("Cars ready")
file.close()

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

queries = []
# populate the list
for i in range(NUMBER_OF_CLIENTS):
    date = SUBMISSION_START + datetime.timedelta(weeks=52*random.randint(0, SUBMISSION_DELTA)+random.randint(0,50), days=random.randint(1,30))
    gen = random.choice(['female', 'male'])
    gen2 = 'F'
    if gen == 'male':
        gen2 = 'M'
    entry = INSERT_INTO + CLIENT_HEADERS + VALUES + APOSTROPHE + pesel(date, gen2) + APOSTROPHE + COMMA
    entry = entry + APOSTROPHE + gen + APOSTROPHE + COMMA
    entry = entry + APOSTROPHE + random.choice(["from 18 to 21", "from 22 to 29", "from 30 to 49", "from 50 to 64", "more than 64"]) + APOSTROPHE + COMMA
    entry = entry + APOSTROPHE + random.choice(["up to one year", "between one and five years", "between five and ten years", "more than ten years"]) + APOSTROPHE + COMMA
    entry = entry + APOSTROPHE + f.administrative_unit() + APOSTROPHE + COMMA
    entry = entry + 'GetDate()' + COMMA
    entry = entry + '1' + END_OF_Q
    queries.append(entry)

with open('exemplary1.sql', 'a', encoding='utf-8-sig') as file:
    for line in queries:
        file.write(f"{line}\n")

print("Clients ready")
file.close()

# generate Assessors ###################################################################################################

def generate_specialisation():
    return random.choice(["cargo", "casual", "premium"])

queries = []
# populate the list
for i in range(NUMBER_OF_ASSESSORS):
    entry = INSERT_INTO + ASSESSOR_HEADERS + VALUES + APOSTROPHE + f.first_name() + ' ' + f.last_name() + APOSTROPHE + COMMA
    entry = entry + APOSTROPHE + generate_specialisation() + APOSTROPHE + END_OF_Q
    queries.append(entry)

with open('exemplary1.sql', 'a', encoding='utf-8-sig') as file:
    for line in queries:
        file.write(f"{line}\n")
print('assessors ready!')
file.close()

# generate Dates ###################################################################################################

queries = []
date = SUBMISSION_START
# populate the list
for i in range(NUMBER_OF_DATES):
    entry = INSERT_INTO + DATES_HEADERS + VALUES + APOSTROPHE + date.isoformat() + APOSTROPHE + COMMA
    entry = entry + APOSTROPHE + str(date.year) + APOSTROPHE + COMMA # YYYY
    entry = entry + APOSTROPHE + f.month_name() + APOSTROPHE + COMMA # month
    entry = entry + APOSTROPHE + str(date.month) + APOSTROPHE + COMMA # MM
    entry = entry + APOSTROPHE + str(date.day) + APOSTROPHE + END_OF_Q ## DD
    queries.append(entry)
    date = date + datetime.timedelta(days=1) # ++

with open('exemplary1.sql', 'a', encoding='utf-8-sig') as file:
    for line in queries:
        file.write(f"{line}\n")
print('dates ready!')
file.close()

# generate Claims ##################################################################################################

def generate_ID(upper_bound):
    return random.randint(1,upper_bound)

def generate_cost():
    return random.random() * MAX_COST

queries = []
# populate the list
for i in range(NUMBER_OF_CLAIMS):
    entry = INSERT_INTO + 'FT_Claim ' + VALUES + str(generate_ID(NUMBER_OF_DATES)) + COMMA #assessment
    entry = entry + str(generate_ID(NUMBER_OF_DATES)) + COMMA # submission
    entry = entry + str(generate_ID(NUMBER_OF_CLIENTS)) + COMMA # client
    entry = entry + str(generate_ID(NUMBER_OF_CARS)) + COMMA # car
    entry = entry + str(generate_ID(NUMBER_OF_ASSESSORS)) + COMMA # assessor
    entry = entry + str(generate_ID(9)) + COMMA # nb of damaged
    entry = entry + str(generate_cost()) + COMMA # indemnity
    entry = entry + str(generate_cost()) + COMMA # eng
    entry = entry + str(generate_cost()) + COMMA # fd
    entry = entry + str(generate_cost()) + COMMA # rd
    entry = entry + str(generate_cost()) + COMMA # lm
    entry = entry + str(generate_cost()) + COMMA # rm
    entry = entry + str(generate_cost()) + COMMA # fh
    entry = entry + str(generate_cost()) + COMMA # rh
    entry = entry + str(generate_cost()) + COMMA # fb
    entry = entry + str(generate_cost()) + END_OF_Q # rb
    queries.append(entry)

print('CLAIMS ready')

with open('exemplary1.sql', 'a', encoding='utf-8-sig') as file:
    for line in queries:
        file.write(f"{line}\n")
file.close()