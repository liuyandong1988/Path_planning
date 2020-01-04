package org.vrprep.translator.converter.tsplib95;

import java.util.HashMap;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import static org.vrprep.translator.impl.tsplib95.TSPLIB95Keyword.*;

import org.vrprep.model.instance.ObjectFactory;
import org.vrprep.model.instance.Instance.Network;
import org.vrprep.model.instance.Tw;
import org.vrprep.model.instance.TwType.End;
import org.vrprep.model.instance.TwType.Start;
import org.vrprep.translator.converter.Converter;
import org.vrprep.translator.exception.NotImplementedException;
import org.vrprep.translator.impl.Keyword;
import org.vrprep.translator.util.Horizon;

public class TimeWindowConverter implements Converter<Network> {

	@Override
	public Network getOutput(String input, Map<Keyword, Object> anteriorValues) throws NotImplementedException {
		ObjectFactory objectFactory = new ObjectFactory();

		Horizon horizon = new Horizon();
		String regex = "^(?<id>[0-9]*)\\s+(?<start>[0-9:]*)\\s+(?<end>[0-9:]*)$";
		Pattern pattern = Pattern.compile(regex);
		for(String line : input.split("\n")) {
			Matcher matcher = pattern.matcher(line);
			if(matcher.find()){
				horizon.add(matcher.group("start"));
				horizon.add(matcher.group("end"));
			}
		}
		
		@SuppressWarnings("unused")
		Map<String, Map<String, Tw>> timeWindows = new HashMap<String, Map<String, Tw>>();
		
		Tw tw = objectFactory.createTw();

		Start start = objectFactory.createTwTypeStart();
		tw.setStart(start);
		start.setValue(07);

		End end = objectFactory.createTwTypeEnd();
		end.setValue(01);
		tw.setEnd(end);

		throw new NotImplementedException(TIME_WINDOW_SECTION);
	}

}
