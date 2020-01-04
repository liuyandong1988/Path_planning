package org.vrprep.translator.impl;

import java.nio.file.Path;

import org.vrprep.model.instance.Instance;

public interface InstanceTranslator {
	
	public Instance getInstance(Path filePath);

}