from faker import Faker
import random

f = Faker(['pl_PL'])
f.seed_instance(1)

NUMBER_OF_FACTS = 10000
CLIENT_AGE_MIN = 18
CLIENT_AGE_MAX = 90


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

    return year_s + month_s + day_s + four_random + str(last_digit)


file = open('dw_inserts.sql', 'w', encoding="utf-8")
file.write('USE [Car_Insurance]\nGO\n')
file.close()

file = open('dw_inserts.sql', 'a', encoding="utf-8")

for i in range(1, NUMBER_OF_FACTS):
    if i % 2 == 0:
        name_and_surname = f.first_name_male() + ' ' + f.last_name_male()
    else:
        name_and_surname = f.first_name_female() + ' ' + f.last_name_female()

    specialisation = random.choice(['cargo', 'premium', 'casual'])

    assessor_text = 'INSERT INTO DT_Assessor (Name_and_Surname, Specialisation) VALUES (\'' \
                    + name_and_surname + '\', \'' + specialisation + '\');\n'

    file.write(assessor_text)

for i in range(1, NUMBER_OF_FACTS):
    vin = generate_vin()
    car_class = random.choice(['cheap', 'medium', 'premium'])
    car_size = random.choice(['small', 'medium', 'large', 'cargo'])
    colour = random.choice(['black', 'silver', 'gray',
                            'white', 'red', 'green',
                            'blue', 'yellow', 'navy',
                            'lime', 'purple', 'maroon'])

    car_text = 'INSERT INTO DT_Car (VIN, Class, Size, Colour) VALUES (\'' \
               + vin + '\', \'' + car_class + '\', \'' + car_size + '\', \'' + colour + '\');\n'

    file.write(car_text)

for i in range(1, NUMBER_OF_FACTS):
    pesel_c = '00000000000'
    sex = 'male'
    birth = f.date_of_birth(minimum_age=CLIENT_AGE_MIN, maximum_age=CLIENT_AGE_MAX)
    insertion = f.date_of_birth(minimum_age=0, maximum_age=30)
    deactivation = f.date_of_birth(minimum_age=0, maximum_age=30)
    if i % 2 == 0:
        pesel_c = pesel(birth, 'M')
        sex = 'male'
    else:
        pesel_c = pesel(birth, 'F')
        sex = 'female'

    age = random.choice(['from 18 to 21', 'from 22 to 29', 'from 30 to 49', 'from 50 to 64', 'more than 64'])
    driving_experience = random.choice(['up to one year', 'between one and five years',
                                        'between five and ten years', 'more than ten years'])
    voivodeship = f.administrative_unit()
    insertion_date = insertion.isoformat()
    deactivation_date = deactivation.isoformat()
    is_current = random.choice(['1', '0'])

    client_text = 'INSERT INTO DT_Client (PESEL, Sex, Age, Driving_experience, Voivodeship, Insertion_date,' \
                  ' Deactivation_date, Is_Current) VALUES (\'' + pesel_c + '\', \'' + sex \
                  + '\', \'' + age + '\', \'' + driving_experience + '\', \'' + voivodeship \
                  + '\', \'' + insertion_date + '\', \'' + deactivation_date + '\', \'' \
                  + is_current + '\');\n'

    file.write(client_text)

for i in range(1, NUMBER_OF_FACTS * 2):
    new_date = f.date_of_birth(minimum_age=0, maximum_age=30)

    year = new_date.year
    month_no = new_date.month
    day = new_date.day

    month = 'January'

    if month_no == 2:
        month = 'February'
    elif month_no == 3:
        month = 'March'
    elif month_no == 4:
        month = 'April'
    elif month_no == 5:
        month = 'May'
    elif month_no == 6:
        month = 'June'
    elif month_no == 7:
        month = 'July'
    elif month_no == 8:
        month = 'August'
    elif month_no == 9:
        month = 'September'
    elif month_no == 10:
        month = 'October'
    elif month_no == 11:
        month = 'November'
    elif month_no == 12:
        month = 'December'

    date_text = 'INSERT INTO DT_Date (Date, Year, Month, MonthNo, Day) VALUES (\'' \
                + new_date.isoformat() + '\', \'' + str(year) + '\', \'' + month + '\', \'' \
                + str(month_no) + '\', \'' + str(day) + '\');\n'

    file.write(date_text)

for i in range(1, NUMBER_OF_FACTS):
    number_of_damaged_parts = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    indemnity = random.randint(100000, 250000)
    en = random.randint(0, 25000)
    fd = random.randint(0, 25000)
    rd = random.randint(0, 25000)
    lm = random.randint(0, 25000)
    rm = random.randint(0, 25000)
    fh = random.randint(0, 25000)
    rh = random.randint(0, 25000)
    fb = random.randint(0, 25000)
    rb = random.randint(0, 25000)

    claim_text = 'INSERT INTO FT_Claim (ID_Assessment_Date, ID_Submission_Date, ID_Client, ' \
                 'ID_Car, ID_Assessor, Number_of_damaged_parts, Indemnity, Engine_cost, Front_doors_cost, ' \
                 'Rear_doors_cost, Left_mirror_cost, Right_mirror_cost, Front_headlights_cost, ' \
                 'Rear_headlights_cost, Front_bumper_cost, Rear_bumper_cost) VALUES (\'' \
                 + str(i * 2) + '\', \'' + str(i) + '\', \'' + str(i) + '\', \'' + str(i) + '\', \'' \
                 + str(i) + '\', \'' + str(number_of_damaged_parts) + '\', \'' \
                 + str(indemnity) + '\', \'' + str(en) + '\', \'' \
                 + str(fd) + '\', \'' + str(rd) + '\', \'' + str(lm) + '\', \'' + str(rm) + '\', \'' \
                 + str(fh) + '\', \'' + str(rh) + '\', \'' + str(fb) + '\', \'' + str(rb) + '\');\n'

    file.write(claim_text)

file.close()
