package org.vrprep.translator.impl;

import java.util.Map;

public interface Canonizer {
	
	public void completeData(Map<Keyword, String> map);
	
	public void cleanData(Map<Keyword, String> map);

}
