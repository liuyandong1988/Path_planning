package org.vrprep.translator.util;

import java.util.HashMap;
import java.util.Map;
import java.util.SortedSet;
import java.util.TreeSet;

/**
 * From some timestamps (09:30 for instance), this class is able to create an horizon.
 * 
 * @author hubertlobit
 *
 */
public class Horizon {

	private SortedSet<String> timestamps;

	private Map<String, Integer> map;

	public Horizon() {
		this.timestamps = new TreeSet<String>(new TimestampComparator());
		this.map = new HashMap<String, Integer>();
	}

	public boolean add(String timestamp) {
		map.clear();
		return timestamps.add(timestamp);
	}

	public int getValue(String timestamp){
		if(map.isEmpty()) {
			build();
		}
		return map.get(timestamp);
	}

	private void build() {
		TimestampComparator comparator = new TimestampComparator();
		String previousTimestamp = null;
		for (String timestamp : timestamps) {
			if(previousTimestamp != null) {
				int lastTimelineElement = map.get(previousTimestamp);
				int difference = comparator.compare(previousTimestamp, timestamp);
				map.put(timestamp, lastTimelineElement - difference);
			} else {
				map.put(timestamp, 0);
			}
			previousTimestamp = timestamp;
		}

		int gcd = Arithmetics.gcd(map.values());
		for(String timestamp : timestamps) {
			map.put(timestamp, map.get(timestamp)/gcd);
		}
	}

	@Override
	public String toString() {
		if(map.isEmpty()) {
			build();
		}
		return map.toString();
	}

}
