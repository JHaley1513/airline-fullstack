import sys
import argparse #for parsing inputs on which tables to clear
import pymysql.cursors
from random import randint
import datetime
import string
import math

import airlines
from airports import airport_attr, airport_tiers
import daylight_savings as dst

conn = pymysql.connect(host='localhost',
                       user='monty',
                       port = 8889,
                       password='some_pass',
                       db='airline_tickets',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

customers = []

tickets = []

def execute_query(query, arguments=None):
    cursor = conn.cursor()
    if arguments:
        cursor.execute(query, arguments)
    else:
        cursor.execute(query)
    conn.commit()
    cursor.close()
    # pass

def remake_all_tables():
    remake_tables(['ticket', 'customer', 'flight', 'airplane', 'airport', 'airline'])

def remake_tables(tables):
    """Removes and regenerates all data in specified tables."""
    if 'none' not in tables:
        t = 'ticket' in tables
        c = 'customer' in tables
        f = 'flight' in tables
        apl = 'airplane' in tables
        apt = 'airport' in tables
        aln = 'airline' in tables

        queries = []
        if t or c or f or apt or apl or aln:
            queries.append('DELETE FROM `ticket`')
        if c:
            queries.append('DELETE FROM `customer`')
        if f or apt or apl or aln:
            queries.append('DELETE FROM `flight`')
        if apl or aln:
            queries.append('DELETE FROM `airplane`')
        if apt:
            queries.append('DELETE FROM `airport`')
        if aln:
            queries.append('DELETE FROM `airline`')
        for q in queries:
            execute_query(q)

        if aln:
            add_airlines()
        if apt:
            add_airports()
        if apl or aln:
            add_airplanes()
        if f or apt or apl or aln:
            create_flights(100000)
        if c:
            generate_customers()
        if t or c or f or apt or apl or aln:
            generate_tickets()

###################################################################################
######################## ADD AIRLINES, AIRPORTS, AIRPLANES ########################
###################################################################################
def add_airlines():
    for code in airlines.airline_codes():
        query = 'INSERT INTO `airline` (`code`, `name`, `hub_code`) VALUES (%s, %s, %s);'
        args = (code, airlines.get_airline_name(code), airlines.get_airline_hub(code))
        execute_query(query, args)

def add_airports():
    for a in airport_attr:
        query = 'INSERT INTO `airport` (`code`, `name`, `city`, `state`, `country`, `is_international`, `longitude`, `latitude`, `gmt_difference`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);'
        execute_query(query, (a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8]))

def add_airplanes():
    for code in airlines.airline_codes():
        i = 0
        for plane in airlines.get_airline_planes(code):
            for j in range(plane[0]):
                query = 'INSERT INTO `airplane` (`id`, `airline_code`, `first_class`, `business_class`, `economy_plus`, `economy`) VALUES (%s, %s, %s, %s, %s);'
                # pad with leading zeros to get a 5-digit ID number string
                plane_code = str(i).zfill(5)
                execute_query(query, (plane_code, airline_code, plane[1], plane[2], plane[3], plane[4]))
                i += 1

###################################################################################
################################ GENERATE FLIGHTS ################################
###################################################################################
def create_flights(n):
    flights = []
    i = 0
    next_flight_time = datetime.datetime.today()
    next_flight_time = next_flight_time + datetime.timedelta(days=-1) #starts yesterday
    last_flight_number = {}
    for code in airline_names.keys():
        last_flight_number[code] = 101 #flight numbers will go from 101 to 999

    while i < n:
        #depart and arrive are the full lists of the departure/arrival airports' attributes
        depart = airport_attr[ randint(0, len(airport_attr)-1) ]
        arrive = airport_attr[ randint(0, len(airport_attr)-1) ]
        if depart[0] == arrive[0]: #same airport code and therefore the same airport
            continue
        # distance = coordinate_distance(depart[6], arrive[6], depart[7], arrive[7])
        distance = distance_between_airports(depart[0], arrive[0])
        if distance < 0.5: #slightly closer than the distance between the two Shanghai airports
            continue
        elif distance > 183.0: #slightly farther than Newark to Singapore, one of the longest routes in the world
            continue
        elif departs_during_off_hours(next_flight_time, depart[3], depart[4], depart[8]): #no departures between midnight and 7 am local time
            continue
        else:
            add_flight = flight_endpoints_dice_roll(depart, arrive)
            if add_flight:
                #Each flight departs 5 minutes after the previous one.
                airline_code = determine_airline(depart[0], arrive[0])
                flight_no = determine_flight_number(airline, last_flight_number)
                airplane_id = None
                base_price = None
                depart_time, length_hrs, length_mins = determine_departure_and_length(depart[0], arrive[0])
                query = 'INSERT INTO `flight` (`flight_no`, `airline_code`, `airplane_id`, `base_price`, `depart_from`, `depart_time`, `arrive_at`, `length_hrs`, `flight_status`, `length_mins`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
                args = (flight_no, airline_code, airplane_id, base_price, depart[0], depart_time, arrive[0], length_hrs, 'ontime', length_mins)
                # execute_query(query, args)
                i += 1

