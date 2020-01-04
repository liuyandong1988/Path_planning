package org.vrprep.translator.impl;

import java.io.IOException;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.List;

import org.apache.commons.configuration.ConfigurationException;
import org.apache.commons.configuration.XMLConfiguration;
import org.apache.commons.lang.ArrayUtils;
import org.vrprep.translator.util.file.ParametrableFileVisitor;
import org.vrprep.translator.util.file.TranslateFiles;
import org.vrprep.translator.util.path.PathSelector;
import org.vrprep.translator.util.path.PathTransformer;
import org.vrprep.translator.util.path.RegexPathSelector;
import org.vrprep.translator.util.path.SimplePathTransformer;

public class Executable {

	public static void main(String[] args) {
		for(String configPath : args) {
			XMLConfiguration config = null;
			try {
				config = new XMLConfiguration(configPath);
			} catch(ConfigurationException e) {
				e.printStackTrace();
			}

			if(config != null) {
				preprocess(config);
				translate(config);
			}
		}
	}

	private static void preprocess(XMLConfiguration config) {
		String[] regexes = config.getStringArray("preprocess.selections.selection[@pattern]");
		PathSelector selector = new RegexPathSelector(Arrays.asList(regexes));

		String copySource = config.getString("preprocess[@source]");
		String copyTarget = config.getString("preprocess[@target]");
		SimplePathTransformer transformer = new SimplePathTransformer();
		transformer.addReplacement(copySource, copyTarget);

		List<Object> list = config.getList("preprocess.replacements.replacement[@source]");
		for(int i = 0 ; i < list.size() ; i++) {
			String replacementSource = config.getString(String.format("preprocess.replacements.replacement(%d)[@source]", i));
			String replacementTarget = config.getString(String.format("preprocess.replacements.replacement(%d)[@target]", i));
			transformer.addReplacement(replacementSource, replacementTarget);
		}

		ParametrableFileVisitor visitor = null;
		try {
			Class<?> aClass = Class.forName(config.getString("preprocess.class[@name]"));
			Constructor<?> ctor = aClass.getDeclaredConstructor(PathSelector.class, PathTransformer.class);
			if(aClass.getSuperclass() == ParametrableFileVisitor.class) { 
				visitor = (ParametrableFileVisitor) ctor.newInstance(selector, transformer);
			}
		} catch (ClassNotFoundException | NoSuchMethodException | SecurityException | InstantiationException | IllegalAccessException | IllegalArgumentException | InvocationTargetException e) {
			e.printStackTrace();
		}

		try {
			Files.walkFileTree(Paths.get(copySource), visitor);
		} catch (IOException e1) {
			e1.printStackTrace();
		}
	}

	private static void translate(XMLConfiguration config) {
		String[] regexes = config.getStringArray("translate.selections.selection[@pattern]");
		PathSelector selector = new RegexPathSelector(Arrays.asList(regexes));
		
		String translateSource = config.getString("translate[@source]");
		String translateTarget = config.getString("translate[@target]");
		SimplePathTransformer transformer = new SimplePathTransformer();
		transformer.addReplacement(translateSource, translateTarget);

		List<Object> list = config.getList("translate.replacements.replacement[@source]");
		for(int i = 0 ; i < list.size() ; i++) {
			String replacementSource = config.getString(String.format("translate.replacements.replacement(%d)[@source]", i));
			String replacementTarget = config.getString(String.format("translate.replacements.replacement(%d)[@target]", i));
			transformer.addReplacement(replacementSource, replacementTarget);
		}

		InstanceTranslator translator = null;
		try {
			Class<?> aClass = Class.forName(config.getString("translate.class[@name]"));
			Constructor<?> ctor = aClass.getDeclaredConstructor();
			if(ArrayUtils.contains(aClass.getInterfaces(), InstanceTranslator.class)) { 
				translator = (InstanceTranslator) ctor.newInstance();
			}
		} catch (ClassNotFoundException | NoSuchMethodException | SecurityException | InstantiationException | IllegalAccessException | IllegalArgumentException | InvocationTargetException e) {
			e.printStackTrace();
		}

		if(translator != null){
			TranslateFiles tf = new TranslateFiles(translator, selector, transformer);

			try {
				Files.walkFileTree(Paths.get(translateSource), tf);
			} catch (IOException e1) {
				e1.printStackTrace();
			}
		}
	}

}
