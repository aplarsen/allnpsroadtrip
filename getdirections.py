import json
import googlemaps

#instantiate Google Maps object
with open('apikey.txt', 'r') as apikeyfile:
	apikey=apikeyfile.read();	
mymaps = googlemaps.Client(apikey);

#open optimized route from NEOS
with open('optimal_route.json') as data_file:    
    optimal_route = json.load(data_file);

#set number of units per route segment
segmentsize = 50;

#initialize file segment counter
filecounter = 0;

#create first segment file
s = open("segment0.txt", "w")

#create file for all segments
a = open("segmentall.txt", "w")

#initialize metadata
metadata = [];

for i in range(0, len(optimal_route)-1):
    #check if first item in segment    
    if (i%segmentsize) == 0:
       
        #write new metadata        
        metadatum = {};
        metadatum['start'] = {"i": i+1, "n": optimal_route[i]['n']}
        metadatum['file'] = "code/raw/segment" + str(filecounter) + ".txt";
    
    #get routes from Google
    routes = mymaps.directions(optimal_route[i]['l'], optimal_route[i+1]['l']);    

    #iterate through legs
    for leg in routes[0]['legs']:
        
        #iterate through steps
        for step in leg['steps']:
            #write encoded polyline to segment and to all file
            s.write(step['polyline']['points'] + "\n")
            a.write(step['polyline']['points'] + "\n")            
    
    #check if last item in segment
    if ((i+1)%segmentsize) == 0:
        #append metadata        
        metadatum['end'] = {"i": i+1, "n": optimal_route[i+1]['n'] };
        metadata.append(metadatum);        
        
        #close segment
        s.close();
        filecounter+=1;        
        
        #open new segment file
        s = open("segment" + str(filecounter) + ".txt", "w");

#close last segment file
s.close();

#append last metadata
metadatum['end'] = {"i": len(optimal_route), "n": optimal_route[ len(optimal_route) -1 ]['n'] };
metadata.append(metadatum);

m = open("metadata.json", "w");
json.dump(metadata, m, indent=4);
m.close();

#close all file    
a.close();