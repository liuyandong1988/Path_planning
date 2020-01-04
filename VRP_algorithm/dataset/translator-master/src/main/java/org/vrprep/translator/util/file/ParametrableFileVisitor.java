package org.vrprep.translator.util.file;

import static java.nio.file.FileVisitResult.CONTINUE;

import java.io.IOException;
import java.nio.file.FileVisitResult;
import java.nio.file.Path;
import java.nio.file.SimpleFileVisitor;
import java.nio.file.attribute.BasicFileAttributes;

import org.vrprep.translator.util.path.PathSelector;
import org.vrprep.translator.util.path.PathTransformer;

public abstract class ParametrableFileVisitor extends SimpleFileVisitor<Path> {

	protected PathSelector selector;

	protected PathTransformer transformer;

	public ParametrableFileVisitor(PathSelector selector, PathTransformer transformer) {
		super();
		this.selector = selector;
		this.transformer = transformer;
	}
	
	@Override
	public FileVisitResult visitFile(Path path, BasicFileAttributes attr) {
		if (attr.isRegularFile() && selector.isSelected(path)) {
			Path outputPath = transformer.get(path);
			outputPath.getParent().toFile().mkdirs();
			
			doSomething(path, outputPath);
		}
		return CONTINUE;
	}

	@Override
	public FileVisitResult postVisitDirectory(Path dir, IOException exc) {
		return CONTINUE;
	}

	@Override
	public FileVisitResult visitFileFailed(Path file, IOException exc) {
		System.err.println(exc);
		return CONTINUE;
	}
	
	public abstract void doSomething(Path inputPath, Path outputPath);

}
