# NOTE: All airlines generated using this script are fictional but are roughly based on real airlines with their countries served, aircraft sizes, and route patterns
airline_names = {
    "AA":"American Airways",
    "DL":"Omega Airlines",
    "UA":"Unity Airways",
    "EK":"Air Dubai",
    "CZ":"South China",
    "LH":"Luft von Hanse",
    "BA":"Britain Air",
    "AF":"Vol de France",
    "FR":"Bryan Airlines",
    "EC":"EZ Jet",
    "MU":"East China",
    "CA":"China Airways",
    "IB":"Aéreas de Iberia",
    "TK":"Turkish Airways",
    "ET":"Ethiopian Air",
    "AI":"India Air"
}

#To generate a flight, first we generate start and endpoints, then we roll a dice to see
#which airline it is. Each airline is based at a certain airport, meaning it's more likely to get flights
#close to that airport.
#We also designate certain airports in tiers, tier 3 are the 10 or so busiest international airports in the
#world, tier 2 are 10-50 or so. The rest are all tier 1.
airline_hubs = {
    "AA":"DFW",
    "DL":"ATL",
    "UA":"ORD",
    "EK":"DXB",
    "CZ":"SHA",
    "LH":"FRA",
    "BA":"LHR",
    "AF":"CDG",
    "FR":"DUB",
    "EC":"LGW",
    "MU":"SHA",
    "CA":"PEK",
    "IB":"MAD",
    "TK":"IST",
    "ET":"ADD",
    "AI":"DEL"
}

airline_planes = {
    #[number of planes, economy, economy_plus, business_class, first_class]
    "AA":[
        [133, 96, 24, 0 ,8],
        [48, 120, 18, 0, 12],
        [218, 123, 47, 0, 20],
        [328, 126, 30, 0, 16],
        [23, 138, 76, 20, 0],
        [69, 200, 55, 30, 0],
        [20, 188, 56, 52, 8]
        ],
    "DL":[
        [79, 178, 28, 0, 40],
        [53, 168, 56, 28, 29],
        [204, 142, 29, 0, 20],
        [130, 139, 21, 0, 20],
        [130, 139, 21, 0, 20],
        [129, 108, 36, 0, 16],
        [60, 102, 18, 0, 12],
        [99, 82 ,15, 0, 12]
        ],
    "UA":[],
    "EK":[],
    "CZ":[],
    "LH":[],
    "BA":[],
    "AF":[],
    "FR":[],
    "EC":[],
    "MU":[],
    "CA":[],
    "IB":[],
    "TK":[],
    "ET":[]
}

def airline_codes():
    for n in airline_names.keys():
        yield n

def get_airline_name(code):
    return airline_names[code]

def get_airline_hub(code):
    return airline_hubs[code]

def get_airline_planes(code):
    return airline_planes[code]

#Airplanes:
#There's 4 types of seats: First class, Business class, Premium Economy (aka Economy+) and Economy.
#Here's the breakdown by airline. Some planes aren't listed so their sum may differ from the airline's actual sum
#Southwest currently operates 495 143-seaters and 241 175-seaters, 736 total:
    #All are economy class
#AA currently operates 862 total:
    #133 128-seaters with 96 econ, 24 econ+, 8 1st
    #48 150-seaters with 120 econ, 18 econ+, 12 1st
    #218 190-seaters with 123 econ, 47 econ+, 20 1st
    #328 172-seaters with 126 e, 30 e+, 16 f
    #23 234-seaters with 138 e, 76 e+, 20 b
    #69 285-seaters with 200 e, 55 e+, 30 b
    #20 304-seaters with 188 e, 56 e+, 52 b, 8 f
#Omega has 761 total.
    #79 246-seaters with 178 e, 28 e+, 40 f
    #53 281-seaters with 168 e, 56 e+, 28 b, 29 f
    #204 191-seaters with 142 e, 29 e+, 20 f
    #130 180-seaters with 139 e, 21 e+, 20 f
    #130 180-seaters with 139 e, 21 e+, 20 f
    #129 160-seaters with 108 e, 36 e+, 16 f
    #60 132-seaters with 102 e, 18 e+, 12 f
    #99 109-seaters with 82 e, 15 e+, 12 f




#Statistics from IATA 2015 (published 2016) at https://www.iata.org/en/pressroom/pr/2016-07-05-01/

#Regions by total passengers:
#Asia-pacific 34%
#Europe 26%
#US/Canada 25%
#Latin America 7.5%
#Mid East 5.3%
#Africa 2.2%

#80% of seats filled

#According to US Bureau of Transport 2019 https://www.bts.gov/newsroom/2019-traffic-data-us-airlines-and-foreign-airlines-us-flights-final-full-year
#Passengers for:
#Domestic airlines domestic: 811 mil
#Domestic airlines to/from US: 115 mil
#International airlines to/from US: 126 mil

#According to the World Bank https://data.worldbank.org/indicator/IS.AIR.PSGR?most_recent_value_desc=true
#Worldwide had 4.233 billion airline passengers and 38 mil flights. We want to get it down to 420,000 passengers/tickets and therefore 3,800 flights (possibly fewer flights since we'll have a larger proportion of intl flights which typically have more passengers)
#China had 611 m
#

#Southwest had 158m domestic and 6m intl
#AA had 30m intl
#British Airways had 7m to/from US

#Atlanta: 47m domestic, 6m intl passengers
#JFK: 17m intl


#Airlines with most total passengers:
#AA - 146.5 mil
#Southwest - 144.6
#Omega - 138.8
#South China - 109.3
#Bryan - 101.4

#Airlines with most intl passenger-kilometers:
#"AA":"American Airways" - 321 mil passenger-kilometers
#"DL":"Omega Airlines"  - 303
#"UA":"Unity Airways"   - 295
#"EK":"Air Dubai"       - 251
#"CZ":"South China"     - 189
#"WN":"Air Southwest"   - 189
#"LH":"Luft von Hanse"  - 146
#"BA":"Britain Air"     - 141
#"AF":"Vol de France"   - 139
#"FR":"Bryan Airlines"  - 125


#Intl airport pairs
#HK-Taipei: 5 mil
#Jakarta-Singapore: 3.4
#Bangkok-HK: 3
#Kuala Lumpur-Singapore: 2.7
#HK-Singapore: 2.7
