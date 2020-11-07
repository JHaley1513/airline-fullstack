from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
from decimal import Decimal
import datetime
import sys
import os

app = Flask(__name__)

conn = pymysql.connect(host='localhost',
                       user='monty',
                       port = 8889,
                       password='some_pass',
                       db='airline_tickets',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

history = []

CUST_FIELDS =   ['email', 'name', 'password', 'password_again', 'building_no', 'street', 'city', 'state',
                'phone_no', 'passport_no', 'passport_country', 'passport_expiration', 'date_of_birth']
AGENT_FIELDS =  ['email', 'password', 'password_again', 'id']
STAFF_FIELDS =  ['username', 'password', 'password_again', 'first_name', 'last_name', 'date_of_birth', 'phone_no', 'airline_name']

currentUserType = 'guest'
info = {}

def executeQuery(query, parameters=None, fetchMultiple=False, queryType='select'):
    cursor = conn.cursor()
    if parameters:
        # if type(parameters) is not tuple and type(parameters) is not list and type(parameters) is not dict:
        #     raise TypeError('Invalid type for parameters:', type(parameters))
        cursor.execute(query, parameters)
    else:
        cursor.execute(query)
    if queryType == 'select':
        if not fetchMultiple:
            data = cursor.fetchone()
        else:
            data = cursor.fetchall()
    elif queryType == 'insert':
        conn.commit()
        data = None
    elif queryType == 'delete': #this was also taken care of in the "if parameters:" statement
        conn.commit()
        data = None
    else:
        raise ValueError('Unknown value for queryType:', queryType)
    cursor.close()
    return data

def addToHistory():
    global history
    currentPage = sys._getframe().f_code.co_name
    history.append(currentPage)
    # print(history)

def clearHistory():
    global history
    history = []

@app.route('/go-back')
def goBack():
    global history
    # print(history)
    history.pop() #removes the current page
    if len(history) > 0:
        previousPage = history.pop()
        return redirect(url_for(previousPage))
    else:
        return redirect(url_for('mainPage'))

# @app.route('/')
# def mainPage():
#     global info
#     if len(session) > 0:
#         updateInfo()
#         # print(session)
#         username = session['username']
#         print("Session currently active for user", username)
#     else: #the user is not logged in
#         clearInfo()
#         clearHistory()
#         username = 'GUEST'
#     addToHistory()
#     return render_template('index.html', username=username, userType=currentUserType, info=info)

#new
@app.route('/')
def mainPage():
    return render_template('index.html', info=info, airports=getAirportsBasicInfo(), today=getTodaysDate())

@app.route('/login')
def login():
    addToHistory()
    return render_template('login.html')

@app.route('/login-auth', methods=['GET', 'POST'])
def loginAuth():
    global currentUserType
    username = request.form['username']
    password = request.form['password']
    desiredUserType = request.form['userType']

    if desiredUserType == 'customer':
        query = 'SELECT * FROM `customer` WHERE email = %s AND password = %s' #for some reason, I'm required to hard-code the table names with `` backticks.
    elif desiredUserType == 'booking_agent':
        query = 'SELECT * FROM `booking_agent` WHERE email = %s AND password = %s'
    elif desiredUserType == 'airline_staff':
        query = 'SELECT * FROM `airline_staff` WHERE username = %s AND password = %s'
    else:
        raise ValueError('Unknown value for desiredUserType:', desiredUserType)

    # cursor = conn.cursor()
    # cursor.execute(query, (username, password))
    # data = cursor.fetchone()
    # cursor.close()
    data = executeQuery(query, (username, password))
    error = None
    if(data):
        #creates a session for the the user
        #session is a built in
        session['username'] = username
        currentUserType = desiredUserType
        return redirect(url_for('mainPage'))
        # return render_template('index.html')
    else:
        error = 'Invalid username or password'
        print(desiredUserType, username, password)
        return render_template('login.html', error=error)

@app.route('/register/select-user-type')
def selectUserType():
    addToHistory()
    return render_template('select_user_type.html')

@app.route('/register/register-by-type', methods=['GET', 'POST'])
def registerByType():
    addToHistory()

    desiredUserType = request.form['userType']

    if desiredUserType == 'customer':
        return render_template('register/customer_registration.html')
    elif desiredUserType == 'booking_agent':
        return render_template('register/agent_registration.html')
    elif desiredUserType == 'airline_staff':
        return render_template('register/staff_registration.html', allAirlines=getAirlines())
    raise ValueError('Unknown value for desiredUserType:', desiredUserType)

def getAirlines():
    query = 'SELECT name FROM `airline`'
    #potential BUG: add `` around name.
    dicts = executeQuery(query, fetchMultiple=True)
    airlines = [a['name'] for a in dicts]
    return airlines

@app.route('/register/register-auth-agent', methods=['GET', 'POST'])
def registerAuthAgent():
    error = ''
    def getAgentFields():
        #this is hard-coded and specific to each user type
        data = []
        password = ''
        for f in AGENT_FIELDS:
            field = request.form.get(f, False)
            if f == 'password':
                password = field
            elif f == 'password_again':
                if password != field:
                    error = 'password'
                    return None #the passwords don't match, must try again
                continue #don't add password twice
            data.append(field)
        return data

    email = request.form['email']
    if userExists(email, 'booking_agent'):
        error = "A user already exists with email address " + email
        return render_template('register/agent_registration.html', error=error)
    elif not validEmail(email):
        error = "Invalid email address: " + email
        return render_template('register/agent_registration.html', error=error)
    else:
        data = getAgentFields()
        if data:
            #the number of fields is different for each user type. For booking_agent, it's 3.
            if len(data) != 3:
                raise ValueError("Incorrect number of fields received from booking agent registration:", data)
            ins = 'INSERT INTO `booking_agent` VALUES(%s, %s, %s)'
            print(ins)
            executeQuery(ins, data, queryType="insert")
            clearHistory()
            return render_template('login.html')
        else:
            if error == 'password':
                error = "Passwords don't match"
            return render_template('register/agent_registration.html', error=error)

def validEmail(email):
    if frequencyOf(email, '@') != 1 or frequencyOf(email, '.') != 1:
        return False
    idx1 = email.index('@')
    idx2 = email.index('.')
    if idx1 > idx2:
        return False
    if idx1 == 0 or idx2 == len(email)-1:
        return False
    if not email[idx2+1:].isalpha():
        return False
    return True

def frequencyOf(string, character):
    count = 0
    for c in string:
        if c == character:
            count += 1
    return count

@app.route('/register/register-auth-staff', methods=['GET', 'POST'])
def registerAuthStaff():
    error = ''
    def getStaffFields():
        #this is hard-coded and specific to each user type
        data = []
        password = ''
        for f in STAFF_FIELDS:
            if f == 'phone_no':
                break
            field = request.form.get(f, False)
            if f == 'password':
                password = field
            elif f == 'password_again':
                if password != field:
                    error = 'password'
                    return None #the passwords don't match, must try again
                continue #don't add password twice
            if f == 'date_of_birth':
                if not field:
                    error = 'date'
                    return None
            data.append(field)
        # print(type(data[-1])) #datetime is a string
        phone = "" + request.form['phone1'] + request.form['phone2'] + request.form['phone3']
        data.append(phone)
        data.append(request.form['airline_name'])
        return data

    username = request.form['username']
    if userExists(username, 'airline_staff'):
        error = "A user already exists with username " + username
        return render_template('register/staff_registration.html', allAirlines=getAirlines(), error = error)
    elif username == 'GUEST':
        error = "Username GUEST is already taken " + username
        return render_template('register/staff_registration.html', allAirlines=getAirlines(), error = error)
    else:
        print("Boom")
        data = getStaffFields()
        print("Data:",data)
        if data:
            #the number of fields is different for each user type. For airline_staff, it's 7.
            if len(data) != 7:
                raise ValueError("Incorrect number of fields received from staff registration:", data)
            ins = 'INSERT INTO `airline_staff` VALUES(%s, %s, %s, %s, %s, %s, %s)'
            # cursor = conn.cursor()
            # cursor.execute(ins, data)
            # conn.commit()
            # cursor.close()
            executeQuery(ins, data)
            clearHistory()
            return render_template('login.html')
        else:
            if error == 'password':
                error = "Passwords don't match"
            elif error == 'date':
                error = 'Invalid birthdate'
            return render_template('register/staff_registration.html', allAirlines=getAirlines(), error = error)

def userExists(username, desiredUserType): #username is email for customer and booking_agent
    if desiredUserType == 'customer':
        query = 'SELECT * FROM `customer` WHERE email = %s'
    elif desiredUserType == 'booking_agent':
        query = 'SELECT * FROM `booking_agent` WHERE email = %s'
    elif desiredUserType == 'airline_staff':
        query = 'SELECT * FROM `airline_staff` WHERE username = %s'
    else:
        raise ValueError('Unknown value for desiredUserType:', desiredUserType)
    user = executeQuery(query, (username))
    return user is not None

def updateInfo():
    global info
    newInfo = {}
    username = session['username']
    if currentUserType == 'customer':
        email = username
        newInfo['name'] = getCustomerName(email)
        newInfo['email'] = email
        newInfo['flights'] = customerGetFlights(email)
        newInfo['temp_flights'] = None
        newInfo['temp_index'] = None
    elif currentUserType == 'booking_agent':
        email = username
        newInfo['email'] = email
        agent_id = getAgentId(email)
        newInfo['id'] = agent_id
        newInfo['commission_by_ticket'] = getCommissionByTicket(agent_id)
        newInfo['commission_thirty_days'] = getCommissionLastThirtyDays(agent_id)
        newInfo['flights'] = agentGetFlights(agent_id)
        newInfo['top_customers'] = agentGetTopCustomers(agent_id)
        newInfo['temp_flights'] = None
        newInfo['temp_index'] = None
    elif currentUserType == 'airline_staff':
        airlineName = getAirlineName()
        newInfo['airline_name'] = airlineName
        newInfo['sales_reports'] = getSalesReports(airlineName)
        newInfo['revenue_comparisons'] = getRevenueComparisons(airlineName)
        newInfo['top_destinations'] = getTopDestinations(airlineName)
        newInfo['frequent_customers'] = getFrequentCustomers(airlineName)
        newInfo['all_customers'] = getAllCustomers(airlineName)
        newInfo['customer_emails_and_names'] = getCustomerEmailsAndNames(airlineName)
        newInfo['top_booking_agents'] = getTopBookingAgents()
        newInfo['airports'] = getAirports()
        newInfo['airplanes'] = getAirplanes(airlineName)
        newInfo['flights'] = airlineGetFlights(airlineName)
    else:
        raise ValueError('Unknown value for currentUserType:', currentUserType)
    info = newInfo

def clearInfo():
    global info
    if len(info) > 0:
        info = {}

def accessDenied():
    error = "You are not authorized to perform this action."
    if currentUserType != 'guest':
        session.pop('username')
    return render_template('login.html', error=error)

########################################## CUSTOMER ###########################################
###############################################################################################
def getCustomerName(email):
    query = 'SELECT name FROM `customer` WHERE email = %s'
    customerDict = executeQuery(query, email)
    return customerDict['name']

def customerGetFlights(email):
    query = 'SELECT ticket.airline_name, ticket.flight_no, depart_from, arrive_at, depart_time, arrive_time FROM `ticket` inner join `flight` ON ticket.flight_no=flight.flight_no AND ticket.airline_name=flight.airline_name WHERE customer_email = %s AND depart_time > NOW()'
    flights = executeQuery(query, email, fetchMultiple=True)
    return flights

@app.route('/view-my-flights')
def viewMyFlights():
    if len(session) == 0 or currentUserType != 'customer':
        return accessDenied()
    return render_template('customer/view_flights.html', info=info)

# @app.route('/search-flights')
# def searchFlights():
#     if len(session) == 0 or currentUserType != 'customer':
#         return accessDenied()
#     return render_template('customer/search_for_flights.html', info=info, airports=getAirports(), today=getTodaysDate())

@app.route('/search-flights-within-dates', methods=['GET', 'POST'])
def searchFlightsWithinDates():
    global info
    if len(session) == 0 or currentUserType != 'customer':
        return accessDenied()
    fromAirport = request.form['fromAirport']
    toAirport = request.form['toAirport']
    if fromAirport == toAirport:
        error = 'Cannot depart and arrive at the same airport.'
        return render_template('customer/search_for_flights.html', info=info, airports=getAirports(), today=getTodaysDate(), error=error)
    start = request.form['start'] #returns a string of format 'YYYY-MM-DD' including the dashes
    end = request.form['end']
    if len(start) != 10 or start[4] != '-' or start[7] != '-' or len(end) != 10 or end[4] != '-' or end[7] != '-':
        error = 'Invalid dates: START: %s, END: %s' % (start, end)
        return render_template('customer/search_for_flights.html', info=info, airports=getAirports(), today=getTodaysDate(), error=error)
    startDate = datetime.datetime(int(start[:4]), int(start[5:7]), int(start[8:]))
    endDate = datetime.datetime(int(end[:4]), int(end[5:7]), int(end[8:]))
    if startDate > endDate:
        error = 'Start date ' + start + ' comes after end date ' + end
        return render_template('customer/search_for_flights.html', info=info, airports=getAirports(), today=getTodaysDate(), error=error)
    todaysDate = datetime.datetime.today()
    if endDate < todaysDate:
        error = 'Can only search for future flights, range ' + start + ' to ' + end + ' is invalid.'
        return render_template('customer/search_for_flights.html', info=info, airports=getAirports(), today=getTodaysDate(), error=error)
    flights = getFlightsWithinDates(startDate, endDate, fromAirport, toAirport)
    info['temp_flights'] = flights
    return render_template('customer/search_for_flights.html', info=info, airports=getAirports(), today=getTodaysDate(), flights=flights)

@app.route('/confirm-booking', methods=['GET', 'POST'])
def confirmBooking():
    global info
    if len(session) == 0 or currentUserType != 'customer':
        return accessDenied()
    addToHistory()
    index = int(request.form['flight'])
    info['temp_index'] = index
    desiredFlight = info['temp_flights'][index]
    return render_template('customer/confirm_booking.html', info=info, desiredFlight=desiredFlight)

@app.route('/reserve-tickets', methods=['GET', 'POST'])
def reserveTickets():
    global info
    if len(session) == 0 or currentUserType != 'customer':
        return accessDenied()

    query = 'SELECT max(ticket_id) as ticket_id from `ticket`'
    old_max_id = executeQuery(query)
    old_max_id = old_max_id['ticket_id']

    flight = info['temp_flights'][info['temp_index']] #returns a dictionary

    date = request.form['expiration']
    year = int(date[:4])
    month = int(date[5:7])
    print(year, month)
    expiration = datetime.date(year, month, 1).strftime("20%y-%m-%d")

    ins = 'INSERT INTO `ticket` (`ticket_id`, `flight_no`, `airline_name`, `sold_price`, `credit_or_debit`, `card_no`, `cardholder`, `expiration`, `purchase_date_time`, `customer_email`, `booking_agent_id`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s, %s)'
    executeQuery(ins, (str(int(old_max_id)+1), flight['flight_no'], flight['airline_name'], flight['base_price'], request.form['credit_or_debit'], request.form['card_no'], request.form['cardholder'], expiration, info['email'], None), queryType='insert')
    message = "Flight successfully booked."
    return render_template('customer/view_flights.html', info=info, message=message)

@app.route('/track-my-spending')
def trackMySpending():
    if len(session) == 0 or currentUserType != 'customer':
        return accessDenied()
    return render_template('customer/track_my_spending.html', info=info)



######################################## BOOKING AGENT ########################################
###############################################################################################



def getAgentId(email):
    query = 'SELECT id FROM `booking_agent` WHERE email = %s'
    agentDict = executeQuery(query, email)
    return agentDict['id']

def getCommissionByTicket(agent_id):
    query = 'SELECT sold_price * 0.1 as commission FROM `ticket` WHERE booking_agent_id = %s'
    commissions = executeQuery(query, agent_id, fetchMultiple=True) #list of dicts
    return commissions

def getCommissionLastThirtyDays(agent_id):
    thirtyDays = {}
    query = 'SELECT sold_price * 0.1 as commission FROM `ticket` WHERE booking_agent_id = %s AND purchase_date_time BETWEEN NOW() - INTERVAL 30 DAY AND NOW()'
    commissions = executeQuery(query, agent_id, fetchMultiple=True) #list of dicts
    totalCommission = 0
    totalTickets = 0
    for c in commissions:
        totalCommission += c['commission']
        totalTickets += 1
    thirtyDays['total_commission'] = '{:.2f}'.format(totalCommission)
    if totalTickets > 0:
        thirtyDays['avg_commission'] = '{:.2f}'.format(totalCommission / totalTickets)
    thirtyDays['total_tickets'] = totalTickets
    return thirtyDays

def agentGetFlights(agent_id):
    query = 'SELECT ticket.airline_name, ticket.flight_no, depart_from, arrive_at, depart_time, arrive_time, customer_email, sold_price * 0.1 as commission FROM `ticket` inner join `flight` ON ticket.flight_no=flight.flight_no AND ticket.airline_name=flight.airline_name  WHERE booking_agent_id = %s AND depart_time > NOW()'
    flights = executeQuery(query, agent_id, fetchMultiple=True)
    return flights

def agentGetTopCustomers(agent_id):
    topCustomers = {}
    ticketsSixMonths = 'SELECT customer_email as email, count(customer_email) as num_tickets FROM `ticket` WHERE booking_agent_id = %s AND purchase_date_time BETWEEN NOW() - INTERVAL 6 MONTH AND NOW() GROUP BY email ORDER BY num_tickets DESC LIMIT 5'
    topCustomers['tickets_six_months'] = executeQuery(ticketsSixMonths, agent_id, fetchMultiple=True)
    ticketsYear = 'SELECT customer_email as email, count(customer_email) as num_tickets FROM `ticket` WHERE booking_agent_id = %s AND purchase_date_time BETWEEN NOW() - INTERVAL 1 YEAR AND NOW() GROUP BY email ORDER BY num_tickets DESC LIMIT 5'
    topCustomers['tickets_year'] = executeQuery(ticketsYear, agent_id, fetchMultiple=True)
    commissionSixMonths = 'SELECT customer_email as email, sum(sold_price) * 0.1 as commission FROM `ticket` WHERE booking_agent_id = %s AND purchase_date_time BETWEEN NOW() - INTERVAL 6 MONTH AND NOW() GROUP BY email ORDER BY commission DESC LIMIT 5'
    topCustomers['commission_six_months'] = executeQuery(commissionSixMonths, agent_id, fetchMultiple=True)
    commissionYear = 'SELECT customer_email as email, sum(sold_price) * 0.1 as commission FROM `ticket` WHERE booking_agent_id = %s AND purchase_date_time BETWEEN NOW() - INTERVAL 1 YEAR AND NOW() GROUP BY email ORDER BY commission DESC LIMIT 5'
    topCustomers['commission_year'] = executeQuery(commissionYear, agent_id, fetchMultiple=True)
    return topCustomers

@app.route('/agent-view-flights')
def agentViewFlights():
    if len(session) == 0 or currentUserType != 'booking_agent':
        return accessDenied()
    return render_template('agent/view_my_flights.html', info=info)

@app.route('/agent-search-flights')
def agentSearchFlights():
    if len(session) == 0 or currentUserType != 'booking_agent':
        return accessDenied()
    addToHistory()
    return render_template('agent/search_flights.html', info=info, airports=getAirports(), today=getTodaysDate())

@app.route('/agent-search-flights-within-dates', methods=['GET', 'POST'])
def agentSearchFlightsWithinDates():
    global info
    if len(session) == 0 or currentUserType != 'booking_agent':
        return accessDenied()
    fromAirport = request.form['fromAirport']
    toAirport = request.form['toAirport']
    if fromAirport == toAirport:
        error = 'Cannot depart and arrive at the same airport.'
        return render_template('agent/search_flights.html', info=info, airports=getAirports(), today=getTodaysDate(), error=error)
    start = request.form['start'] #returns a string of format 'YYYY-MM-DD' including the dashes
    end = request.form['end']
    if len(start) != 10 or start[4] != '-' or start[7] != '-' or len(end) != 10 or end[4] != '-' or end[7] != '-':
        error = 'Invalid dates: START: %s, END: %s' % (start, end)
        return render_template('agent/search_flights.html', info=info, airports=getAirports(), today=getTodaysDate(), error=error)
    startDate = datetime.datetime(int(start[:4]), int(start[5:7]), int(start[8:]))
    endDate = datetime.datetime(int(end[:4]), int(end[5:7]), int(end[8:]))
    if startDate > endDate:
        error = 'Start date ' + start + ' comes after end date ' + end
        return render_template('agent/search_flights.html', info=info, airports=getAirports(), today=getTodaysDate(), error=error)
    todaysDate = datetime.datetime.today()
    if endDate < todaysDate:
        error = 'Can only search for future flights, range ' + start + ' to ' + end + ' is invalid.'
        return render_template('agent/search_flights.html', info=info, airports=getAirports(), today=getTodaysDate(), error=error)
    flights = getFlightsWithinDates(startDate, endDate, fromAirport, toAirport)
    info['temp_flights'] = flights
    return render_template('agent/search_flights.html', info=info, airports=getAirports(), today=getTodaysDate(), flights=flights)

def getFlightsWithinDates(start, end, depart, arrive):
    query = 'SELECT airline_name, flight_no, depart_from, arrive_at, depart_time, arrive_time, base_price FROM `flight` WHERE depart_time >= %s AND depart_time <= %s'
    return executeQuery(query, (start, end), fetchMultiple=True) #list of dicts

@app.route('/agent-confirm-booking', methods=['GET', 'POST'])
def agentConfirmBooking():
    global info
    if len(session) == 0 or currentUserType != 'booking_agent':
        return accessDenied()
    addToHistory()
    index = int(request.form['flight'])
    info['temp_index'] = index
    desiredFlight = info['temp_flights'][index]
    return render_template('agent/confirm_agent_booking.html', info=info, desiredFlight=desiredFlight)

@app.route('/agent-reserve-tickets', methods=['GET', 'POST'])
def agentReserveTickets():
    global info
    if len(session) == 0 or currentUserType != 'booking_agent':
        return accessDenied()
    email = request.form['customer_email']

    query = 'SELECT credit_or_debit, card_no, cardholder, expiration FROM `ticket` WHERE customer_email=%s'
    cust_info = executeQuery(query, email)
    if not cust_info:
        error = 'No payment information on file for customer with email ' + email
        history.pop() #remove the previous confirmation page
        return render_template('agent/search_flights.html', info=info, airports=getAirports(), today=getTodaysDate(), error=error)

    query = 'SELECT max(ticket_id) as ticket_id from `ticket`'
    old_max_id = executeQuery(query)
    print(old_max_id)
    old_max_id = old_max_id['ticket_id']

    flight = info['temp_flights'][info['temp_index']] #returns a dictionary

    ins = 'INSERT INTO `ticket` (`ticket_id`, `flight_no`, `airline_name`, `sold_price`, `credit_or_debit`, `card_no`, `cardholder`, `expiration`, `purchase_date_time`, `customer_email`, `booking_agent_id`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s, %s)'
    executeQuery(ins, (str(int(old_max_id)+1), flight['flight_no'], flight['airline_name'], flight['base_price'], cust_info['credit_or_debit'], cust_info['card_no'], cust_info['cardholder'], cust_info['expiration'], email, info['id']), queryType='insert')
    message = "Flight successfully booked."
    return render_template('agent/view_my_flights.html', info=info, message=message)

@app.route('/view-my-commission')
def viewMyCommission():
    if len(session) == 0 or currentUserType != 'booking_agent':
        return accessDenied()
    return render_template('agent/view_commission.html', info=info, today=getTodaysDate())

@app.route('/view-commission-within-dates', methods=['GET', 'POST'])
def viewCommissionWithinDates():
    if len(session) == 0 or currentUserType != 'booking_agent':
        return accessDenied()

    start = request.form['start'] #returns a string of format 'YYYY-MM-DD' including the dashes
    end = request.form['end']
    if len(start) != 10 or start[4] != '-' or start[7] != '-' or len(end) != 10 or end[4] != '-' or end[7] != '-':
        error = 'Invalid dates: START: %s, END: %s' % (start, end)
        return render_template('agent/view_commission.html', info=info, today=getTodaysDate(), error=error)
    startDate = datetime.datetime(int(start[:4]), int(start[5:7]), int(start[8:]))
    endDate = datetime.datetime(int(end[:4]), int(end[5:7]), int(end[8:]))
    if startDate > endDate:
        error = 'Start date ' + start + ' comes after end date ' + end
        return render_template('agent/view_commission.html', info=info, today=getTodaysDate(), error=error)
    commission = getCommissionWithinDates(info['id'], startDate, endDate)
    print(commission)
    return render_template('agent/view_commission.html', info=info, start=start, end=end, commission=commission)

def getCommissionWithinDates(agent_id, start, end):
    commission = {}
    query = 'SELECT sold_price * 0.1 as commission FROM `ticket` WHERE booking_agent_id = %s AND purchase_date_time >= %s AND purchase_date_time <= %s'
    commissions = executeQuery(query, (agent_id, start, end), fetchMultiple=True) #list of dicts
    totalCommission = 0
    totalTickets = 0
    for c in commissions:
        totalCommission += c['commission']
        totalTickets += 1
    commission['total_commission'] = '{:.2f}'.format(totalCommission)
    if totalTickets > 0:
        commission['avg_commission'] = '{:.2f}'.format(totalCommission / totalTickets)
    commission['total_tickets'] = totalTickets
    return commission

def getTodaysDate():
    return datetime.datetime.now().date().strftime("20%y-%m-%d")

@app.route('/agent-view-top-customers')
def agentViewTopCustomers():
    if len(session) == 0 or currentUserType != 'booking_agent':
        return accessDenied()
    return render_template('agent/view_top_customers.html', info=info)



######################################## AIRLINE STAFF ########################################
###############################################################################################



def getAirlineName():
    username = session['username']
    if currentUserType == 'airline_staff':
        query = 'SELECT airline_name FROM `airline_staff` WHERE username = %s'
    else:
        raise ValueError('Can only get airline name for airline_staff, not for', currentUserType)
    result = executeQuery(query, (username))
    if result:
        return result['airline_name']
    else:
        return 'NULL AIRLINE'

def getSalesReports(airlineName):
    #list of length 3: [{'year':{'start_date':'', 'end_date':'', 'tickets_sold':XX}}, {'month': ...}, {'custom': ...}]. Custom points to None if not specified (default)
    return None

def getCustomerEmailsAndNames(airlineName):
    query = 'SELECT distinct(email), name FROM `customer`, `ticket` where email = customer_email and airline_name = %s'
    dicts = executeQuery(query, (airlineName), fetchMultiple=True)
    emailsAndNames = {}
    for d in dicts:
        email, name = d['email'], d['name']
        emailsAndNames[email] = name
    return emailsAndNames

def getRevenueComparisons(airlineName):
    #Each query returns a list containing one dict. Each dict is {'total': Decimal('XX.XX'})
    queryWithAgent = 'SELECT sum(sold_price) as total FROM `ticket` WHERE airline_name = %s and booking_agent_id is not null'
    totalWithAgent = executeQuery(queryWithAgent, (airlineName), fetchMultiple=True)
    if not totalWithAgent:
        totalWithAgent = {'total': Decimal('0.0')}

    queryWithoutAgent = 'SELECT sum(sold_price) as total FROM `ticket` WHERE airline_name = %s and booking_agent_id is null'
    totalWithoutAgent = executeQuery(queryWithoutAgent, (airlineName), fetchMultiple=True)
    if not totalWithoutAgent[0]['total']:
        totalWithoutAgent = [{'total': Decimal('0.0')}]

    return {'total_with_agent': totalWithAgent[0]['total'], 'total_without_agent': totalWithoutAgent[0]['total']}

def getTopDestinations(airlineName): #for last three months and last year
    #each result is a list of dicts.
    queryThreeMonths = 'SELECT arrive_at as destination, count(arrive_at) as num_customers FROM `ticket` natural join `flight` WHERE airline_name = %s AND depart_time BETWEEN NOW() - INTERVAL 3 MONTH AND NOW() GROUP BY destination ORDER BY num_customers DESC LIMIT 3'
    pastThreeMonths = executeQuery(queryThreeMonths, (airlineName), fetchMultiple=True)

    queryYear = 'SELECT arrive_at as destination, count(arrive_at) as num_customers FROM `ticket` natural join `flight` WHERE airline_name = %s AND depart_time BETWEEN NOW() - INTERVAL 1 YEAR AND NOW() GROUP BY destination ORDER BY num_customers DESC LIMIT 3'
    pastYear = executeQuery(queryYear, (airlineName), fetchMultiple=True)
    print({'past_three_months': pastThreeMonths, 'past_year': pastYear})
    return {'past_three_months': pastThreeMonths, 'past_year': pastYear}

def getFrequentCustomers(airlineName):
    query = 'SELECT name, email, count(email) as total_flights FROM `ticket`, `customer` WHERE airline_name = %s and customer_email = email GROUP BY email ORDER BY total_flights DESC LIMIT 5'
    return executeQuery(query, airlineName, fetchMultiple=True) #returns a list of dicts, with keys 'name', 'email' and 'total_flights'

def getAllCustomers(airlineName):
    query = 'SELECT distinct email, name FROM `ticket`, `customer` WHERE airline_name = %s and customer_email = email'
    return executeQuery(query, airlineName, fetchMultiple=True) #returns a list of dicts, with keys 'name' and 'email'

def getTopBookingAgents():
    topAgents = {}
    #Keys in topAgents: 'tickets_month', 'tickets_year', 'commission_month', 'commission_year'. Values are lists of length <= 5
    query = 'SELECT COUNT(booking_agent_id) as tickets_this_month, booking_agent_id FROM `ticket` WHERE booking_agent_id IS NOT NULL AND purchase_date_time BETWEEN NOW() - INTERVAL 1 MONTH AND NOW() GROUP BY booking_agent_id ORDER BY tickets_this_month DESC LIMIT 5'
    ticketsMonth = executeQuery(query, fetchMultiple=True)
    #ticketsMonth is a list of dicts.
    temp = [] #ordered list of lists, from most to least revenue. Each inner list represents one agent.
    for d in ticketsMonth:
        innertemp = [] #innertemp[0] = booking_agent_id, innertemp[1] = commission/tickets_sold
        innertemp.append( d['booking_agent_id'])
        innertemp.append( d['tickets_this_month'])
        temp.append(innertemp)
    topAgents['tickets_month'] = temp

    query = 'SELECT COUNT(booking_agent_id) as tickets_this_year, booking_agent_id FROM `ticket` WHERE booking_agent_id IS NOT NULL AND purchase_date_time BETWEEN NOW() - INTERVAL 1 YEAR AND NOW() GROUP BY booking_agent_id ORDER BY tickets_this_year DESC LIMIT 5'
    ticketsYear = executeQuery(query, fetchMultiple=True)
    temp = []
    for d in ticketsYear:
        innertemp = []
        innertemp.append( d['booking_agent_id'])
        innertemp.append( d['tickets_this_year'])
        temp.append(innertemp)
    topAgents['tickets_year'] = temp

    query = 'SELECT SUM(sold_price) as revenue_this_month, booking_agent_id FROM `ticket` WHERE booking_agent_id IS NOT NULL AND purchase_date_time BETWEEN NOW() - INTERVAL 1 MONTH AND NOW() GROUP BY booking_agent_id ORDER BY revenue_this_month DESC LIMIT 5'
    revenueMonth = executeQuery(query, fetchMultiple=True)
    temp = []
    for d in revenueMonth:
        innertemp = []
        commission = d['revenue_this_month'] * Decimal('0.1')
        innertemp.append( d['booking_agent_id'])
        innertemp.append( commission )
        temp.append(innertemp)
    topAgents['commission_month'] = temp

    query = 'SELECT SUM(sold_price) as revenue_this_year, booking_agent_id FROM `ticket` WHERE booking_agent_id IS NOT NULL AND purchase_date_time BETWEEN NOW() - INTERVAL 1 YEAR AND NOW() GROUP BY booking_agent_id ORDER BY revenue_this_year DESC LIMIT 5'
    revenueYear = executeQuery(query, fetchMultiple=True)
    temp = []
    for d in revenueYear:
        innertemp = []
        commission = d['revenue_this_year'] * Decimal('0.1')
        innertemp.append( d['booking_agent_id'])
        innertemp.append( commission )
        temp.append(innertemp)
    topAgents['commission_year'] = temp
    return topAgents

def getAirports():
    query = 'SELECT code, name FROM `airport`'
    airports = executeQuery(query, fetchMultiple=True)
    return airports

#new
def getAirportsBasicInfo():
    query = 'SELECT code, name, city, state, country FROM `airport`'
    airports = executeQuery(query, fetchMultiple=True)
    return airports

def getAirplanes(airlineName):
    query = 'SELECT id, total_seats FROM `airplane` where airline_name = %s'
    airplanes = executeQuery(query, (airlineName), fetchMultiple=True)
    return airplanes

def airlineGetFlights(airlineName):
    query = 'SELECT airline_name, airplane_id, flight_no, depart_from, arrive_at, depart_time, arrive_time, base_price, flight_status, delay_length FROM `flight` WHERE airline_name = %s'
    flights = executeQuery(query, airlineName, fetchMultiple=True)
    print(flights)
    return flights

def airlineDeleteFlights(airlineName):
    pass


########################################## Statistics ##########################################



@app.route('/view-sales-reports')
def viewSalesReports():
    if len(session) == 0 or currentUserType != 'airline_staff':
        return accessDenied()

    addToHistory()
    return render_template('statistics/sales_reports.html', info=info)

@app.route('/view-revenue-comparisons')
def viewRevenueComparisons():
    if len(session) == 0 or currentUserType != 'airline_staff':
        return accessDenied()

    addToHistory()
    return render_template('statistics/revenue_comparisons.html', info=info)

@app.route('/view-top-destinations')
def viewTopDestinations():
    if len(session) == 0 or currentUserType != 'airline_staff':
        return accessDenied()

    addToHistory()
    return render_template('statistics/top_destinations.html', info=info)

@app.route('/view-frequent-customers')
def viewFrequentCustomers():
    if len(session) == 0 or currentUserType != 'airline_staff':
        return accessDenied()

    addToHistory()
    return render_template('statistics/frequent_customers.html', info=info)

@app.route('/get-customer-flights', methods = ['GET', 'POST'])
def getCustomerFlights():
    if len(session) == 0 or currentUserType != 'airline_staff':
        return accessDenied()

    customerNameAndEmail = request.form['selected_customer']
    email = customerNameAndEmail.split()[-1]
    flightsQuery = 'SELECT flight_no, depart_from, arrive_at, depart_time, arrive_time, sold_price FROM `ticket` natural join `flight` where customer_email = %s and airline_name = %s'
    flights = executeQuery(flightsQuery, (email, info['airline_name']), fetchMultiple=True)
    return render_template('statistics/frequent_customers.html', info=info, email=email, flights=flights)

@app.route('/view-top-booking-agents')
def viewTopBookingAgents():
    if len(session) == 0 or currentUserType != 'airline_staff':
        return accessDenied()

    addToHistory()
    return render_template('statistics/top_booking_agents.html', info=info)



############################################ Flights ############################################



@app.route('/view-our-flights')
def viewOurFlights():
    if len(session) == 0 or currentUserType != 'airline_staff':
        return accessDenied()
    addToHistory()
    return render_template('view_our_flights.html', info=info)

@app.route('/edit-flight')
def editFlights():
    if len(session) == 0 or currentUserType != 'airline_staff':
        return accessDenied()

@app.route('/edit-flight-status')
def editFlightStatus():
    if len(session) == 0 or currentUserType != 'airline_staff':
        return accessDenied()

@app.route('/create-flight')
def createFlight():
    if len(session) == 0 or currentUserType != 'airline_staff':
        return accessDenied()



##################################### Airplanes & Airports #####################################



@app.route('/airports')
def airports():
    if len(session) == 0 or currentUserType != 'airline_staff':
        return accessDenied()
    addToHistory()
    return render_template('airports.html', info=info)

@app.route('/airport-insert-auth', methods=['GET', 'POST'])
def airportInsertAuth():
    global history, info
    if len(session) == 0 or currentUserType != 'airline_staff':
        return accessDenied()

    code = request.form['code']
    query = 'SELECT * FROM `airport` WHERE code = %s'
    data = executeQuery(query, (code))
    if data:
        error = "Airport " + code + " already exists."
        return render_template('airports.html', info=info, error=error)
    else:
        ins = 'INSERT INTO `airport` VALUES(%s, %s)'
        executeQuery(ins, (request.form['code'], request.form['name']))
        history.pop() #remove the previous record of the aiport page since we're going back there, to avoid duplicate history entries
        info['airports'] = getAirports() #get the updated airports data
        return render_template('airports.html', info=info)

@app.route('/airplanes')
def airplanes():
    if len(session) == 0 or currentUserType != 'airline_staff':
        return accessDenied()

    addToHistory()
    return render_template('airplanes.html', info=info)

@app.route('/airplane-insert-auth', methods=['GET', 'POST'])
def airplaneInsertAuth():
    global history, info
    if len(session) == 0 or currentUserType != 'airline_staff':
        return accessDenied()

    id_num = request.form['id']
    total_seats = request.form['total_seats']
    query = 'SELECT * FROM `airplane` WHERE id = %s'
    data = executeQuery(query, (id_num))
    if data:
        error = "Airplane with ID " + id_num + " already exists."
        return render_template('airplanes.html', info=info, error=error)
    else:
        ins = 'INSERT INTO `airplane` (id, airline_name, total_seats) VALUES(%s, %s, %s)'
        executeQuery(ins, (id_num, info['airline_name'], total_seats), queryType='insert')

        history.pop() #remove the previous record of the aiport page since we're going back there, to avoid duplicate history entries
        info['airplanes'] = getAirplanes(info['airline_name']) #get the updated airports data
        return render_template('airplanes.html', info=info)

@app.route('/logout')
def logout():
    global currentUserType
    session.pop('username')
    currentUserType = 'guest'
    return redirect('/')


app.secret_key = str(os.urandom(16))


#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    # extra_dirs = ['directory/to/watch',]
    # extra_files = extra_dirs[:]
    # for extra_dir in extra_dirs:
    #     for dirname, dirs, files in walk(extra_dir):
    #         for filename in files:
    #             filename = path.join(dirname, filename)
    #             if path.isfile(filename):
    #                 extra_files.append(filename)
    # app.run('127.0.0.1', 5000, debug=True, extra_files=extra_files)
	app.run('127.0.0.1', 5000, debug=True)
