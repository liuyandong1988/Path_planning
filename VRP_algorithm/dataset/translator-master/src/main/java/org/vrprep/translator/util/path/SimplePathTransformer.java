package org.vrprep.translator.util.path;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;

public class SimplePathTransformer implements PathTransformer {
	
	private Map<String, String> replacements;
	
	public SimplePathTransformer() {
		this.replacements = new HashMap<String, String>();
	}
	
	public void addReplacement(String source, String target) {
		this.replacements.put(source, target);
	}

	@Override
	public Path get(Path path) {
		String modifiedPath = path.toString();
		for(Entry<String, String> entry : replacements.entrySet()){
			modifiedPath = modifiedPath.replace(entry.getKey(), entry.getValue());
		}
		return Paths.get(modifiedPath);
	}

}
