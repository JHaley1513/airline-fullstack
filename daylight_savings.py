# only these US states/territories do not observe daylight savings
no_dst_usa = ["AZ", "HI", "AS", "GU", "MP", "PR", "VI"]

# These are all the major countries/regions that observe daylight savings.
dst_start_end = {
    #North America
    "United States": ["Mar second Sun 02:00", "Nov first Sun 02:00"],
    "Canada": ["Mar second Sun 02:00", "Nov first Sun 02:00"],
    "Mexico": ["Apr first Sun 02:00", "Oct last Sun 02:00"],
    #South America
    "Chile": ["Sep first Sun 00:00", "Apr first Sun 00:00"],
    #Europe - see below
    "Europe": ["Mar last Sun 01:00", "Oct last Sun 01:00"],
    #Asia
    "Iran": ["Mar 22 00:00", "Sep 22 00:00"],
    "Israel": ["Mar Fri before last Sun 02:00", "Oct last Sun 02:00"],
}

#All the countries in europe that follow dst (Russia, Belarus, Iceland and Turkey do not) follow it on the same schedule.
dst_europe = ["United Kingdom", "Ireland", "Portugal", "Spain", "France", "Belgium", "Netherlands", "Italy", "Switzerland", "Germany", "Norway", "Denmark", "Sweden", "Finland", "Poland", "Greece", "Austria", "Romania", "Czech Republic", "Ukraine"]



def is_daylight_savings(date_and_time, year, state, country):
    if country in dst_europe:
        is_within_dates(date_and_time, year, dst_start_end['Europe'])
    else:
        if country == 'United States':
            if state not in no_dst_usa:
                is_within_dates(date_and_time, year, dst_start_end['United States'])
        else:
            is_within_dates(date_and_time, year, dst_start_end[country])

def is_within_dates(date_and_time, year, start_end_datetimes): #start_end_dates is a list of length 2.
    start_datetime = extract_date_time(year, start_end_datetimes[0],)
    end_datetime = extract_date_time(year, start_end_datetimes[1],)
    #...

def extract_date(year, dateDescr):
    #example: "Mar 22 00:00" or "Mar Fri before last Sun 02:00"
    words = " ".split(dateDescr)
    month = words[0]
    if words[1].isnumeric(): #this is the day of the month
        day = int(words[1])
    else:
        rule = words[1:-2] #a rule like 'second Fri' or 'Fri before last Sun'
    time = words[-1] #like "02:00"
    hours = int(time[0:2])
    mins = int(time[2:4])
