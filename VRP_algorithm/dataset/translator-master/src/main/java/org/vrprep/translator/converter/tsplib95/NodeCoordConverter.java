package org.vrprep.translator.converter.tsplib95;

import java.math.BigInteger;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import static org.vrprep.translator.impl.tsplib95.TSPLIB95Keyword.*;

import org.vrprep.model.instance.Instance.Network.Euclidean;
import org.vrprep.model.instance.ObjectFactory;
import org.vrprep.model.instance.Instance.Network;
import org.vrprep.model.instance.Instance.Network.Nodes;
import org.vrprep.model.instance.Instance.Network.Nodes.Node;
import org.vrprep.translator.converter.Converter;
import org.vrprep.translator.exception.ConverterException;
import org.vrprep.translator.exception.NotImplementedException;
import org.vrprep.translator.exception.UnexpectedValueException;
import org.vrprep.translator.exception.UnknownValueException;
import org.vrprep.translator.impl.Keyword;

public class NodeCoordConverter implements Converter<Network> {

	@Override
	public Network getOutput(String input, Map<Keyword, Object> anteriorValues)
			throws ConverterException {

		ObjectFactory objectFactory = new ObjectFactory();
		Network network = objectFactory.createInstanceNetwork();
		Nodes nodes = objectFactory.createInstanceNetworkNodes();

		String nodeCoordType = (String) anteriorValues.get(NODE_COORD_TYPE);
		String edgeWeightFormat = (String) anteriorValues.get(EDGE_WEIGHT_FORMAT);
		String edgeWeightType = (String) anteriorValues.get(EDGE_WEIGHT_TYPE);

		if(nodeCoordType.equals("NO_COORDS")) {
			System.err.println("NODE_COORD_SECTION ignored because of NODE_COORD_TYPE set to NO_COORDS.");
		} else {
			String regex;
			Pattern pattern;
			
			if(nodeCoordType.equals("TWOD_COORDS")) {
				regex = "^(?<id>[0-9]*)\\s+(?<x>[0-9.-]*)\\s+(?<y>[0-9.-]*)$";
			} else if(nodeCoordType.equals("THREED_COORDS")) {
				regex = "^(?<id>[0-9]*)\\s+(?<x>[0-9.-]*)\\s+(?<y>[0-9.-]*)$";
			} else {
				throw new UnknownValueException(NODE_COORD_TYPE, nodeCoordType);
			}
			
			pattern = Pattern.compile(regex);
			for(String line : input.split("\n")){
				Matcher matcher = pattern.matcher(line);
				if (matcher.find()) {
					Node node = objectFactory.createInstanceNetworkNodesNode();
					int id = Integer.valueOf(matcher.group("id"));
					node.setId(BigInteger.valueOf(id));
					node.setType(BigInteger.valueOf(1));
					node.setCx(Double.valueOf(matcher.group("x")));
					node.setCy(Double.valueOf(matcher.group("y")));
					if(nodeCoordType.equals("THREED_COORDS")) {
						node.setCz(Double.valueOf(matcher.group("z")));
					}
					nodes.getNode().add(node);
				}
			}
		}

		switch (edgeWeightFormat) {
		case "FUNCTION":
			switch (edgeWeightType) {
			case "EXPLICIT":
				throw new UnexpectedValueException(EDGE_WEIGHT_TYPE, edgeWeightType);
			case "EUC_2D":
				network.setEuclidean(new Euclidean());
				network.setDecimals(0);
				break;
			case "EUC_3D":
				throw new NotImplementedException(EDGE_WEIGHT_TYPE, edgeWeightType);
			case "MAX_2D":
				throw new NotImplementedException(EDGE_WEIGHT_TYPE, edgeWeightType);
			case "MAX_3D":
				throw new NotImplementedException(EDGE_WEIGHT_TYPE, edgeWeightType);
			case "MAN_2D":
				throw new NotImplementedException(EDGE_WEIGHT_TYPE, edgeWeightType);
			case "MAN_3D":
				throw new NotImplementedException(EDGE_WEIGHT_TYPE, edgeWeightType);
			case "CEIL_2D":
				throw new NotImplementedException(EDGE_WEIGHT_TYPE, edgeWeightType);
			case "GEO":
				throw new NotImplementedException(EDGE_WEIGHT_TYPE, edgeWeightType);
			case "ATT":
				throw new NotImplementedException(EDGE_WEIGHT_TYPE, edgeWeightType);
			case "XRAY1":
				throw new NotImplementedException(EDGE_WEIGHT_TYPE, edgeWeightType);
			case "XRAY2":
				throw new NotImplementedException(EDGE_WEIGHT_TYPE, edgeWeightType);
			case "SPECIAL":
				throw new NotImplementedException(EDGE_WEIGHT_TYPE, edgeWeightType);
			default:
				throw new UnknownValueException(EDGE_WEIGHT_TYPE, edgeWeightType);
			}
			break;
		case "FULL_MATRIX": case "UPPER_ROW": case "LOWER_ROW":
		case "UPPER_DIAG_ROW": case "LOWER_DIAG_ROW":
		case "UPPER_COL": case "LOWER_COL":
		case "UPPER_DIAG_COL": case "LOWER_DIAG_COL":
			throw new UnexpectedValueException(EDGE_WEIGHT_FORMAT, edgeWeightFormat);
		default:
			throw new UnknownValueException(EDGE_WEIGHT_FORMAT, edgeWeightFormat);
		}

		network.setNodes(nodes);
		return network;
	}

}
