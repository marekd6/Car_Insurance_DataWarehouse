from faker import Faker
import pandas as pd
import random

f = Faker(["pl_PL"]) # "en-GB"

ids = []
names = []
surnames = []
functions = []
agents = 200
assessors = 70

#1-agents - agents
for i in range(agents):
    ids.append(i)
    names.append(f.first_name())
    surnames.append(f.last_name())
    functions.append("agent")

#agents-(agents+assessors) - assessors
for i in range(assessors):
    ids.append(i+agents)
    names.append(f.first_name())
    surnames.append(f.last_name())
    functions.append("assessor")

employees = {
    'ID':ids,
    'Name':names,
    'Surname':surnames,
    'Function':functions
}

p = 'C:/Users/laptop/Desktop/employees.csv'
df = (pd.DataFrame(employees, columns = ['ID', 'Name', 'Surname', 'Function']))
df.to_csv(p, encoding = 'utf-8', index = False)