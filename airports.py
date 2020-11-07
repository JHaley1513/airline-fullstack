# airport format: code, name (if any), city, state (or "null"), country, is_international (1=true), longitude,  latitude, gmt_difference (timezone)
# is_international is whether the airport has international flights.
# longitude is positive for E and negative for W, latitude is positive for N and negative for S.
airport_attr = [
    #United States (not incl. territories)
    ["HNL", "", "Honolulu", "HI", "United States", 1, 21.3245, -157.9251, -10],
    ["SFO", "", "San Francisco", "CA", "United States", 1, 37.6213, -122.3790, -8],
    ["SEA", "Seattle-Tacoma", "Seattle", "WA", "United States", 1, 47.4502, -122.3088, -8],
    ["LAX", "", "Los Angeles", "CA", "United States", 1, 33.9416, -118.4085, -8],
    ["LAS", "McCarran", "Las Vegas", "NV", "United States", 1, 36.2093, -115.1995, -8],
    ["PHX", "Sky Harbor", "Phoenix", "AZ", "United States", 1, 33.4373, -112.0078, -7],
    ["DFW", "Fort Worth", "Dallas", "TX", "United States", 1, 32.8998, -97.0403, -6],
    ["IAH", "George Bush Intercontinental", "Houston", "TX", "United States", 1, 29.9902, -95.3368, -6],
    ["MSP", "Minneapolis-St Paul", "Minneapolis", "MN", "United States", 1, 44.8848, -93.2223, -6],
    ["ORD", "O'Hare", "Chicago", "IL", "United States", 1, 41.9742, -87.9073, -6],
    ["ATL", "Hartsfield-Jackson", "Atlanta", "GA", "United States", 1, 33.6407, -84.4277, -5],
    ["DTW", "Wayne County", "Detroit", "MI", "United States", 1, 42.2162, -83.3554, -5],
    ["MCO", "", "Orlando", "FL", "United States", 1, 28.4312, -81.3081, -5],
    ["CLT", "Douglas", "Charlotte", "NC", "United States", 1, 35.2144, -80.9473, -5],
    ["MIA", "", "Miami", "FL", "United States", 1, 25.7959, -80.2871, -5],
    ["FLL", "", "Fort Lauderdale", "FL", "United States", 1, 26.0742, -80.1506, -5],
    ["BWI", "Baltimore Washington", "Baltimore", "MD", "United States", 1, 39.1774, -76.6684, -5],
    ["PHL", "", "Philadelphia", "PA", "United States", 1, 39.8744, -75.2424, -5],
    ["EWR", "Liberty", "Newark", "NJ", "United States", 1, 40.6895, -74.1745, -5],
    ["LGA", "LaGuardia", "New York", "NY", "United States", 1, 40.7769, -73.8740, -5],
    ["JFK", "John F Kennedy", "New York", "NY", "United States", 1, 40.6413, -73.7781, -5],
    ["BOS", "Logan", "Boston", "MA", "United States", 1, 42.3656, -71.0096, -5],
    #Canada
    ["YVR", "", "Vancouver", "BC", "Canada", 1, 49.1967, -123.1815, -8],
    ["YYC", "", "Calgary", "AB", "Canada", 1, 51.1215, -114.0076, -7],
    ["YYZ", "Pearson", "Toronto", "ON", "Canada", 1, 43.6777, -79.6248, -5],
    ["YUL", "Pierre Elliott Trudeau", "Montreal", "QC", "Canada", 1, 45.4657, -73.7455, -5],
    #Central America
    ["GDL", "", "Guadalajara", "null", "Mexico", 1, 20.5260, -103.3076, -6],
    ["MEX", "Juárez", "Mexico City", "null", "Mexico", 1, 19.4361, -99.0719, -6],
    ["CUN", "", "Cancún", "null", "Mexico", 1, 21.0417, -86.8740, -5],
    ["PUJ", "", "Punta Cana", "null", "Dominican Republic", 1, 18.5633, -68.3685, -5],
    ["SJU", "Luis Muñoz Marín", "San Juan", "PR", "United States", 1, 18.4373, -66.0041, -5],
    ["PTY", "Tocumen", "Panama City", "null", "Panama", 1, 9.0669, -79.3871, -5],
    #South America
    ["MDE", "José María Córdova", "Medellín", "null", "Colombia", 1, 6.1708, -75.4276, -5],
    ["BOG", "El Dorado", "Bogotá", "null", "Colombia", 1, 4.7010, -74.1461, -5],
    ["LIM", "Jorge Chávez", "Lima", "null", "Peru", 1, -12.0241, -77.1120, -5],
    ["SCL", "Arturo Merino Benítez", "Santiago", "null", "Chile", 1, -33.3898, -70.7944, -4],
    ["BSB", "", "Brasília", "null", "Brazil", 1, -15.8697, -47.9172, -3],
    ["CNF", "Tancredo Neves", "Belo Horizonte", "null", "Brazil", 1, -19.6341, -43.9654, -3],
    ["GIG", "Galeão", "Rio de Janeiro", "null", "Brazil", 1, -22.8053, -43.2566, -3],
    ["GRU", "Guarulhos", "Sāo Paulo", "null", "Brazil", 1, -23.4306, -46.4730, -3],
    ["CGH", "Congonhas", "Sāo Paulo", "null", "Brazil", 1, -23.6273, -46.6566, -3],
    ["AEP", "Jorge Newbery", "Buenos Aires", "null", "Argentina", 1, -34.5580, -58.4170, -3],
    ["EZE", "Ministro Pistarini", "Buenos Aires", "null", "Argentina", 1, -34.8150, -58.5348, -3],
    #Western Europe
    ["DUB", "", "Dublin", "null", "Ireland", 1, 53.4264, -6.2499, 0],
    ["EDI", "", "Edinburgh", "null", "United Kingdom", 1, 55.9508, -3.3615, 0],
    ["BHX", "", "Birmingham", "null", "United Kingdom", 1, 52.4524, -1.7435, 0],
    ["LGW", "Gatwick", "London", "null", "United Kingdom", 1, 51.1537, 0.1821, 0],
    ["LHR", "Heathrow", "London", "null", "United Kingdom", 1, 51.4700, 0.4543, 0],
    ["LIS", "Humberto Delgado", "Lisbon", "null", "Portugal", 1, 38.7756, -9.1354, 0],
    ["MAD", "", "Madrid", "null", "Spain", 1, 40.4983, -3.5676, 1],
    ["BCN", "El Prat", "Barcelona", "null", "Spain", 1, 41.2974, 2.0833, 1],
    ["ORY", "Orly", "Paris", "null", "France", 1, 48.7262, 2.3652, 1],
    ["CDG", "Charles de Gaulle", "Paris", "null", "France", 1, 49.0139, 2.5425, 1],
    ["LYS", "Saint Exupéry", "Lyon", "null", "France", 1, 45.7234, 5.0888, 1],
    ["NCE", "Côte d'Azur", "Nice", "null", "France", 1, 43.6598, 7.2148, 1],
    ["BRU", "", "Brussels", "null", "Belgium", 1, 50.9010, 4.4856, 1],
    ["AMS", "Schiphol", "Amsterdam", "null", "Netherlands", 1, 52.3105, 4.7683, 1],
    ["GVA", "", "Geneva", "null", "Switzerland", 1, 46.2370, 6.1092, 1],
    ["ZRH", "", "Zurich", "null", "Switzerland", 1, 47.4612, 8.5535, 1],
    ["BGY", "Bergamo", "Milan", "null", "Italy", 1, 45.6696, 9.7036, 1],
    ["FCO", "Fiumincino", "Rome", "null", "Italy", 1, 41.7999, 12.2462, 1],
    ["FRA", "am Main", "Frankfurt", "null", "Germany", 1, 50.0379, 8.5622, 1],
    ["STR", "", "Stuttgart", "null", "Germany", 1, 48.6876, 9.2056, 1],
    ["MUC", "", "Munich", "null", "Germany", 1, 48.3537, 11.7751, 1],
    ["TXL", "Tegel", "Berlin", "null", "Germany", 1, 52.5588, 13.2884, 1],
    #Scandinavia
    ["OSL", "Gardermoen", "Oslo", "null", "Norway", 1, 60.1976, 11.1004, 1],
    ["CPH", "", "Copenhagen", "null", "Denmark", 1, 55.6180, 12.6508, 1],
    ["ARN", "Arlanda", "Stockholm", "null", "Sweden", 1, 59.6498, 17.9238, 1],
    ["HEL", "Vantaa", "Helsinki", "null", "Finland", 1, 60.3210, 24.9529, 2],
    #Eastern Europe/Russia
    ["PRG", "Václav Havel", "Prague", "null", "Czech Republic", 1, 50.1018, 14.2632, 1],
    ["VIE", "", "Vienna", "null", "Austria", 1, 48.1126, 16.5755, 1],
    ["BUD", "Ferenc Liszt", "Budapest", "null", "Hungary", 1, 47.4385, 19.2523, 1],
    ["WAW", "", "Warsaw", "null", "Poland", 1, 52.1672, 20.9679, 1],
    ["ATH", "", "Athens", "null", "Greece", 1, 37.9356, 23.9484, 2],
    ["OTP", "Henri Coandă", "Bucharest", "null", "Romania", 1, 44.5707, 26.0844, 2],
    ["KBP", "Boryspil", "Kyiv", "LEN", "Ukraine", 1, 50.3382, 30.8939, 2],
    ["LED", "Pulkovo", "St Petersburg", "LEN", "Russia", 1, 59.8029, 30.2678, 3],
    ["SVO", "Sheremetyevo", "Moscow", "MOS", "Russia", 1, 55.9736, 37.4125, 3],
    ["DME", "Domodedovo", "Moscow", "MOS", "Russia", 1, 55.4103, 37.9025, 3],
    #Africa
    ["CMN", "Mohammed V", "Casablanca", "null", "Morocco", 1, 33.3700, -7.5857, 1],
    ["ALG", "Houari Boumediene", "Algiers", "null", "Algeria", 1, 36.6879, 3.2092, 1],
    ["TUN", "Tunis-Carthage", "Tunis", "null", "Tunisia", 1, 36.8459, 10.2191, 1],
    ["CAI", "", "Cairo", "null", "Egypt", 1, 30.1128, 31.3998, 2],
    ["LOS", "Murtala Muhammed", "Lagos", "null", "Nigeria", 1, 6.5730, 3.3193, 1],
    ["ADD", "Bole", "Addis Ababa", "null", "Ethiopia", 1, 8.9834, 38.7963, 3],
    ["NBO", "Jomo Kenyatta", "Nairobi", "null", "Kenya", 1, -1.3227, 36.9261, 3],
    ["DAR", "Julius Nyerere", "Dar es Salaam", "null", "Tanzania", 1, -6.8725, 39.2069, 3],
    ["JNB", "OR Tambo", "Johannesburg", "null", "South Africa", 1, -26.1367, 28.2411, 2],
    ["CPT", "", "Cape Town", "null", "South Africa", 1, -33.9715, 18.6021, 2],
    #Near/Middle East
    ["IST", "", "Istanbul", "null", "Turkey", 1, 40.9830, 28.8104, 3],
    ["AYT", "", "Antalya", "null", "Turkey", 1, 36.9043, 30.8019, 3],
    ["TLV", "Ben Gurion", "Tel Aviv", "null", "Israel", 1, 32.0055, 34.8854, 2],
    ["JED", "King Abdulaziz", "Jeddah", "null", "Saudi Arabia", 1, 21.6677, 39.1737, 3],
    ["RUH", "King Khalid", "Riyadh", "null", "Saudi Arabia", 1, 24.9636, 46.7007, 3],
    ["DOH", "Hamad", "Doha", "null", "Qatar", 1, 25.2609, 51.6138, 3],
    ["AUH", "", "Abu Dhabi", "null", "United Arab Emirates", 1, 24.4419, 54.6501, 4],
    ["DXB", "", "Dubai", "null", "United Arab Emirates", 1, 25.2532, 55.3657, 4],
    ["IKA", "", "Tehran", "null", "Iran", 1, 35.4095, 51.1552, 3.5],
    #Indian subcontinent
    ["KHI", "Jinnah", "Karachi", "null", "Pakistan", 1, 24.9008, 67.1681, 5],
    ["BOM", "Chhatrapati Shivaji", "Mumbai", "MH", "India", 1, 19.0896, 72.8656, 5.5],
    ["DEL", "Indira Gandhi", "New Delhi", "DL", "India", 1, 28.5562, 77.1000, 5.5],
    ["BLR", "Kempegowda", "Bangalore", "KA", "India", 1, 13.1986, 77.7066, 5.5],
    ["MAA", "", "Chennai", "TN", "India", 1, 12.9941, 80.1709, 5.5],
    ["CMB", "Bandaranaike", "Colombo", "null", "Sri Lanka", 1, 7.1802, 79.8843, 5.5],
    #East Asia
    ["KMG", "Changshui", "Kunming", "YN", "China", 1, 25.0966, 102.9286, 8],
    ["CTU", "Shuangliu", "Chengdu", "SC", "China", 1, 30.5675, 103.9493, 8],
    ["CKG", "Jiangbei", "Chongqing", "CQ", "China", 1, 29.7192, 106.6417, 8],
    ["CAN", "Baiyun", "Guangzhou", "GD", "China", 1, 23.3959, 113.3080, 8],
    ["SZX", "Bao'an", "Shenzhen", "GD", "China", 1, 22.6368, 113.8146, 8],
    ["WUH", "Tianhe", "Wuhan", "HB", "China", 1, 30.7766, 114.2124, 8],
    ["PEK", "Capital", "Beijing", "BJ", "China", 1, 40.0799, 116.6031, 8],
    ["TSN", "Binhai", "Tianjin", "TJ", "China", 1, 39.1304, 117.3592, 8],
    ["XMN", "Gaoqi", "Xiamen", "FJ", "China", 1, 24.5391, 118.1344, 8],
    ["NKG", "Lukou", "Nanjing", "JS", "China", 1, 31.7336, 118.8715, 8],
    ["HGH", "Xiaoshan", "Hangzhou", "ZJ", "China", 1, 30.2359, 120.4389, 8],
    ["SHA", "Hongqiao", "Shanghai", "SH", "China", 1, 31.1922, 121.3343, 8],
    ["PVG", "Pudong", "Shanghai", "SH", "China", 1, 31.1443, 121.8083, 8],
    ["HKG", "", "Hong Kong", "null", "Hong Kong SAR", 1, 22.3080, 113.9185, 8],
    ["TPE", "Taoyuan", "Taipei", "null", "Taiwan", 1, 25.0797, 121.2342, 8],
    ["ICN", "Incheon", "Seoul", "null", "South Korea", 1, 37.4602, 126.4407, 9],
    ["NRT", "Narita", "Tokyo", "null", "Japan", 1, 35.7720, 140.3929, 9],
    #SE Asia
    ["BKK", "Suvarnabhumi", "Bangkok", "null", "Thailand", 1, 13.6900, 100.7501, 7],
    ["SIN", "Changi", "Singapore", "null", "Singapore", 1, 1.3644, 103.9915, 8],
]

