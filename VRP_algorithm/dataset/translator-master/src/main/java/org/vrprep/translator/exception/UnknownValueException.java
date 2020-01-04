package org.vrprep.translator.exception;

import org.vrprep.translator.impl.Keyword;

public class UnknownValueException extends ConverterException {

	/**
	 * 
	 */
	private static final long serialVersionUID = 2915522482499259101L;

	public UnknownValueException(Keyword keyword, String value) {
		super("Value " + value + " for keyword " + keyword.displayName() + " is not known.");
	}

}
