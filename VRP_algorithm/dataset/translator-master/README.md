#Instances translator
This projects aims to make it easy to translate VRP instances to the VRP-REP unified format, based on XML.

For the moment, the translator converts most of TSPLIB95 files, using conventions as described in [the official document](http://www.iwr.uni-heidelberg.de/groups/comopt/software/TSPLIB95/DOC.PS), and Solomon-based instances.

##Overview of datasets

###[ATD-LAB datasets](http://vrp.atd-lab.inf.puc-rio.br/index.php/en/instances?view=vrp)

Dataset | Variant | Number of instances | Format | Translated ?
--- | --- | --- | --- | ---
Augerat 1995 — Set A | CVRP | 27 | TSPLIB95 | Yes
Augerat 1995 — Set B | CVRP | 23 | TSPLIB95 | Yes
Augerat 1995 — Set P | CVRP | 24 | TSPLIB95 | Yes
Christofides and Eilon 1969 — Set E | CVRP | 13 | TSPLIB95 | Yes
Christofides et al. 1979 | CVRP | 14 | TSPLIB95 | Yes
Christofides et al. 1979 — Set M | CVRP | 5 | TSPLIB95 | Yes
Fisher 1994 — Set F | CVRP | 3 | TSPLIB95 | Yes
Golden et al. 1998 | CVRP | 20 | TSPLIB95 | Yes
Li et al. 2005 | CVRP | 12 | TSPLIB95 | Yes
Rochat and Taillard 1995 | CVRP | 13 | Own format | No
Uchoa et al. 2013 | CVRP | 100 | TSPLIB95 | Yes

###[PILLAC datasets](https://api.assembla.com/code/victor-pillac/git/nodes/master/Instances)

Dataset | Variant | Number of instances | Format | Translated ?
--- | --- | --- | --- | ---
Augerat 1995 — Set A | CVRP | 27 | TSPLIB95 | Yes
Augerat 1995 — Set B | CVRP | 23 | TSPLIB95 | Yes
Augerat 1995 — Set P | CVRP | 24 | TSPLIB95 | Yes
Christofides and Eilon 1969 — Set E | CVRP | 13 | TSPLIB95 | Yes
Christofides et al. 1979 | CVRP | 14 | Own format | No
Christofides et al. 1979 — Set M | CVRP | 5 | TSPLIB95 | Yes
Golden et al. 1998 | CVRP | 20 | TSPLIB95 | Yes
Rochat and Taillard 1995 | CVRP | 13 | Own format | No
Solomon_100 | CVRPTW | 56 | Own format | Yes
Solomon_25 | CVRPTW | 56 | Own format | Yes
Solomon_50 | CVRPTW | 56 | Own format | Yes
Pillac | DVRP | 42 | Own format | No
Lackner | DVRP | 336 | Own format | No
Lackner_rd | DVRP | 280 | Own format | No
Kovacs | STRSP | ? | Own format | No
TRSP instances | TRSP | Own format | No
Novoa | VRPSD | 160 | Own format | No

###[TSPLIB dataset](http://www.iwr.uni-heidelberg.de/groups/comopt/software/TSPLIB95/vrp/)

Almost every instance is translated, except the ones with special distance calculators.

###[VRPLIB](http://www.or.deis.unibo.it/research_pages/ORinstances/VRPLIB/VRPLIB.html)

Dataset | Variant | Number of instances | Format | Translated ?
--- | --- | --- | --- | ---
Christofides and Eilon 1969 | CVRP | 3 | TSPLIB95 | Yes
Christofides et al. 1979 | CVRP | 5 | TSPLIB95 | Yes
Christofides et al. 1979 (version b) | CVRP | 3 | TSPLIB95 | Yes
Christofides et al. 1981 | CVRP | 7 | TSPLIB95 | Yes
Clarke and Wright 1963 | CVRP | 1 | TSPLIB95 | Yes
Dantzig et al. 1959 | CVRP | 2 | TSPLIB95 | Yes
Fischetti et al. 1994 | CVRP | 8 | TSPLIB95 | Yes
Fisher 1994 | CVRP | 3 | TSPLIB95 | Yes
Gaskell 1967 | CVRP | 4 | TSPLIB95 | Yes
Gillet and Johnson 1976 | CVRP | 1 | TSPLIB95 | Yes
Gillett and Miller 1974 | CVRP | 8 | TSPLIB95 | Yes
Golden et al. 1997 | CVRP | 12 | TSPLIB95 | Yes
Hadjiconstantinou et al. 1995 | CVRP | 3 | TSPLIB95 | Yes
Hayes 1967 | CVRP | 1 | TSPLIB95 | Yes
Noon et al. 1994 | CVRP | 1 | TSPLIB95 | Yes
Rinaldi et al. 1985 | CVRP | 1 | TSPLIB95 | Yes
Rochat and Taillard 1995 | CVRP | 12 | TSPLIB95 | Yes
Russell 1977 | CVRP | 4 | TSPLIB95 | Yes
Taillard 1993 | CVRP | 1 | TSPLIB95 | Yes
--- | --- | --- | --- | ---
Christofides et al. 1979 | DCVRP | 7 | TSPLIB95 | Yes
Christofides et al. 1979 (version b) | DCVRP | 2 | TSPLIB95 | Yes
Gaskell 1967 | DCVRP | 4 | TSPLIB95 | Yes
Golden et al. 1997 | DCVRP | 8 | TSPLIB95 | Yes

###[VRPWEB](http://neo.lcc.uma.es/vrp/vrp-instances/)

Dataset | Variant | Number of instances | Format | Translated ?
--- | --- | --- | --- | ---
Augerat 1995 — Set A | CVRP | 27 | TSPLIB95 | Yes
Augerat 1995 — Set B | CVRP | 23 | TSPLIB95 | Yes
Augerat 1995 — Set P | CVRP | 24 | TSPLIB95 | Yes
Christofides and Eilon 1969 — Set E | CVRP | 16 | TSPLIB95 | Yes
Christofides et al. 1979 | CVRP | 14 | Own format | No
Fisher 1994 | CVRP | 3 | TSPLIB95 | Yes
Golden et al. 1998 | CVRP | 20 | Own format | No
Rinaldi et al. 1985 | CVRP | 1 | TSPLIB95 | Yes
Rochat and Taillard 1995 | CVRP | 12 | Own format | No
Breedam 1994 – Set 15 | CVRPPDTW | 15 | Own format | No
Breedam 1994 – Set G1 | CVRPPDTW | 80 | Own format | No
Breedam 1994 – Set G2 | CVRPPDTW | 80 | Own format | No
Breedam 1994 – Set G3 | CVRPPDTW | 80 | Own format | No
Breedam 1994 — Set P1 | CVRPPDTW | 60 | Own format | No
Breedam 1994 — Set P2 | CVRPPDTW | 60 | Own format | No
Breedam 1994 – Set T1 | CVRPPDTW | 60 | Own format | No
Breedam 1994 – Set T2 | CVRPPDTW | 60 | Own format | No
VRPLIB | CVRPPDTW | 77 | Extension of TSPLIB95 | No
Cordeau et al. 2002a | CVRPTW | 56 | Own format | No
Homberger | CVRPTW | 300 | Own format | Yes
Solomon_100 | CVRPTW | 56 | Own format | Yes
Solomon_25 | CVRPTW | 56 | Own format | Yes
Solomon_50 | CVRPTW | 56 | Own format | Yes
Cordeau et al. 1997 | MDVRP | 33 | Own format | No
Gillet and Johnson 1976 | MDVRP | 1 | TSPLIB95 | Yes
Cordeau et al. 2004 | MDVRPTW | 20 | Own format | No
Cordeau et al. 1998 | PVRP | 42 | Own format | No
Cordeau et al. 2001 | PVRPTW | 20 | Own format | No

###[OTHER SOURCES]
Dataset | Variant | Number of instances | Translated ?
--- | --- | --- | --- | ---
Cristiansen and Lysgaard 2007  | VRPSD | 40 | Yes
Chao 2002 | TTRP | 21 | No
El Fallahi et al. 2008 - Set 1| MC-VRP | 20 | No
El Fallahi et al. 2008 - Set 2| MC-VRP | 20 | No
Lin et al. 2010 | TTRP | 36 | No
Mendoza et al. 2010 | MC-VRPSD | 180 | Yes
Mendoza et al. 2014 | VRPSD-DC | 39 | Yes
Villegas et al. 2010 | STTRPSD | 32 | No


##How to create your own instance translator ?

To be written later…
