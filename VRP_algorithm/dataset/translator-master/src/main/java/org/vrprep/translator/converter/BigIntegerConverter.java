package org.vrprep.translator.converter;


import java.math.BigInteger;
import java.util.Map;

import org.vrprep.translator.impl.Keyword;

public class BigIntegerConverter implements Converter<BigInteger> {

	@Override
	public BigInteger getOutput(String input, Map<Keyword, Object> anteriorValues) {
		return BigInteger.valueOf((Integer.valueOf(input)));
	}

}
