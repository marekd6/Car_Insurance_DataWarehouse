import datetime
import pandas as pd
import random
from faker import Faker

random.seed(1)
f = Faker(["pl_PL"])

# from exisiting files
MaxClient = 100000
MaxCar = 99866

# arbitrary setup
MinMileage = 0
MaxMileage = 35000
GarageProbFact = 4
DamageProbFact = 2
ReplaceProbFact = 4
MaxAgent = 199
MaxAssessor = 270
MinPrice = 900
MaxPrice = 3700

# desired number
NbInsurances = 3000 #3000000
NbClaims = 3040 #3000700

# load Cars and Clients
cars = pd.read_csv('cars.csv')
clients = pd.read_csv('clients.csv')
parts = pd.read_csv('parts.csv')
types = pd.read_csv('car_types.csv')
###############

# retrieve VIN from Insurances
def get_VIN(insurance):
    return insurances['Car'][insurance]

# from Claim, Car type and parts catalogue
def get_part_price(part, VIN):
    val = 0
    carType = 4 # broken
    filter = 4 # broken (parts['Part'] == part) & (parts['Car_type_ID'])
    val = 4 # broken (parts.where(filter))[carType]
    return val
###############

# create Insurances
insurances = pd.DataFrame(columns=['Sale_date', 'Car', 'Mileage', 'Garage', 'Agent_ID', 'Price', 'Client_ID'])

client = 0
carID = 0
for i in range(NbInsurances):
    # every Car is insured, VIN through carID
    carID += 1
    if carID > MaxCar:
        carID = 1
    car = cars['VIN'][carID]

    mileage = random.randint(MinMileage,MaxMileage)

    garage = 0
    if random.randint(1,1000) % GarageProbFact == 0:
        garage = 1

    agent = random.randint(1,MaxAgent)

    price = random.randint(MinPrice,MaxPrice)

    # every Client has an Insurance
    client += 1
    if client > MaxClient:
        client = 1

    insurances.loc[i] = [datetime.datetime(2020, 5, 17), car, mileage, garage, agent, price, client]

# save Insurances
insurances.index += 1
insurances.to_csv('insurances.csv', index_label='ID')
###############

# create Claims
part_names_insurance = ["Engine", "Front doors", "Rear doors",
              "Left mirror", "Right mirror", "Front headlights",
              "Rear headlights", "Front bumper", "Rear bumper", "Insurance_ID"]
cols = ['Submission_date', 'Parking_place', 'Assessor_ID', 'Indemnity', 'Evaluation_date'] + part_names_insurance
claims = pd.DataFrame(columns=cols)

parts_vals = []
for j in range(9):
    parts_vals.append(0)
insurance = 0
for i in range(NbClaims):
    # Faker again
    parking = f.address()
    parking = parking.replace('\n', ' ')

    assessor = random.randint(MaxAgent+1,MaxAssessor)

    # indemnity calulated?
    value = 0 # random.randint(MinPrice,MaxPrice)

    insurance += 1
    if insurance > NbInsurances:
        insurance = 1

    VIN = get_VIN(insurance)

    # damages
    coef = 0
    for j in range(9):
        # no damage
        parts_vals[j] = 0
        # damaged
        if random.randint(1,1000) % DamageProbFact == 0:
            # repair
            parts_vals[j] = 1
            coef = 1
            if random.randint(1,1000) % ReplaceProbFact == 0:
                # replace
                parts_vals[j] = 2
                coef = 0.5
        part = part_names_insurance[j]
        # here apply 50% for repair
        value += get_part_price(part, VIN) * coef

    claims.loc[i] = [datetime.datetime(2020, 5, 17), parking, assessor, value, datetime.datetime(2020, 5, 17)] + parts_vals + [insurance]

# save Claims
claims.index += 1
claims.to_csv('claims.csv', index_label='ID')
###############


# gather Cars (produkcja), Insurances (sale), Claims (claim), Client (birth, license)
# urodzenie Cli < license Cli < sale Ins < claim Cl < evaluation Cl
# produkcja Car < sale Ins
# join
# operate, alter
# from DF to CSVs