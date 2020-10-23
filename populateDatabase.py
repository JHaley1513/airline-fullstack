import pymysql.cursors
from random import randint, choice
from decimal import Decimal
import datetime
import string

# conn = pymysql.connect(host='localhost',
#                        user='monty',
#                        port = 8889,
#                        password='some_pass',
#                        db='airline_tickets',
#                        charset='utf8mb4',
#                        cursorclass=pymysql.cursors.DictCursor)

airlines = ["China Eastern", "Haley Airways", "Smith Airlines"]

# airport format: code, name, city, state (or "null"), country, is_international (1=true), longitude,  latitude, gmt_difference (timezone)
# is_international is whether the airport has international flights.
# longitude is positive for E and negative for W, latitude is positive for N and negative for S.
airports = [
    #United States
    ["HNL", "", "Honolulu", "HI", "United States", 1, 21.3245, -157.9251, -10],
    ["SFO", "", "San Francisco", "CA", "United States", 1, 37.6213, -122.3790, -8],
    ["LAX", "", "Los Angeles", "CA", "United States", 1, 33.9416, -118.4085, -8],
    ["DFW", "Fort Worth", "Dallas", "TX", "United States", 1, 32.8998, -97.0403, -6],
    ["ORD", "O'Hare", "Chicago", "IL", "United States", 1, 41.9742, -87.9073, -6],
    ["ATL", "Hartsfield-Jackson", "Atlanta", "GA", "United States", 1, 33.6407, -84.4277, -5],
    ["JFK", "John F. Kennedy", "New York", "NY", "United States", 1, 40.6413, -73.7781, -5],
    ["MIA", "", "Miami", "FL", "United States", 1, 25.7959, -80.2871, -6],
    #Canada
    ["YVR", "", "Vancouver", "BC", "Canada", 1, 49.1967, -123.1815, -8],
    ["YYZ", "Pearson", "Toronto", "ON", "Canada", 1, 43.6777, -79.6248, -5],
    #Europe
    ["DUB", "", "Dublin", "null", "Ireland", 1, 53.4264, -6.2499, 0],
    ["MAD", "", "Madrid", "null", "Spain", 1, 40.4983, -3.5676, 1],
    ["LHR", "Heathrow", "London", "null", "United Kingdom", 1, 51.4700, 0.4543, 0],
    ["CDG", "Charles de Gaulle", "Paris", "null", "France", 1, 49.0139, 2.5425, 1],
    ["FRA", "am Main", "Frankfurt", "null", "Germany", 1, 50.0379, 8.5622, 1],
    ["FCO", "Fiumincino", "Rome", "null", "Italy", 1, 41.7999, 12.2462, 1],
    ["CPH", "", "Copenhagen", "null", "Denmark", 1, 55.6180, 12.6508, 1],
    ["VIE", "", "Vienna", "null", "Austria", 1, 48.1126, 16.5755, 1],
    ["ATH", "", "Athens", "null", "Greece", 1, 37.9356, 23.9484, 2],
    ["SVO", "Sheremetyevo", "Moscow", "Moscow", "Russia", 1, 55.9736, 37.4125, 3],
    #Near/Middle East
    ["IST", "", "Istanbul", "null", "Turkey", 1, 40.9830, 28.8104, 3],
    ["DOH", "Hamad", "Doha", "null", "Qatar", 1, 25.2609, 51.6138, 3],
    ["DXB", "", "Dubai", "null", "United Arab Emirates", 1, 25.2532, 55.3657, 4],
    #Far East
    ["BKK", "Suvarnabhumi", "Bangkok", "null", "Thailand", 1, 13.6900, 100.7501, 7],
    ["SIN", "Changi", "Singapore", "null", "Singapore", 1, 1.3644, 103.9915, 8],
    ["HKG", "", "Hong Kong", "null", "China", 1, 22.3080, 113.9185, 8],
    ["PVG", "Pudong", "Shanghai", "null", "China", 1, 31.1443, 121.8083, 8],
    ["PEK", "Capital", "Beijing", "null", "China", 1, 40.0799, 116.6031, 8],
    ["TPE", "Taoyuan", "Taipei", "null", "Taiwan", 1, 25.0797, 121.2342, 8],
    ["ICN", "Incheon", "Seoul", "null", "South Korea", 1, 37.4602, 126.4407, 9],
    ["NRT", "Narita", "Tokyo", "null", "Japan", 1, 35.7720, 140.3929, 9]
]