#top 20 or so: tier 3, 21-50: tier 2
#if not in this dict, tier is 1. first number is domestic, second is international.
#The tier number gets multiplied into the base odds, plus an extra 2x multiplier if both airports
#are in the same country


airport_tiers = {
    "SFO": [2,2],
    "SEA": [2,1],
    "LAX": [3,3],
    "LAS": [2,1],
    "PHX": [2,1],
    "DFW": [3,2],
    "IAH": [2,1],
    "MSP": [2,1],
    "ORD": [3,2],
    "ATL": [3,2],
    "MCO": [2,1],
    "CLT": [2,1],
    "MIA": [2,2],
    "EWR": [2,1],
    "JFK": [3,3],
    "YYZ": [2,3],
    "MEX": [2,1],
    "GRU": [2,1],
    "DUB": [1,2],
    "LGW": [2,3],
    "LHR": [3,3],
    "MAD": [2,3],
    "BCN": [2,3],
    "CDG": [3,3],
    "BRU": [1,2],
    "AMS": [3,3],
    "ZRH": [1,3],
    "FCO": [2,3],
    "FRA": [3,3],
    "MUC": [2,3],
    "CPH": [1,2],
    "VIE": [1,2],
    "SVO": [2,2],
    "IST": [2,3],
    "AYT": [1,2],
    "DOH": [1,3],
    "AUH": [1,2],
    "DXB": [3,3],
    "BOM": [2,1],
    "DEL": [3,1],
    "KMG": [2,1],
    "CTU": [2,1],
    "CAN": [3,1],
    "SZX": [2,1],
    "PEK": [3,1],
    "SHA": [2,1],
    "PVG": [3,2],
    "HKG": [3,3],
    "TPE": [2,3],
    "ICN": [3,3],
    "NRT": [2,3],
    "BKK": [3,3],
    "SIN": [3,3]
}
#Generating flights:
#Each airport gets a certain number of "turns".
#for fairness, each airport takes one turn, then the next airport takes its turn, etc.
#At the end, there will be more flights allotted than we have flights available -
#we want to end up with 3800 flights or so, but to ensure we get this many, we'll have to over-allocate flights.
#Then to trim down to 3800, we sort the list of flights in ascending order based on the sum of the departing and arriving airports' traffic weights.
#The higher-weighted airports will very likely have more flights to remove. To compensate, we start from the bottom of the list (lower-weighted airports) and roll a dice to determine whether to remove the flight. The lower the weights, the higher the chances of removal AND the higher chance they'll get rolled on at all (we might finish trimming down to 3800 before we get to the end of the list)

