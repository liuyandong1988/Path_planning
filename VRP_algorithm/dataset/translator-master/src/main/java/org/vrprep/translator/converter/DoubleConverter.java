package org.vrprep.translator.converter;


import java.util.Map;

import org.vrprep.translator.impl.Keyword;

public class DoubleConverter implements Converter<Double> {

	@Override
	public Double getOutput(String input, Map<Keyword, Object> anteriorValues) {
		return Double.valueOf(input);
	}

}
