package org.vrprep.translator.util;

import java.util.Collection;

public class Arithmetics {
	
	public static int gcd(int number1, int number2) {
		if(number2 == 0) {
			return number1;
		}
		return gcd(number2, number1 % number2);
	}

	public static int gcd(Collection<Integer> integers) {
		int result = 0;
		for(int number: integers) {
			result = gcd(result, number);
		}
		return result;
	}

}
