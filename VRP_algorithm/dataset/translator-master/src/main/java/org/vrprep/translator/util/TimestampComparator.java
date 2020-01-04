package org.vrprep.translator.util;

import java.util.Comparator;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class TimestampComparator implements Comparator<String> {

	@Override
	public int compare(String o1, String o2) {
		String regex = "^(?<hour>[0-9]{1,2}):(?<minute>[0-9]{2})$";
		Pattern pattern = Pattern.compile(regex);
		Matcher matcher1 = pattern.matcher(o1);
		Matcher matcher2 = pattern.matcher(o2);

		if(!matcher1.find() || !matcher2.find()){
			return o1.compareTo(o2);
		}
		
		int hour1 = Integer.valueOf(matcher1.group("hour"));
		int minute1 = Integer.valueOf(matcher1.group("minute"));
		int hour2 = Integer.valueOf(matcher2.group("hour"));
		int minute2 = Integer.valueOf(matcher2.group("minute"));
		
		if(hour1 != hour2) {
			return (hour1 - hour2)*60 + (minute1 - minute2);
		} else {
			return minute1 - minute2;
		}
	}

}