# only these US states do not observe daylight savings
no_daylight_savings_usa = ["AZ", "HI"]
# only these countries observe daylight savings
daylight_savings = {
    "United States": ["Mar second Su", "Nov first Su"],
    "Canada": ["Mar second Su", "Nov first Su"],
    "Austria": ["Mar last Su", "Oct last Su"],
    "Denmark": ["Mar last Su", "Oct last Su"],
    "France": ["Mar last Su", "Oct last Su"],
    "Germany": ["Mar last Su", "Oct last Su"],
    "Greece": ["Mar last Su", "Oct last Su"],
    "Ireland": ["Mar last Su", "Oct last Su"],
    "Italy": ["Mar last Su", "Oct last Su"],
    "Spain": ["Mar last Su", "Oct last Su"]
}

# Airport coordinates are listed by country or region, roughly in descending degrees W to ascending degrees E
# [+degrees N/-degrees S, +degrees E/-degrees W]
airport_coord = {
    #United States
    "HNL":[21.3245, -157.9251],
    "SFO":[37.6213, -122.3790],
    "LAX":[33.9416, -118.4085],
    "DFW":[32.8998, -97.0403],
    "ORD":[41.9742, -87.9073],
    "ATL":[33.6407, -84.4277],
    "JFK":[40.6413, -73.7781],
    "MIA":[25.7959, -80.2871],
    #Canada
    "YVR":[49.1967, -123.1815],
    "YYZ":[43.6777, -79.6248],
    #Europe
    "DUB":[53.4264, -6.2499],
    "MAD":[40.4983, -3.5676],
    "LHR":[51.4700, 0.4543],
    "CDG":[49.0139, 2.5425],
    "FRA":[50.0379, 8.5622],
    "FCO":[41.7999, 12.2462],
    "CPH":[55.6180, 12.6508],
    "VIE":[48.1126, 16.5755],
    "AIA":[37.9356, 23.9484],
    "SVO":[55.9736, 37.4125],
    #Near/Middle East
    "ISL":[40.9830, 28.8104],
    "DOH":[25.2609, 51.6138],
    "DXB":[25.2532, 55.3657],
    #Far East
    "BKK":[13.6900, 100.7501],
    "SIN":[1.3644, 103.9915],
    "HKG":[22.3080, 113.9185],
    "PVG":[31.1443, 121.8083],
    "PEK":[40.0799, 116.6031],
    "TPE":[25.0797, 121.2342],
    "ICN":[37.4602, 126.4407],
    "NRT":[35.7720, 140.3929]
}

max_planes = 12000
# keep track of which plane ID numbers are in use
plane_ids = [False for i in range(max_planes)]
small_planes = []
big_planes = []
planes = []
planes_by_id = {}
for a in airlines:
    planes_by_id[a] = [None for i in range(max_planes)]

flights = []

booking_agents = []

customers = []

tickets = []

def executeQuery(query, arguments=None):
    # cursor = conn.cursor()
    # if arguments:
    #     cursor.execute(query, arguments)
    # else:
    #     cursor.execute(query)
    # conn.commit()
    # cursor.close()
    pass

def clearDatabase():
    """Removes all rows of undesired data but preserves structure of database tables. In our case, we want to remove all data except for airline staff and admins (since we want to keep at least one easy-to-type username-password combination, for use in debugging), however we then re-insert the same names for airlines and airports as these are not auto-generated"""

    #I originally did 'DELETE FROM %s' but this doesn't work with PYMYSQL as the table name requires ``

    queries = ['DELETE FROM `ticket`', 'DELETE FROM `flight`', 'DELETE FROM `airplane`', 'DELETE FROM `airport`', 'DELETE FROM `airline`', 'DELETE FROM `customer`', 'DELETE FROM `booking_agent`']
    for q in queries:
        executeQuery(q)

def addAirlines():
    # query = 'INSERT INTO `airline` (`name`) VALUES ('
    # for i in range(len(airlines)-1):
    #     query += airlines[i] + ', '
    # query += airlines[len(airlines)-1] + ');'
    # executeQuery(query)
    for a in airlines:
        query = 'INSERT INTO `airline` (`name`) VALUES (%s);'
        executeQuery(query, (a))

