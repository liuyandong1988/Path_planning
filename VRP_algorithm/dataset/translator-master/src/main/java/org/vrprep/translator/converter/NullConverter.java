package org.vrprep.translator.converter;


import java.util.Map;

import org.vrprep.translator.impl.Keyword;

public class NullConverter implements Converter<String> {

	@Override
	public String getOutput(String input, Map<Keyword, Object> anteriorValues) {
		return input;
	}

}
