package org.vrprep.translator.test;

import java.util.Map;

import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.vrprep.translator.converter.Converter;
import org.vrprep.translator.exception.ConverterException;
import org.vrprep.translator.impl.Keyword;

@RunWith(Parameterized.class)
public abstract class ConverterTest<R> {

	protected String input;
	protected Map<Keyword, Object> anteriorValues;
	protected Converter<R> converter;
	protected R result;

	public ConverterTest(String input, Map<Keyword, Object> options) throws ConverterException {
		this.input = input;
		this.anteriorValues = options;
	}

}
