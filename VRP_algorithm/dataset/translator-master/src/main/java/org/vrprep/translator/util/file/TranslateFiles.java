package org.vrprep.translator.util.file;

import java.nio.file.Path;

import javax.xml.bind.JAXBException;

import org.vrprep.model.instance.Instance;
import org.vrprep.model.util.Instances;
import org.vrprep.translator.impl.InstanceTranslator;
import org.vrprep.translator.util.path.PathSelector;
import org.vrprep.translator.util.path.PathTransformer;
import org.xml.sax.SAXException;

public class TranslateFiles extends ParametrableFileVisitor {
	
	private InstanceTranslator translator;
	
	public TranslateFiles(InstanceTranslator translator, PathSelector selector, PathTransformer transformer) {
		super(selector, transformer);
		this.translator = translator;
	}

	@Override
	public void doSomething(Path inputPath, Path outputPath) {
		System.out.format("Started translation of %s.\n", inputPath);
		Instance instance = translator.getInstance(inputPath);
		
		try {
			Instances.write(instance, outputPath);
		} catch (SAXException | JAXBException e) {
			e.printStackTrace();
		}
		
		System.out.format("%s successfully translated.\n", inputPath.getFileName());
	}
	
}
