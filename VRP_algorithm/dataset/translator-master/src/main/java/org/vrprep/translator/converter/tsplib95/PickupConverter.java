package org.vrprep.translator.converter.tsplib95;

import java.util.Map;

import org.vrprep.translator.converter.Converter;
import org.vrprep.translator.exception.NotImplementedException;
import org.vrprep.translator.impl.Keyword;

import static org.vrprep.translator.impl.tsplib95.TSPLIB95Keyword.*;

public class PickupConverter implements Converter<Object> {

	@Override
	public Object getOutput(String input, Map<Keyword, Object> anteriorValues)
			throws NotImplementedException {
		
		throw new NotImplementedException(PICKUP_SECTION);
	}

}
