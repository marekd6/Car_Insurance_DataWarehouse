import datetime
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
# 7. Claims

# random seed, faker, and constants
random.seed(1)
f = Faker(["pl_PL"])

NUMBER_OF_CARS = 10  # > NUMBER_OF_CLIENTS to account for dropping rows with duplicate VINs and Registration_IDs
NUMBER_OF_CLIENTS = 10
NUMBER_OF_EMPLOYEES = 10
NUMBER_OF_INSURANCES = 10
NUMBER_OF_CLAIMS = 10
PRODUCTION_YEAR_START = 1975
PRODUCTION_YEAR_END = 2023


# generate Car_types ###################################################################################################

# variables with all possible values
car_class = ["cheap", "medium", "premium"]
car_size = ["small", "medium", "large", "cargo"]
car_production_year = list(range(PRODUCTION_YEAR_START, PRODUCTION_YEAR_END))

# create a data frame
# product() is responsible for generating all possible combinations
car_types = pd.DataFrame(list(product(car_class, car_size, car_production_year)),
                         columns=["Class", "Size", "Production_year"])

# shift indices so the first index equals 1 not 0
car_types.index += 1

# save the data frame to the csv file
car_types.to_csv("car_types.csv", index_label="ID")


# generate Cars ########################################################################################################

# define functions generating VIN, Registration_ID, Colour, Car_type, and Engine_capacity
def generate_vin():
    letters = "ABCDEFGHJKLMNPRSTUVWXYZ"
    digits = "0123456789"
    letters_and_digits = "ABCDEFGHJKLMNPRSTUVWXYZ0123456789"
    vin = ""

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
    letters_first = "BCDEFGKLNOPRSTWZ"
    letters_second = "ABCDEFGHIJKLMNOPRSTUVWXYZ"
    digits = "0123456789"
    plate = ""

    plate += random.choice(letters_first)
    plate += random.choice(letters_second)
    plate += " "

    for d in range(5):
        plate += random.choice(digits)

    return plate


def generate_colour():
    colours = ["black", "silver", "gray", "white", "red" "green", "blue", "yellow", "navy", "lime", "purple", "maroon"]

    colour = random.choice(colours)

    return colour


def generate_car_type(number_of_car_types):
    return random.randrange(1, number_of_car_types)


def generate_engine_capacity():
    return random.randrange(10, 40) / 10


# create a data frame
cars = pd.DataFrame(columns=["VIN", "Registration_ID", "Car_type_ID", "Colour", "Engine_capacity"])

# populate the data frame
for i in range(NUMBER_OF_CARS):
    cars.loc[i] = [generate_vin(), generate_registration_id(), generate_car_type(len(car_types.index) + 1),
                   generate_colour(), generate_engine_capacity()]

# keep only the rows with unique VIN and Registration_ID
cars = cars.drop_duplicates("VIN")
cars = cars.drop_duplicates("Registration_ID")

# save the data frame to the csv file
cars.to_csv("cars.csv", index=False)


# generate Parts #######################################################################################################

# variables with values known upfront
part_names = ["Engine", "Front doors", "Rear doors",
              "Left mirror", "Right mirror", "Front headlights",
              "Rear headlights", "Front bumper", "Rear bumper"]
car_type_ids = list(range(1, len(car_types.index) + 1))

# create a data frame and add a column "Value" with the default value = 0
parts = pd.DataFrame(list(product(part_names, car_type_ids)),
                     columns=["Part", "Car_type_ID"])
parts["Value"] = 0


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

    if part == "Engine":
        initial_value = 30000
    elif part == "Front doors":
        initial_value = 10000
    elif part == "Rear doors":
        initial_value = 8000
    elif part == "Left mirror":
        initial_value = 1000
    elif part == "Right mirror":
        initial_value = 1000
    elif part == "Front headlights":
        initial_value = 500
    elif part == "Rear headlights":
        initial_value = 700
    elif part == "Front bumper":
        initial_value = 1500
    elif part == "Rear bumper":
        initial_value = 2000

    # the car_type_id is decreased as index of data frame starts from 0 and index of car types start from 1
    car_type_id = car_type_id - 1

    # default parameters for cheap and small cars
    class_parameter = 1
    size_parameter = 1

    # calculate age parameter
    car_age = 2023 - car_types.iloc[car_type_id]["Production_year"]
    age_parameter = (1 - (car_age / 50))

    # adjust class and size parameters if needed
    if car_types.iloc[car_type_id]["Class"] == "medium":
        class_parameter = 1.5
    elif car_types.iloc[car_type_id]["Class"] == "premium":
        class_parameter = 2.5

    if car_types.iloc[car_type_id]["Size"] == "medium":
        class_parameter = 1.2
    elif car_types.iloc[car_type_id]["Size"] == "large":
        class_parameter = 1.7
    elif car_types.iloc[car_type_id]["Size"] == "cargo":
        class_parameter = 2

    # calculate part value
    value = initial_value * class_parameter * size_parameter * age_parameter
    return round(value, 2)


# calculate a value of a given part; Parts (0: Part, 1: Car_type_ID, 2: Value)
for i in range(0, len(parts)):
    parts.iloc[i, 2] = generate_value(parts.iloc[i, 0], parts.iloc[i, 1])

# save the data frame to the csv file
parts.to_csv("parts.csv", index=False)


# generate Clients #####################################################################################################


# generate Employees ###################################################################################################


# generate Insurances ##################################################################################################


# generate Claims ######################################################################################################

# generator a data frame
claims = pd.DataFrame(columns=["Submission_date", "Parking_place",
                               "Assessor_ID", "Indemnity", "Evaluation_date",
                               "Engine", "Front_doors", "Rear_doors",
                               "Left_mirror", "Right_mirror", "Front_headlights",
                               "Rear_headlights", "Front_bumper", "Rear_bumper"])


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
# The status of Submission_date, Assessor_ID, Indemnity, Evaluation_date is To Be Determined (TBD)
for i in range(NUMBER_OF_CLAIMS):
    parking = f.address()
    parking = parking.replace('\n', ' ')

    claims.loc[i] = ["TBD", parking, "TBD", "TBD", "TBD",
                     generate_damage(), generate_damage(), generate_damage(),
                     generate_damage(), generate_damage(), generate_damage(),
                     generate_damage(), generate_damage(), generate_damage()]

claims.to_csv("claims.csv", index=False)
