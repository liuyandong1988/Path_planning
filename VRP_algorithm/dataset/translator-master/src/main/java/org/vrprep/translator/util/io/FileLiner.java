package org.vrprep.translator.util.io;

import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.ListIterator;

/**
 * This class intends to read any type of text file, converting it
 * to an array containing the lines.
 * 
 * @author hubertlobit
 */
public class FileLiner {
	
	/**
	 * The path of file.
	 */
	private Path path;
	
	/**
	 * The lines of file.
	 */
	private List<String> lines;
	
	public FileLiner(Path path){
		this.path = path;
		this.lines = read();
	}
	
	private List<String> read() {
		Charset charset = Charset.defaultCharset();   
		
		List<String> lines = null;
		try {
			lines = Files.readAllLines(path, charset);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		ListIterator<String> iter = lines.listIterator();
		while(iter.hasNext()){
			String value = iter.next().trim();
			if(value.length() == 0){
				iter.remove();
			} else {
				iter.set(value);
			}
		}
		
		return lines;
	}
	
	public Path getPath() {
		return this.path;
	}
	
	public List<String> getLines() {
		return this.lines;
	}

}