if __name__=='__main__':
    total_weights = {}
    for fromcode,v in airports_weights.items():
        if len(v[2]) != 0:
            for tocode,wt in v[2].items():
                if fromcode not in total_weights:
                    total_weights[fromcode] = wt
                else:
                    total_weights[fromcode] += wt
                if tocode not in total_weights:
                    total_weights[tocode] = wt
                else:
                    total_weights[tocode] += wt
    sorted_airports2 = sorted(total_weights.items(), key=lambda x: x[1], reverse=True)
    for a in sorted_airports2:
    	print(a[0], a[1])

    import random

    total = 0
    flights = []
    while total < 3800:
        for k,v in airports_weights.items():
            if len(v[2]) != 0:
                for code,wt in v[2].items():
                    if random.randint(0, 9999) < wt:
                        flights.append([k, code])
                        total += 1


    #sample_flight = [FROM, TO]
    flights_by_airport = {} #{"LAX":10,"SIN":12,...}
    for f in flights:
        if f[0] not in flights_by_airport:
            flights_by_airport[f[0]] = 1
        else:
            flights_by_airport[f[0]] += 1
        if f[1] not in flights_by_airport:
            flights_by_airport[f[1]] = 1
        else:
            flights_by_airport[f[1]] += 1

    print("Total:", total)
    #prints out all airports sorted by number of flights in descending order
    sorted_airports = sorted(flights_by_airport.items(), key=lambda x: x[1], reverse=True)
    for a in sorted_airports:
    	print(a[0], a[1])

