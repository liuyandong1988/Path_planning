package org.vrprep.translator.util.path;

import java.nio.file.Path;
import java.util.List;

public class RegexPathSelector implements PathSelector {
	
	private List<String> regexes;

	public RegexPathSelector(List<String> regexes){
		this.regexes = regexes;
	}

	@Override
	public boolean isSelected(Path path) {
		for(String regex : regexes) {
			if(path.toString().matches(regex)) {
				return true;
			};
		}
		return false;
	}

}
