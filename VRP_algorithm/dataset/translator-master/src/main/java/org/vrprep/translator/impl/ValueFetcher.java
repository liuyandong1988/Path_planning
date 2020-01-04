package org.vrprep.translator.impl;

import java.nio.file.Path;
import java.util.List;

/**
 * 
 * @author hubertlobit
 *
 */
public interface ValueFetcher {
	
	public void initialize(List<String> lines);
	
	public Keyword[] getKeywords();
	
	public String getValue(Keyword keyword);

	public void write(Path path);
	
}