def distance_between_airports(code1, code2):
    if code1 == code2:
        return 0
    idx1 = idx2 = -1
    for i in range(len(airport_attr)):
        if airport_attr[i][0] == code1:
            idx1 = i
        if airport_attr[i][0] == code2:
            idx2 = i
        if idx1 > -1 and idx2 > -1:
            break
    if idx1 == -1:
        raise ValueError("Code " + code1 + " not found in airport_attr list")
    if idx2 == -1:
        raise ValueError("Code " + code2 + " not found in airport_attr list")
    distance = coordinate_distance(airport_attr[idx1][6],airport_attr[idx2][6],airport_attr[idx1][7],airport_attr[idx2][7])
    #print("The distance between " + code1 + " and " + code2 + " is " + "{:.2f}".format(distance))
    return distance

def coordinate_distance(x1, x2, y1, y2):
    lat_distance = abs(x1 - x2)
    long_distance = abs(y1 - y2)
    # print(lat_distance, long_distance)
    if lat_distance > 180:
        lat_distance = 360 - lat_distance
    if long_distance > 180:
        long_distance = 360 - long_distance
    # print(lat_distance, long_distance)
    return math.sqrt(lat_distance**2 + long_distance**2)

def departs_during_off_hours(depart_time, state, country, gmt_diff):
    #depart_time is a datetime object, gmt_diff is a float (an int followed by .0, .75, .5, or .25)
    #depart_time uses the gmt time zone. gmt_diff is the number of hours plus or minus GMT.
    #We're checking whether the depart time is between midnight and 7 am local time.
    hours_diff = int(gmt_diff)
    if math.isclose(abs(gmt_diff - hours_diff), 0.0):
        mins_diff = 0
    elif math.isclose(abs(gmt_diff - hours_diff), 0.25):
        mins_diff = 15
    elif math.isclose(abs(gmt_diff - hours_diff), 0.5):
        mins_diff = 30
    elif math.isclose(abs(gmt_diff - hours_diff), 0.75):
        mins_diff = 45
    diff = datetime.timedelta(hours=hours_diff, minutes=mins_diff)
    local_time = depart_time + diff

    year = depart_time.year
    if dst.is_daylight_savings(local_time, year, state, country):
        local_time += datetime.timedelta(hours=1)

    if 0 < local_time.hours < 7:
        return True
    return False


