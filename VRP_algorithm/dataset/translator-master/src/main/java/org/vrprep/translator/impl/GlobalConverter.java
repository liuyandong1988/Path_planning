package org.vrprep.translator.impl;

import java.util.HashMap;
import java.util.Map;

import org.vrprep.translator.exception.ConverterException;

public class GlobalConverter {

	private Map<Keyword, Object> values;

	public GlobalConverter() {
		this.values = new HashMap<Keyword, Object>();
	}

	public void convert(ValueFetcher fetcher) {
		values.clear();
		for(Keyword kw : fetcher.getKeywords()){
			String input = fetcher.getValue(kw);
			try {
				values.put(kw, kw.converter().getOutput(input, values));
			} catch (ConverterException e) {
				System.err.println(e.getMessage());;
			}
		}
	}

	public Object get(Keyword keyword) {
		return values.get(keyword);
	}

}
