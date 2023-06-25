# https://gist.github.com/anonymous/cade4cca984b733d5c30

# the first 6 digits are for d.o.b.: respectively: year, month, day 022 927
# years 1900 - 1999 have normal months numbers (1 - 12)
# years 2000 - 2099 have normal months numbers + 20 (21 - 32)
# the following four digits are random (well, excluding last one coz it stands for sex) 0391
# the last digit comes out of a equation, and it is for checking the validity 7
# equation: 1*a + 3*b + 7*c + 9*d + 1*e + 3*f + 7*g + 9*h + 1*i + 3*j 0+6+14+81+2+21+0+27+9+3=163
# (where the a-j letters are standing for the digits of first ten digits of PESEL number respectively)
# then: 10 - (the last digit of the equation result) gives you the last digit of PESEL number 10-3=7 OK
# (if the last digit of the equation was 0, then it is the last digit of PESEL as well)

from datetime import date, datetime
import random

def pesel(bd, sex):
    #year = random.randint(1900,2099)
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

    # printing the final number out

    """ print('%02d' % (year % 100), end='')
    print('%02d' % month, end='')
    print('%02d' % day, end='')
    print(four_random, end='')
    print(last_digit) """
    out = str(year%100)
    out += str(month)
    out += str(day)
    out += four_random
    out += str(last_digit)
    print(out)

new_var = date(2023, 3, 20)
pesel(new_var, 'F')