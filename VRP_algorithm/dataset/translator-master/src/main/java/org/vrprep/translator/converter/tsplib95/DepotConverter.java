package org.vrprep.translator.converter.tsplib95;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.vrprep.model.instance.Instance.Network;
import org.vrprep.model.instance.Instance.Network.Nodes.Node;
import org.vrprep.translator.converter.Converter;
import org.vrprep.translator.impl.Keyword;

import static org.vrprep.translator.impl.tsplib95.TSPLIB95Keyword.*;

public class DepotConverter implements Converter<List<Integer>> {

	@Override
	public List<Integer> getOutput(String input, Map<Keyword, Object> anteriorValues) {
		ArrayList<Integer> list = new ArrayList<Integer>();

		for(String depot : input.split("\n")) {
			list.add(Integer.valueOf(depot));
		}

		if(anteriorValues.containsKey(NODE_COORD_SECTION)) {
			Network network = (Network) anteriorValues.get(NODE_COORD_SECTION);
			for(Node node : network.getNodes().getNode()) {
				if(list.contains(node.getId().intValue())) {
					node.setType(BigInteger.valueOf(0));
				}
			}
		}

		return list;
	}

}
