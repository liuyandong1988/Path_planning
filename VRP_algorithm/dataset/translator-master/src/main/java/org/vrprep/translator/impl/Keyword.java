package org.vrprep.translator.impl;

import org.vrprep.translator.converter.Converter;

public interface Keyword {
	
	public int priority();
	
	public String displayName();
	
	public Converter<?> converter();

}