def addAirports():
    # query = 'INSERT INTO `airport` (`code`) VALUES ('
    # for i in range(len(airports)-1):
    #     query += airports[i] + ', '
    # query += airports[len(airports)-1] + ');'
    # executeQuery(query)
    for a in airports:
        query = 'INSERT INTO `airport` (`code`, `name`, `city`, `state`, `country`, `is_international`, `longitude`, `latitude`, `gmt_difference`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'
        executeQuery(query, (a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7]))

def generatePlanes():
    global small_planes, big_planes, planes, planes_by_id

    # keep track of which plane ID numbers are in use
    nums = [False for i in range(max_planes)]

    generateSmallPlanes(50)
    generateBigPlanes(70, 5000)

def generateSmallPlanes(howmany):
    global plane_ids, small_planes, planes, planes_by_id

    for i in range(howmany):
        # generate a random plane ID number. If already in use, re-roll
        new_id = randint(0, howmany*100)
        while plane_ids[new_id]:
            new_id = randint(0, howmany*100)

        plane_ids[new_id] = True # mark this plane ID as being used

        # pad with leading zeros to get a 5-digit ID number string
        new_id_str = str(new_id).zfill(5)

        seats = randint(100, 250)
        airline = airlines[randint(0, len(airlines)-1)]

        newplane = (new_id_str, airline, seats)
        small_planes.append(newplane)
        planes.append(newplane)
        planes_by_id[airline][new_id] = newplane

def generateBigPlanes(howmany, id_start):
    global plane_ids, small_planes, planes, planes_by_id

    for i in range(howmany):
        new_id = randint(id_start, max_planes-1)
        while plane_ids[new_id] is True:
            new_id = randint(5000, max_planes-1)
        plane_ids[new_id] = True

        # pad with leading zeros to get a 5-digit ID number string
        new_id_str = str(new_id).zfill(5)

        airline = airlines[randint(0, len(airlines)-1)]
        seats = randint(200, 399)

        newplane = (new_id_str, airline, seats)
        big_planes.append(newplane)
        planes.append(newplane)
        planes_by_id[airline][new_id] = newplane
    #print planes
    for i in planes:
        # print("INSERT INTO `airplane` (`id`, `airline_name`, `total_seats`) VALUES (%s, %s, %d);" % (i[0], i[1], i[2]))
        query = 'INSERT INTO `airplane` (`id`, `airline_name`, `total_seats`) VALUES (%s, %s, ' + str(i[2]) + ');'
        args = (i[0], i[1]) #for some reason doesn't work when using i[2] as well (which is an integer substituting in for "%d")
        executeQuery(query, args)


