package org.vrprep.translator.converter;


import java.util.Map;

import org.vrprep.translator.exception.ConverterException;
import org.vrprep.translator.impl.Keyword;

/**
 * This interface intends to convert a string value read from a text file
 * to an output of type T.
 * @author hubertlobit
 *
 * @param <T> the output type
 */
public interface Converter<T> {

	public T getOutput(String input, Map<Keyword, Object> anteriorValues)  throws ConverterException;
	
}