#Dice roll to determine whether to keep a prospective flight.
def flight_endpoints_dice_roll(depart, arrive):
    #Oct 30 - this is calibrated to output roughly equal numbers of domestic and intl flights
    #when using our current database (which has few same-country flights besides the US and China).
    #There's also significantly more intl flights for higher-tier airports, but roughly equal amounts of
    #domestic flights among all tiers.
    combined_odds = -1
    target = -1
    if depart[4] == arrive[4]: #same country
        tier_d = get_airport_tier(depart[0], 'domestic') #depart[0] is the airport code
        tier_a = get_airport_tier(arrive[0], 'domestic')
        if tier_d == tier_a == 1:
            target = 5
        elif (tier_d == 1 and tier_a == 2) or (tier_d == 2 and tier_a == 1):
            target = 10
        elif tier_d == tier_a == 2:
            target = 5
        elif (tier_d == 3 and tier_a == 1) or (tier_d == 1 and tier_a == 3):
            target = 5
        elif (tier_d == 3 and tier_a == 2) or (tier_d == 2 and tier_a == 3):
            target = 4
        elif tier_d == tier_a == 3:
            target = 1 #100% odds, these are rare enough that we'll want to keep them every time
    else:
        tier_d = get_airport_tier(depart[0], 'intl')
        tier_a = get_airport_tier(arrive[0], 'intl')
        #these are weighted 50% less/more to both tier 1's/tier 3's, 25% less/more to a 2+1/3+2
        if tier_d == tier_a == 1:
            target = 450
        elif (tier_d == 1 and tier_a == 2) or (tier_d == 2 and tier_a == 1):
            target = 112
        elif tier_d == tier_a == 2:
            target = 160
        elif (tier_d == 3 and tier_a == 1) or (tier_d == 1 and tier_a == 3):
            target = 5
        elif (tier_d == 3 and tier_a == 2) or (tier_d == 2 and tier_a == 3):
            target = 17
        elif tier_d == tier_a == 3:
            target = 9
    dice = randint(1, target)
    return dice == target

#Possible tiers are 3 (busiest airports in the world), 2 (other major airports), or 1 (all others).
#Each airport has a domestic and international tier, since some airports have a lot
#of domestic traffic but little international traffic or vice versa
def get_airport_tier(code, domestic_or_intl):
    if code in airport_tiers:
        if domestic_or_intl == 'domestic':
            return airport_tiers[code][0]
        elif domestic_or_intl == 'intl' or domestic_or_intl == 'international':
            return airport_tiers[code][1]
    return 1


def determine_airline(code1, code2):
    #must be less than 50 for each
    weight1 = weight2 = 1
    weights = []
    weights_total = 0
    for airline_abbrev,base_airport in airline_hubs.items():
        dist1 = distance_between_airports(code1, base_airport)
        if dist1 == 0:
            weight1 = 10
        elif dist1 < 10:
            weight1 = 5
        else:
            weight1 = int(50 / dist1) #becomes 0 if dist1 > 50
        dist2 = distance_between_airports(code2, base_airport)
        if dist2 == 0:
            weight2 = 10
        elif dist2 < 10:
            weight2 = 5
        else:
            weight2 = int(50 / dist2)
        if weight1+weight2 > 0:
            weights.append([weight1+weight2, airline_abbrev])
            weights_total += weight1+weight2
    if len(weights) > 0:
        dice_roll = randint(0, weights_total-1)
        total = 0
        for weight_and_airline in weights:
            if total >= dice_roll:
                return weight_and_airline[1]
            total += weight_and_airline[0]
            if total >= dice_roll:
                return weight_and_airline[1]
    raiseValueError('No suitable airline found for the flight from ' + code1 + ' to ' + code2 + '.')
# print(determine_airline('JFK','ORD'))

def determine_flight_number(airline_code, last_flight_number):
    #last_flight_number is a dict where key is airline code, val is the most recently used flight number for that airline
    if last_flight_number[airline_code] == 999:
        last_flight_number[airline_code] = 101
    else:
        last_flight_number[airline_code] += 1
    return airline_code + str(last_flight_number[airline_code])

dict = {}
def increment_dict(code, type):
    if code in dict:
        dict[code][type] += 1
    else:
        dict[code] = {'domestic':0,'intl':0}

