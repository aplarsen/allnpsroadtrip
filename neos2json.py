import json
#converts NEOS output to a JSON file for Google Maps processing and drawing

parks_raw = open("parks_raw.txt");
neos_output = open("neos_output_mikah.txt");
optimal_route = open("optimal_route.json", "w");

parks = [];
route = [];

for line in parks_raw:
    data = line.split("\t");    
    
    parks.append({"n": data[2].strip(), "l": data[0] + "," + data[1]});

for line in neos_output:
    data = line.split(" ");
    
    if len(data) > 2:
        route.append( parks[int(data[0])] );

json.dump(route, optimal_route, indent=4);

optimal_route.close();