def generateFlights():
    global flights
    #'airport':[hours,minutes,price]
    times = {"JFK":[23,37,611], "ANC":[24,5,595], "DFW":[18,15,595], "DSM":[18,5,425], "HAM":[18,40,625], "HAN":[6,10,183],
                "PVG":[2,25,160], "IST":[16,15,495], "JLH":[12,40,303], "KHI":[13,55,695], "NRT":[6,15,338],
                "HKG":[3,25,200], "SEA":[11,50,375], "SFO":[15,45,403]
            }
    #flights
    for i in range(100):
        status = randint(0, 7) #0 is delayed, 1 and above are ontime
        is_early = randint(0, 75) #0-4 are early, rest are not; if early, takes delay_min as amount of minutes early (must be under 1 hour early)
        delay_hr = randint(0, 9) #x = 40 means 5 hours early, x = 38 or 36 means 4 hours early, x = 34 to 24 even means 3 hours early, 22 to 4 means 2 hours early, remaining (mainly odds) are 1 hour early
        delay_min = randint(0, 59)
        if is_early > 0 and is_early < 4:
            delay_min //= 2
        if delay_min < 10:
            delay_min = "0" + str(delay_min)
        if is_early < 4:
            flight_status = "early"
            delay = "-0:" + str(delay_min)
        else:
            if status > 0:
                flight_status = "ontime"
                delay = "null"
            else:
                flight_status = "delayed"
                if delay_hr == 40:
                    delay_hr = 5
                elif delay_hr >= 36 and delay_hr % 2 == 0:
                    delay_hr = 4
                elif delay_hr >= 24 and delay_hr % 2 == 0:
                    delay_hr = 3
                elif delay_hr >= 4 and delay_hr % 2 == 0:
                    delay_hr = 2
                else:
                    delay_hr = 1
                delay = str(delay_hr) + ":" + str(delay_min)

        start_airport = ""
        end_airport = ""
        while start_airport == end_airport or (start_airport not in ["PEK", "PVG", "HKG"] and end_airport not in ["PEK", "PVG", "HKG"]):
            start_airport = airports[randint(0, len(airports)-1)]
            end_airport = airports[randint(0, len(airports)-1)]
        start_yr = randint(2016, 2020)
        start_mo = randint(1, 12)
        start_dy = randint(1, 28)
        start_hr = randint(7, 22)
        start_mn = randint(0, 11) * 5
        start_sc = 0

        start_date = datetime.datetime(start_yr, start_mo, start_dy, start_hr, start_mn, start_sc)

        domestic = False

        if start_airport in ["PEK", "PVG", "HKG", "HAN", "NRT"] and end_airport in ["PEK", "PVG", "HKG", "HAN", "NRT"]: #Locations in East Asia, including China, Hanoi (HAN), and Tokyo (NRT), are close enough to count as domestic-length flights
            domestic = True
            plane = small_planes[randint(0, len(small_planes)-1)]
            if (start_airport == "PEK" and end_airport == "PVG") or (end_airport == "PEK" and start_airport == "PVG") or (start_airport == "HKG" and end_airport == "PVG") or (end_airport == "HKG" and start_airport == "PVG"):
                info = times["PVG"]
            elif (start_airport == "PEK" and end_airport == "HKG") or (end_airport == "PEK" and start_airport == "HKG"):
                info = times["HKG"]
            else:
                if start_airport in ["PEK", "PVG", "HKG"]:
                    info = times[end_airport]
                else:
                    info = times[start_airport]
            end_date = start_date + datetime.timedelta(hours=info[0], minutes=info[1]) + datetime.timedelta(hours=randint(-1, 1), minutes=randint(-59, 59))
            price = info[2] + (randint(-10000, 10000) / 100)
        else:
            plane = big_planes[randint(0, len(big_planes)-1)]
            if start_airport in ["PEK", "PVG", "HKG"]:
                info = times[end_airport]
            else:
                info = times[start_airport]
            end_date = start_date + datetime.timedelta(hours=info[0], minutes=info[1]) + datetime.timedelta(hours=randint(-3, 3), minutes=randint(-59, 59))
            price = info[2] + (randint(-20000, 20000) / 100)

        # start_airport = "" + start_airport + ""
        # end_airport = "" + end_airport + ""

        airline = airlines[randint(0, 2)]
        if airline == "China Eastern":
            flight_no = "MU"
            if domestic:
                num = randint(100, 399)
            else:
                num = randint(400, 999)
        elif airline == "Haley Airways":
            flight_no = "HY"
            if domestic:
                num = randint(1100, 1399)
            else:
                num = randint(1400, 1999)
        else:
            # flight_no = ["", "SM"]
            flight_no = "SM"
            if domestic:
                num = randint(2100, 2399)
            else:
                num = randint(2400, 2999)
        # flight_no.append(str(num))
        flight_no += str(num)
        # flight_no = "".join(flight_no)
        plane_num = generateAirplaneUsingAirline(airline)

        flight = (flight_no, airline, plane_num, price, start_airport, start_date.strftime("20%y-%m-%d %H:%M:%S"), end_airport, end_date.strftime("20%y-%m-%d %H:%M:%S"), flight_status, delay)
        flights.append(flight)
    #print flights
    for flight in flights:
        # print("INSERT INTO `flight` (`flight_no`, `airline_name`, `airplane_id`, `base_price`, `depart_from`, `depart_time`, `arrive_at`, `arrive_time`, `flight_status`, `delay_length`) VALUES (%s, %s, %s, %f, %s, %s, %s, %s, %s, %s);" % (flight[0], flight[1], flight[2], flight[3], flight[4], flight[5], flight[6], flight[7], flight[8], flight[9]))
        query = 'INSERT INTO `flight` (`flight_no`, `airline_name`, `airplane_id`, `base_price`, `depart_from`, `depart_time`, `arrive_at`, `arrive_time`, `flight_status`, `delay_length`) VALUES (%s, %s, %s, ' + '{0:.2f}'.format(flight[3]) + ', %s, %s, %s, %s, %s, %s);'
        args = (flight[0], flight[1], flight[2], flight[4], flight[5], flight[6], flight[7], flight[8], flight[9])
        executeQuery(query, args)