###################################################################################
############################### GENERATE CUSTOMERS ###############################
###################################################################################
def generate_customers():
    global customers
    firsts = ["James", "David", "Chris", "George", "Ron", "John", "Richard", "Daniel",
                "Kenneth", "Anthony", "Robert", "Charles", "Paul", "Steven", "Kevin",
                "Michael", "Joseph", "Mark", "Edward", "Jason", "William", "Thomas",
                "Donald", "Brian", "Jeff", "Emma", "Olivia", "Ava", "Isabella",
                "Sophia", "Mia", "Charlotte", "Amelia", "Evelyn", "Abigail", "Harper",
                "Emily", "Elizabeth", "Avery", "Sofia", "Ella", "Madison", "Scarlett",
                "Victoria", "Aria", "Grace", "Chloe", "Camila", "Penelope", "Riley"]
    states = ["AK", "AL", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID",
                "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS",
                "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK",
                "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    countries = ["Russia", "Israel", "Turkey", "Japan", "Singapore", "France", "Germany",
                    "South Korea", "Denmark", "Finland", "Italy", "Spain", "Sweden", "Austria",
                    "Luxembourg", "Netherlands", "Norway", "Portugal", "UK", "Belgium", "Canada",
                    "Ireland", "Switzerland", "Australia", "Greece", "Malta", "Czech Republic",
                    "New Zealand", "Iceland", "Hungary", "Malaysia", "Slovenia"]
    for i in range(10000):
        first = firsts[randint(0, len(firsts)-1)]
        last = "Customer" + str(i)
        name = first + " " + last
        email = first[0].lower() + first[1:] + str(i) + "@example.org"
        password = "0000" + str(i)

        building_no = randint(0, 999)
        street = "Street St"
        city = "ABCity"
        state = states[randint(0, len(states)-1)]
        phone_no = "{:0>10d}".format(randint(0, 9999999999))

        passport_no = "{:0>9d}".format(randint(0, 999999999))
        exp_yr = randint(2020, 2029)
        exp_mo = randint(1, 12)
        exp_dy = randint(1, 28)
        passport_exp = datetime.date(exp_yr, exp_mo, exp_dy).strftime("20%y-%m-%d")
        coinflip = randint(0, 3) #1/2 chance of USA, 1/4 of China, 1/4 of all other countries
        if coinflip >= 2:
            passport_country = "USA"
        elif coinflip == 1:
            passport_country = "China"
        else:
            passport_country = countries[randint(0, len(countries)-1)]

        coinflip = randint(0, 63)
        #The following distribution of ages taken from US census, didn't include people born after 2001 as they're less likely to be buying tickets (as of 2019).
        #Technically the numbers should be skewed more towards the middle-aged as they're the most likely to actually be ordering tickets (i.e. business trips, or ordering tickets for their family), but this is a programming project, not a study in advanced demographics.
        if coinflip < 8:
            birth_yr = randint(1995, 2001)
        elif coinflip < 46:
            birth_yr = randint(1975, 1994)
        elif coinflip < 60:
            birth_yr = randint(1955, 1974)
        elif coinflip < 63:
            birth_yr = randint(1934, 1954)
        else:
            birth_yr = randint(1906, 1933)
        birth_mo = randint(1, 12)
        birth_dy = randint(1, 28)
        if birth_yr >= 2000:
            date_of_birth = datetime.date(birth_yr, birth_mo, birth_dy).strftime("20%y-%m-%d")
        else:
            date_of_birth = datetime.date(birth_yr, birth_mo, birth_dy).strftime("19%y-%m-%d")

        customers.append((email, name, password, building_no, street, city, state, phone_no, passport_no, passport_exp, passport_country, date_of_birth))
    for i in customers:
        # print("INSERT INTO `customer` (`email`, `name`, `password`, `building_no`, `street`, `city`, `state`, `phone_no`, `passport_no`, `passport_expiration`, `passport_country`, `date_of_birth`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);" % (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11]))
        query = 'INSERT INTO `customer` (`email`, `name`, `password`, `building_no`, `street`, `city`, `state`, `phone_no`, `passport_no`, `passport_expiration`, `passport_country`, `date_of_birth`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
        args = (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11])
        execute_query(query, args)

