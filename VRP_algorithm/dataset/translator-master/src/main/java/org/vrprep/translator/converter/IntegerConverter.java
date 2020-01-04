package org.vrprep.translator.converter;


import java.util.Map;

import org.vrprep.translator.impl.Keyword;

public class IntegerConverter implements Converter<Integer> {

	@Override
	public Integer getOutput(String input, Map<Keyword, Object> anteriorValues) {
		return Integer.valueOf(input);
	}

}
