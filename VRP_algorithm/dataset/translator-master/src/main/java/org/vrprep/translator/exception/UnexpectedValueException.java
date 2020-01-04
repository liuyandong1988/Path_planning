package org.vrprep.translator.exception;

import org.vrprep.translator.impl.Keyword;

public class UnexpectedValueException extends ConverterException {

	/**
	 * 
	 */
	private static final long serialVersionUID = -6451192254701908788L;

	public UnexpectedValueException(Keyword keyword, String value) {
		super("Value " + value + " for keyword " + keyword.displayName() + " is not expected.");
	}

}