###################################################################################
################################ GENERATE TICKETS ################################
###################################################################################
def generate_tickets():
    global tickets
    # refflight = (flight_no, airline, plane_num, price, start_airport, start_date.strftime("20%y-%m-%d %H:%M:%S"), end_airport, end_date.strftime("20%y-%m-%d %H:%M:%S"), flight_status, delay)
    ticket_id = 0
    for f in flights:
        flight_no = f[0]
        airline = f[1]
        plane_num = f[2]
        temp_capacity = planes_by_id[airline][int(plane_num)][2]
        temp_tenpercent = temp_capacity * 0.1
        tickets_sold = temp_capacity + randint(0, int((temp_tenpercent-1)*2)) - int(temp_tenpercent) #can go between 90% and 110% capacity sold
        base_price = f[3]
        temp_flightdatetime = extract_datetime(f[5])
        if temp_flightdatetime == "wut":
            return
        temp_custticketsleft = 0
        temp_thirtypercent = None
        credit_or_debit = None
        card_no = None
        expiration = None
        purchase_date_time = None
        customer_name = None
        customer_email = None
        for t in range(tickets_sold):
            if temp_custticketsleft == 0:
                temp_custticketsleft = make_tickets_num()
                temp_thirtypercent = base_price * 0.3
                coinflip = randint(0, 1)
                credit_or_debit = "debit" if coinflip == 0 else "credit"
                card_no = []
                for _ in range(16):
                    card_no.append(str(randint(0, 9)))
                card_no = "".join(card_no)
                expiration = datetime.datetime(randint(2020, 2029), randint(1, 12), 1)
                purchase_date_time = temp_flightdatetime + datetime.timedelta(days=randint(0,240), hours=randint(0, 23), minutes=randint(0, 59))
                idx = randint(0, len(customers)-1)
                customer_email, customer_name = customers[idx][0], customers[idx][1]
            sold_price = base_price + randint(0, int((temp_thirtypercent-1)*2)) - temp_thirtypercent
            tickets.append((ticket_id, flight_no, airline, sold_price, credit_or_debit, card_no, customer_name, expiration.strftime("20%y-%m-%d"), purchase_date_time.strftime("20%y-%m-%d %H:%M:%S"), customer_email))
            temp_custticketsleft -= 1
            ticket_id += 1
    for t in tickets:
        # print("INSERT INTO `ticket` (`ticket_id`, `flight_no`, `airline_name`, `sold_price`, `credit_or_debit`, `card_no`, `cardholder`, `expiration`, `purchase_date_time`, `customer_email`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);" % (t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], t[10]))
        query = 'INSERT INTO `ticket` (`ticket_id`, `flight_no`, `airline_name`, `sold_price`, `credit_or_debit`, `card_no`, `cardholder`, `expiration`, `purchase_date_time`, `customer_email`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
        args = (t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9])
        execute_query(query, args)


# "INSERT INTO `ticket` (`ticket_id`, `flight_no`, `airline_name`, `sold_price`, `credit_or_debit`, `card_no`, `cardholder`, `expiration`, `purchase_date_time`, `customer_email`) VALUES ("048", "MU411", "China Eastern", "947.56", "debit", "100020003011", "Emre Yorgy", "2028-02-01", "2019-05-08 06:18:18", "boom@dotcom.com", "y268115");"


def extract_datetime(string):
    #example: "20%y-%m-%d %H:%M:%S"
    y = int(string[0:4])
    mth = int(string[5:7])
    d = int(string[8:10])
    h = int(string[11:13])
    min = int(string[14:16])
    s = int(string[17:19])
    return datetime.datetime(y, mth, d, h, min, s)

def make_tickets_num():
    """Number of tickets per order. Uses Fibonacci sequence, skipping every other number"""
    coinflip = randint(0, 142)
    if coinflip >= 141:
        return 5
    elif coinflip >= 136:
        return 4
    elif coinflip >= 123:
        return 3
    elif coinflip >= 89:
        return 2
    else:
        return 1

###################################################################################
################################## MAIN FUNCTION ##################################
###################################################################################
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""
    After "python populateDatabase.py", list the tables you would like to clear, separated by spaces. If no tables are listed then all will be cleared. Or type none to keep all of them.\n
    WARNING: If you clear a higher-level table (i.e. airline), all the tables that rely on it (i.e. airplane, flight, ticket) will also be cleared.\n
    Tables: ticket customer flight airplane airport airline
    """)
    parser.add_argument("tables", nargs="*", help="Tables to Clear")
    args = parser.parse_args()
    if args.tables:
        remake_tables(args.tables)
    else:
        remake_all_tables()
