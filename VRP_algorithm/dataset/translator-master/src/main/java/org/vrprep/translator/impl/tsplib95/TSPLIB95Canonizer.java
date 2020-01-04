package org.vrprep.translator.impl.tsplib95;

import static org.vrprep.translator.impl.tsplib95.TSPLIB95Keyword.*;

import java.util.Arrays;
import java.util.Map;

import org.vrprep.translator.impl.Canonizer;
import org.vrprep.translator.impl.Keyword;

/**
 * A strategy class that can add/remove implicit data to complete/clean what was read/written in files.
 * 
 * @author hubertlobit
 *
 */
public class TSPLIB95Canonizer implements Canonizer {

	@Override
	public void completeData(Map<Keyword, String> map) {

		/**
		 * If EDGE_WEIGHT_TYPE is not explicit, they are given by a function.
		 * This piece of information has no default value, so it won't be removed in cleanData method.
		 */
		if(map.containsKey(EDGE_WEIGHT_TYPE) && !map.get(EDGE_WEIGHT_TYPE).equals("EXPLICIT")){
			map.put(EDGE_WEIGHT_FORMAT, "FUNCTION");
		}
		
		/**
		 * Default value for NODE_COORD_TYPE as specified in documentation.
		 */
		if(!map.containsKey(NODE_COORD_TYPE)){
			map.put(NODE_COORD_TYPE, "NO_COORDS");
		}

		/**
		 * Default value for DISPLAY_DATA_TYPE as specified in documentation.
		 */
		if(map.containsKey(NODE_COORD_SECTION) && !map.containsKey(DISPLAY_DATA_TYPE)){
			map.put(DISPLAY_DATA_TYPE, "COORD_DISPLAY");
		}

		/**
		 * Removal of unused information.
		 */
		if(map.containsKey(DEPOT_SECTION)) {
			String[] depots = map.get(DEPOT_SECTION).split("\n");
			if(depots[depots.length - 1].startsWith("-1")){
				map.put(DEPOT_SECTION, String.join("\n", Arrays.copyOfRange(depots, 0, depots.length - 1)));
			}
		}

	}

	@Override
	public void cleanData(Map<Keyword, String> map) {

		if(map.get(NODE_COORD_TYPE).equals("NO_COORDS")){
			map.remove(NODE_COORD_TYPE);
		}

		if(map.containsKey(NODE_COORD_SECTION) && map.get(DISPLAY_DATA_TYPE).equals("COORD_DISPLAY")){
			map.remove(DISPLAY_DATA_TYPE);
		}
		
		if(map.containsKey(DEPOT_SECTION)) {
			map.put(DEPOT_SECTION, map.get(DEPOT_SECTION).concat("\n-1"));
		}

	}

}
