package org.vrprep.translator.exception;

import org.vrprep.translator.impl.Keyword;

public class NotImplementedException extends ConverterException {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 4707105774750431538L;

	public NotImplementedException(Keyword keyword) {
		super("Converter for keyword " + keyword.displayName() + " is not implemented yet.");
	}

	public NotImplementedException(Keyword keyword, String value) {
		super("Converter for value " + value + " of keyword " + keyword.displayName() + " is not implemented yet.");
	}

}