airports_raw = [
    ["HNL"],
    ["SFO"],
    ["SEA"],
    ["LAX"],
    ["LAS"],
    ["PHX"],
    ["DFW"],
    ["IAH"],
    ["MSP"],
    ["ORD"],
    ["ATL"],
    ["DTW"],
    ["MCO"],
    ["CLT"],
    ["MIA"],
    ["FLL"],
    ["BWI"],
    ["PHL"],
    ["EWR"],
    ["LGA"],
    ["JFK"],
    ["BOS"],
    ["YVR"],
    ["YYC"],
    ["YYZ"],
    ["YUL"],
    ["GDL"],
    ["MEX"],
    ["CUN"],
    ["PUJ"],
    ["SJU"],
    ["PTY"],
    ["MDE"],
    ["BOG"],
    ["LIM"],
    ["SCL"],
    ["BSB"],
    ["CNF"],
    ["GIG"],
    ["GRU"],
    ["CGH"],
    ["AEP"],
    ["EZE"],
    ["DUB"],
    ["EDI"],
    ["BHX"],
    ["LGW"],
    ["LHR"],
    ["LIS"],
    ["MAD"],
    ["BCN"],
    ["ORY"],
    ["CDG"],
    ["LYS"],
    ["NCE"],
    ["BRU"],
    ["AMS"],
    ["GVA"],
    ["ZRH"],
    ["BGY"],
    ["FCO"],
    ["FRA"],
    ["STR"],
    ["MUC"],
    ["TXL"],
    ["OSL"],
    ["CPH"],
    ["ARN"],
    ["HEL"],
    ["PRG"],
    ["VIE"],
    ["BUD"],
    ["WAW"],
    ["ATH"],
    ["OTP"],
    ["KBP"],
    ["LED"],
    ["SVO"],
    ["DME"],
    ["CMN"],
    ["ALG"],
    ["TUN"],
    ["CAI"],
    ["LOS"],
    ["ADD"],
    ["NBO"],
    ["DAR"],
    ["JNB"],
    ["CPT"],
    ["IST"],
    ["AYT"],
    ["TLV"],
    ["JED"],
    ["RUH"],
    ["DOH"],
    ["AUH"],
    ["DXB"],
    ["IKA"],
    ["KHI"],
    ["BOM"],
    ["DEL"],
    ["BLR"],
    ["MAA"],
    ["CMB"],
    ["KMG"],
    ["CTU"],
    ["CKG"],
    ["CAN"],
    ["SZX"],
    ["WUH"],
    ["PEK"],
    ["TSN"],
    ["XMN"],
    ["NKG"],
    ["HGH"],
    ["SHA"],
    ["PVG"],
    ["HKG"],
    ["TPE"],
    ["ICN"],
    ["NRT"],
    ["BKK"],
    ["SIN"],
]
