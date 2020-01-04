package org.vrprep.translator.converter.tsplib95;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Map;

import static org.vrprep.translator.impl.tsplib95.TSPLIB95Keyword.*;

import org.vrprep.model.instance.ObjectFactory;
import org.vrprep.model.instance.Instance.Network;
import org.vrprep.model.instance.Instance.Network.Links;
import org.vrprep.model.instance.Instance.Network.Nodes;
import org.vrprep.model.instance.Instance.Network.Links.Link;
import org.vrprep.model.instance.Instance.Network.Nodes.Node;
import org.vrprep.translator.converter.Converter;
import org.vrprep.translator.exception.ConverterException;
import org.vrprep.translator.exception.UnexpectedValueException;
import org.vrprep.translator.exception.UnknownValueException;
import org.vrprep.translator.impl.Keyword;

public class EdgeWeightConverter implements Converter<Network> {

	@Override
	public Network getOutput(String input, Map<Keyword, Object> anteriorValues)
			throws ConverterException {

		ObjectFactory objectFactory = new ObjectFactory();
		Network network = objectFactory.createInstanceNetwork();
		Nodes nodes = objectFactory.createInstanceNetworkNodes();

		@SuppressWarnings("unchecked")
		ArrayList<Integer> depots = (ArrayList<Integer>) anteriorValues.get(DEPOT_SECTION);
		int dimension = (Integer) anteriorValues.get(DIMENSION);
		String edgeWeightType = (String) anteriorValues.get(EDGE_WEIGHT_TYPE);
		String edgeWeightFormat = (String) anteriorValues.get(EDGE_WEIGHT_FORMAT);

		List<String> tokens = new ArrayList<String>(Arrays.asList(input.split("\\s+")));
		switch (edgeWeightType) {
		case "EXPLICIT":
			for(int i = 1 ; i <= dimension ; i++){
				Node node = objectFactory.createInstanceNetworkNodesNode();
				node.setId(BigInteger.valueOf(i));
				int isClient = depots.contains(i) ? 0 : 1;
				node.setType(BigInteger.valueOf(isClient));
				nodes.getNode().add(node);
			}

			Links links = objectFactory.createInstanceNetworkLinks();
			if(!edgeWeightFormat.equals("FULL_MATRIX")){
				links.setSymmetric(true);
			}
			switch (edgeWeightFormat) {
			case "FUNCTION":
				throw new UnexpectedValueException(EDGE_WEIGHT_FORMAT, edgeWeightFormat);
			case "FULL_MATRIX":
				/**
				 * 0     (1,2) (1,3) (1,4) (1,5)
				 * (2,1) 0     (2,3) (2,4) (2,5)
				 * (3,1) (3,2) 0     (3,4) (3,5)
				 * (4,1) (4,2) (4,3) 0     (4,5)
				 * (5,1) (5,2) (5,3) (5,4) 0    
				 */
				for(int i = 1 ; i <= dimension ; i++){
					for(int j = 1 ; j <= dimension ; j++){
						String value = tokens.remove(0);
						if(i != j){
							links.getLink().add(link(i, j, value));
						}
					}
				}
				break;
			case "UPPER_ROW":
				/**
				 * (1,2) (1,3) (1,4) (1,5)
				 *       (2,3) (2,4) (2,5)
				 *             (3,4) (3,5)
				 *                   (4,5)
				 */
				for (int i = 1 ; i < dimension; i++) {
					for (int j = i + 1 ; j <= dimension ; j++) {
						links.getLink().add(link(i, j, tokens.remove(0)));
					}
				}
				break;
			case "LOWER_ROW":
				links.setSymmetric(true);
				/**
				 * (2,1)
				 * (3,1) (3,2)
				 * (4,1) (4,2) (4,3)
				 * (5,1) (5,2) (5,3) (5,4) 
				 */
				for(int i = 2 ; i <= dimension ; i++){
					for(int j = 1 ; j < i ; j++){
						links.getLink().add(link(i, j, tokens.remove(0)));
					}
				}
				break;
			case "UPPER_DIAG_ROW":
				/**
				 * 0     (1,2) (1,3) (1,4) (1,5)
				 *       0     (2,3) (2,4) (2,5)
				 *             0     (3,4) (3,5)
				 *                   0     (4,5)
				 *                         0    
				 */
				for(int i = 1 ; i <= dimension ; i++){
					for(int j = i ; j <= dimension ; j++){
						String value = tokens.remove(0);
						if(i != j){
							links.getLink().add(link(i, j, value));
						}
					}
				}
				break;
			case "LOWER_DIAG_ROW":
				/**
				 * 0    
				 * (2,1) 0    
				 * (3,1) (3,2) 0    
				 * (4,1) (4,2) (4,3) 0    
				 * (5,1) (5,2) (5,3) (5,4) 0
				 */
				for(int i = 1 ; i <= dimension ; i++){
					for(int j = 1 ; j <= i ; j++){
						String value = tokens.remove(0);
						if(i != j){
							links.getLink().add(link(i, j, value));
						}
					}
				}
				break;
			case "UPPER_COL":
				/**
				 * (1,2)
				 * (1,3) (2,3)
				 * (1,4) (2,4) (3,4)
				 * (1,5) (2,5) (3,5) (4,5)
				 */
				for (int j = 2 ; j <= dimension; j++) {
					for (int i = 1 ; i < j ; i++) {
						links.getLink().add(link(i, j, tokens.remove(0)));
					}
				}
				break;
			case "LOWER_COL":
				/**
				 * (2,1) (3,1) (4,1) (5,1)
				 *       (3,2) (4,2) (5,2)
				 *             (4,3) (5,3)
				 *                   (5,4)
				 */
				for (int j = 1 ; j < dimension ; j++) {
					for (int i = j + 1 ; i <= dimension ; i++) {
						links.getLink().add(link(i, j, tokens.remove(0)));
					}
				}
				break;
			case "UPPER_DIAG_COL":
				/**
				 * 0
				 * (1,2) 0
				 * (1,3) (2,3) 0
				 * (1,4) (2,4) (3,4) 0
				 * (1,5) (2,5) (3,5) (4,5) 0
				 */
				for (int j = 1 ; j <= dimension; j++) {
					for (int i = 1 ; i <= j ; i++) {
						String value = tokens.remove(0);
						if(i != j){
							links.getLink().add(link(i, j, value));
						}
					}
				}
				break;
			case "LOWER_DIAG_COL":
				/**
				 * 0     (2,1) (3,1) (4,1) (5,1)
				 *       0     (3,2) (4,2) (5,2)
				 *             0     (4,3) (5,3)
				 *                   0     (5,4)
				 *                         0
				 */
				for (int j = 1 ; j <= dimension ; j++) {
					for (int i = j ; i <= dimension ; i++) {
						String value = tokens.remove(0);
						if(i != j){
							links.getLink().add(link(i, j, value));
						}
					}
				}
				break;
			default:
				throw new UnknownValueException(EDGE_WEIGHT_FORMAT, edgeWeightFormat);
			}
			network.setLinks(links);
			break;
		case "EUC_2D": case "EUC_3D": case "MAX_2D": case "MAX_3D":
		case "MAN_2D": case "MAN_3D": case "CEIL_2D": case "GEO":
		case "ATT": case "XRAY1": case "XRAY2": case "SPECIAL":
			throw new UnexpectedValueException(EDGE_WEIGHT_TYPE, edgeWeightType);
		default:
			throw new UnknownValueException(EDGE_WEIGHT_TYPE, edgeWeightType);
		}

		network.setNodes(nodes);
		return network;
		
	}

	private Link link(int i, int j, String value) {
		ObjectFactory objectFactory = new ObjectFactory();
		Link link = objectFactory.createInstanceNetworkLinksLink();
		link.setTail(BigInteger.valueOf(i));
		link.setHead(BigInteger.valueOf(j));
		link.setLength(Double.valueOf(value));
		return link;
	}

}
