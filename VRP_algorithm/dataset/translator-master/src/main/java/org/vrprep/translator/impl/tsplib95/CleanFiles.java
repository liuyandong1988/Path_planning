package org.vrprep.translator.impl.tsplib95;

import java.nio.file.Path;

import org.vrprep.translator.impl.ValueFetcher;
import org.vrprep.translator.util.file.ParametrableFileVisitor;
import org.vrprep.translator.util.io.FileLiner;
import org.vrprep.translator.util.path.PathSelector;
import org.vrprep.translator.util.path.PathTransformer;

public class CleanFiles extends ParametrableFileVisitor {
	
	private ValueFetcher fetcher;
	
	public CleanFiles(PathSelector selector, PathTransformer transformer) {
		super(selector, transformer);
		this.fetcher = new TSPLIB95ValueFetcher();
	}

	@Override
	public void doSomething(Path inputPath, Path outputPath) {
		System.out.format("Started cleaning of %s.\n", inputPath);
		FileLiner liner = new FileLiner(inputPath);
		fetcher.initialize(liner.getLines());
		fetcher.write(outputPath);
		System.out.format("%s successfully cleaned.\n", inputPath.getFileName());
		
	}
}
