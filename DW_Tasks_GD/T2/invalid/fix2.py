import datetime
from datetime import timedelta
import pandas as pd
import random
from faker import Faker
from itertools import product

start_date = datetime.date(1993, 1, 1)

submission = []
parking = []
assessor = []
indemnity = []
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

for i in range(1000000):
    delta = random.randint(1, 365)
    delta2 = random.randint(1, 14)
    submission.append(start_date + datetime.timedelta(days=delta))
    parking.append(random.choice([0, 1]))
    assessor.append(random.randint(1, 5000))
    indemnity.append(random.randint(500, 250000))
    evaluation.append(submission[i] + datetime.timedelta(days=delta2))
    engine.append(random.choice([0, 1, 2]))
    fd.append(random.choice([0, 1, 2]))
    rd.append(random.choice([0, 1, 2]))
    lm.append(random.choice([0, 1, 2]))
    rm.append(random.choice([0, 1, 2]))
    fh.append(random.choice([0, 1, 2]))
    rh.append(random.choice([0, 1, 2]))
    fb.append(random.choice([0, 1, 2]))
    rb.append(random.choice([0, 1, 2]))
    if i % 10000 == 0:
        print(i)

insurance = list(range(1, 1000001))

#print('Length', len(submission), len(parking), len(assessor), len(indemnity), len(evaluation),
#                  len(engine), len(fd), len(rd), len(lm), len(rm), len(fh), len(rh), len(fb), len(rb), len(insurance))

output = list(zip(submission, parking, assessor, indemnity, evaluation,
                  engine, fd, rd, lm, rm, fh, rh, fb, rb, insurance))

claims2 = pd.DataFrame(output, columns=['Submission_date', 'Parking_place',
                               'Assessor_ID', 'Indemnity', 'Evaluation_date',
                               'Engine', 'Front_doors', 'Rear_doors',
                               'Left_mirror', 'Right_mirror', 'Front_headlights',
                               'Rear_headlights', 'Front_bumper', 'Rear_bumper', 'Insurance_ID'])

# shift indices so the first index equals 1 not 0
claims2.index += 1

claims2.to_csv('claims2.csv', index_label='ID')
