package org.vrprep.translator.util.path;

import java.nio.file.Path;

public interface PathSelector {

	public boolean isSelected(Path path);
	
}
