# allnpsroadtrip
Inspired by the Optimal U.S. National Parks Centennial Road Trip work of Dr. Randal Olson  , I sought out to expand on his work to include more of the National Park Service Units to line up with our trips and with Mikah Meyer's world record national parks trip. People commonly misunderstand that the National Park Service encompases the 59 sites designated with the National Parks label, but the System actually includes six times that number when National Historic Sites, Battlefields, Monuments and others are counted.

Of course, adding another 300+ points to the Traveling Salesman Problem makes the task considerably more complicated. For one, not all of the sites are accessible by car, at least not in the way that we are traveling. Mikah was gracious enough to begin with my units database and move some points around so that even the island parks are placed at a point where they are accessible by car. This is usually a visitor center or a ferry entry point if the acutal park is in water. Units that are outside the lower 48 were excluded to keep the problem manageable, and because they will likely be visited by plane or boat. Another tweak made to the alphabetical list was to place the Washington Monument at position 0 so the trek would begin there.

One of the best Traveling Salesman Problem solvers out there is an implementation called Concorde. A brilliant mathematician at Arizona State named Hans Mittelmann has made this available on a web server at a project called NEOS, hosted at the University of Wisconsin. The first transformation involved converting the raw file (parks_raw.txt) from Mikah into the format for the NEOS solver. This was a simple Python script (raw2neos.py) with some minor position juggling. After uploading the new input file (neos_input.txt) to NEOS, the output file (neos_output.txt) needed to be converted back to JSON for processing in future Python scripts and JavaScript. The output from NEOS is just a list of indexed legs, so while impressive in its calculation, the output needs quite a bit of manipulation in order to be useful. It should also be noted that the solver at NEOS is incredibly fast. The problem was solved in a mere matter of seconds.

The next parts were the most complicated to code. The NEOS solver processes the points without respect to roads, so the output has no information about how to get to each point. This is where we turn to the Google Maps API. This API is amazing, but it is throttled to keep projects (like this one) to hammer their servers beyond what is appropriate. I ended up securing an API key and authorizing the Directions endpoint. Even with a paid key, the Directions endpoint still limits the number of locations that can be passed in a directions query. Since the order of points was already known (computed by NEOS, modified a bit to move Mikah's finish at the Lincoln Memorial to the end of the list), I decided to compute the turn-by-turn for each pair of points and store each list separately. The Google API returns the directions polyline as a block of encoded data that must either be plotted directly on a map or stored and later decoded for plotting. Fortunately, the Google Maps JavaScript library already includes the decode() method needed to do this. Early attempts at storing and recalling the data for the whole trip ended up bogging down browsers and even crashing tabs, so I decided to segment the trip in blocks of 50 units each. The Python script (getdirections.py) relies on another Google Maps library to send and process these calls. It opens the JSON file (optimal_route.json) with the optimal route information in it, gets the route between each pair of points, and writes the encoded polyline to a file with 50 units in it and a file with all of the units in it. In this example, there are 8 segmented files and one file with all units.

Finally, I wrote a web interface (this HTML page) to display the points and provide an opportunity to jump to a park unit. There is an option to view all of the route legs, but it does bog down a browser and has a lot of overhead once loaded.

There is an obvious caveat to solving the problem in this way, by using an as-the-crow-flies algorithm to solve the Traveling Salesman Problem and a road mapping tool to do the plotting. You may find a possible inefficiency in the solution with a backtrack or criss-cross that doesn't make sense, but this is a concession that needed to be made to keep this problem doable for a hack like me. Ideally, we would run Randy's genetic algorithm over all 375 of the identified park unit locations. I tried it once, and it ran for 14 hours before failing. The goal here was to extend the idea to apply to all the units in the lower 48, and I think we are pretty close. Randy's map is likely more accurate, but we included far more parks in this project.

Enjoy! Be sure to check out the GitHub repo for all of the code. Many thanks to Mikah for helping formulate this idea, Randal Olson for some of the technical writeups that I read, and of course to the team who built that NEOS server and tool.