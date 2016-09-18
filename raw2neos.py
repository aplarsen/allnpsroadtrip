#open raw list of parks and coords and output list of coords for NEOS solver

r = open("parks_raw.txt");
w = open("neos_input.txt", "w");

lines = [];

for line in r:
        lines.append(line.split("\t"));

r.close();

w.write( str(len(lines)) + "\n");
for line in lines:    
    w.write( str(float(line[0])*1000) + " " + str(float(line[1])*1000) + "\n");

w.close();