def generateAirplaneUsingAirline(airline):
    id = randint(0, max_planes-1)
    while planes_by_id[airline][id] is None:
        num = randint(0, max_planes-1)
    return planes_by_id[airline][id][0] #when not None, you get an airplane tuple, index 0 is the plane's number

def generateAgents():
    global booking_agents
    #booking agents
    booking_agent_nums = [False for i in range(10000)]
    for i in range(500):
        agent_id = randint(1000, 9999)
        while booking_agent_nums[agent_id] is True:
            agent_id = randint(1000, 9999)
        booking_agent_nums[agent_id] = True
        agent_id = str(agent_id)
        password = agent_id #lazy solution
        email = "agent" + agent_id + "@example.org"
        agent_id = choice(string.ascii_letters).lower() + agent_id + "00" #add random letter and trailing zeros
        booking_agents.append((email, password, agent_id))
    #print booking agents
    for i in booking_agents:
        # print("INSERT INTO `booking_agent` (`email`, `password`, `id`) VALUES (%s, %s, %s);" % (i[0], i[1], i[2]))
        query = 'INSERT INTO `booking_agent` (`email`, `password`, `id`) VALUES (%s, %s, %s);'
        args = (i[0], i[1], i[2])
        executeQuery(query, args)

def generateCustomers():
    global customers
    firsts = ["James", "David", "Christopher", "George", "Ronald", "John", "Richard", "Daniel",
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
        executeQuery(query, args)

def generateTickets():
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
        temp_flightdatetime = extractDatetime(f[5])
        if temp_flightdatetime == "wut":
            return
        temp_custticketsleft = 0
        currentBookingAgentId = None
        temp_thirtypercent = None
        credit_or_debit = None
        card_no = None
        expiration = None
        purchase_date_time = None
        customer_name = None
        customer_email = None
        for t in range(tickets_sold):
            if temp_custticketsleft == 0:
                temp_custticketsleft = makeTicketsNum()
                currentBookingAgentId = determineNewAgent()
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
            tickets.append((ticket_id, flight_no, airline, sold_price, credit_or_debit, card_no, customer_name, expiration.strftime("20%y-%m-%d"), purchase_date_time.strftime("20%y-%m-%d %H:%M:%S"), customer_email, currentBookingAgentId))
            temp_custticketsleft -= 1
            ticket_id += 1
    for t in tickets:
        # print("INSERT INTO `ticket` (`ticket_id`, `flight_no`, `airline_name`, `sold_price`, `credit_or_debit`, `card_no`, `cardholder`, `expiration`, `purchase_date_time`, `customer_email`, `booking_agent_id`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);" % (t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], t[10]))
        query = 'INSERT INTO `ticket` (`ticket_id`, `flight_no`, `airline_name`, `sold_price`, `credit_or_debit`, `card_no`, `cardholder`, `expiration`, `purchase_date_time`, `customer_email`, `booking_agent_id`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
        args = (t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], t[10])
        executeQuery(query, args)


# "INSERT INTO `ticket` (`ticket_id`, `flight_no`, `airline_name`, `sold_price`, `credit_or_debit`, `card_no`, `cardholder`, `expiration`, `purchase_date_time`, `customer_email`, `booking_agent_id`) VALUES ("048", "MU411", "China Eastern", "947.56", "debit", "100020003011", "Emre Yorgy", "2028-02-01", "2019-05-08 06:18:18", "boom@dotcom.com", "y268115");"


def extractDatetime(string):
    #example: "20%y-%m-%d %H:%M:%S"
    y = int(string[0:4])
    mth = int(string[5:7])
    d = int(string[8:10])
    h = int(string[11:13])
    mte = int(string[14:16])
    s = int(string[17:19])
    return datetime.datetime(y, mth, d, h, mte, s)

def makeTicketsNum():
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

def determineNewAgent():
    coinflip = randint(1, 7) #3 in 7 chance that a customer will use a booking agent (source: https://www.condorferries.co.uk/travel-agency-statistics)
    if coinflip <= 3:
        return booking_agents[randint(0, len(booking_agents)-1)][2] #gets the agent's ID
    else:
        return "null" #no agent for this customer

if __name__ == '__main__':
    clearDatabase()
    addAirlines()
    addAirports()
    generatePlanes()
    # generateFlights()
    # generateAgents()
    # generateCustomers()
    # generateTickets()
