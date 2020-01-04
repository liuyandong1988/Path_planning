package org.vrprep.translator.util.file;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import org.vrprep.translator.util.path.PathSelector;
import org.vrprep.translator.util.path.PathTransformer;

import static java.nio.file.StandardCopyOption.*;

public class CopyFiles extends ParametrableFileVisitor {
	
	public CopyFiles(PathSelector selector, PathTransformer modifier) {
		super(selector, modifier);
	}

	@Override
	public void doSomething(Path inputPath, Path outputPath) {
		System.out.format("Started copying of %s.\n", inputPath);
		try {
			Files.copy(inputPath, outputPath, REPLACE_EXISTING);
		} catch (IOException e) {
			e.printStackTrace();
		}
		System.out.format("%s successfully copied to %s.\n", inputPath.getFileName(), outputPath);
	}
	
}
