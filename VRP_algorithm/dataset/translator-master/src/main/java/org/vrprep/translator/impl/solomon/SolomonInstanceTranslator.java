package org.vrprep.translator.impl.solomon;

import java.math.BigInteger;
import java.nio.file.Path;
import java.util.Iterator;

import org.vrprep.model.instance.Instance;
import org.vrprep.model.instance.Instance.Fleet;
import org.vrprep.model.instance.Instance.Network;
import org.vrprep.model.instance.Instance.Network.Euclidean;
import org.vrprep.model.instance.Instance.Network.Nodes;
import org.vrprep.model.instance.Instance.Network.Nodes.Node;
import org.vrprep.model.instance.Instance.Requests;
import org.vrprep.model.instance.Instance.Requests.Request;
import org.vrprep.model.instance.ObjectFactory;
import org.vrprep.model.instance.Instance.Info;
import org.vrprep.model.instance.Instance.Fleet.VehicleProfile;
import org.vrprep.model.instance.Tw;
import org.vrprep.model.instance.TwType.End;
import org.vrprep.model.instance.TwType.Start;
import org.vrprep.translator.impl.InstanceTranslator;
import org.vrprep.translator.util.io.FileLiner;

public class SolomonInstanceTranslator implements InstanceTranslator {

	@Override
	public Instance getInstance(Path path){
		ObjectFactory objectFactory = new ObjectFactory();
		Instance instance = objectFactory.createInstance();

		FileLiner liner = new FileLiner(path);
		Iterator<String> iter = liner.getLines().iterator();
		Info info = objectFactory.createInstanceInfo();
		iter.next();
		String filename = (String) path.getFileName().toString();
		String instancename = filename.substring(0, filename.lastIndexOf("."));
		info.setName(instancename);
		info.setDataset((String) path.getParent().getFileName().toString());
		instance.setInfo(info);

		if(!iter.next().equals("VEHICLE")) { System.err.println("Error"); }
		if(!iter.next().matches("NUMBER\\s+CAPACITY")) { System.err.println("Error"); }

		Fleet fleet = objectFactory.createInstanceFleet();
		VehicleProfile profile = objectFactory.createInstanceFleetVehicleProfile();
		String[] earlyInfo = iter.next().split("\\s+");
		profile.setNumber(Integer.valueOf(earlyInfo[0]));
		profile.setCapacity(Double.valueOf(earlyInfo[1]));
		profile.setType(BigInteger.valueOf(0));
		fleet.getVehicleProfile().add(profile);

		if(!iter.next().equals("CUSTOMER")) { System.err.println("Error"); }
		if(!iter.next().matches("CUST\\s+NO.\\s+XCOORD.\\s+YCOORD.\\s+DEMAND\\s+READY\\s+TIME\\s+DUE\\s+DATE\\s+SERVICE\\s+TIME")) { System.err.println("Error"); }

		Network network = objectFactory.createInstanceNetwork();
		Nodes nodes = objectFactory.createInstanceNetworkNodes();
		Requests requests = objectFactory.createInstanceRequests();
		while(iter.hasNext()) {
			String[] customerInfo = iter.next().split("\\s+");
			BigInteger nodeId = BigInteger.valueOf(Integer.valueOf(customerInfo[0]));
			double cx = Double.valueOf(customerInfo[1]);
			double cy = Double.valueOf(customerInfo[2]);
			double demand = Double.valueOf(customerInfo[3]);
			boolean isDepot = demand == 0;
			BigInteger type = BigInteger.valueOf(isDepot ? 0 : 1);
			int twStart = Integer.valueOf(customerInfo[4]);
			int twEnd = Integer.valueOf(customerInfo[5]);
			double serviceTime = Double.valueOf(customerInfo[6]);

			Node node = objectFactory.createInstanceNetworkNodesNode();
			node.setId(nodeId);
			node.setCx(cx);
			node.setCy(cy);
			if(isDepot) {
				profile.getDepartureNode().add(nodeId);
				profile.getArrivalNode().add(nodeId);
			}
			node.setType(type);
			nodes.getNode().add(node);

			if(demand != 0) {
				Request request = objectFactory.createInstanceRequestsRequest();
				request.setId(BigInteger.valueOf(Integer.valueOf(customerInfo[0])));
				request.setNode(nodeId);
				request.setQuantity(demand);

				Tw tw = objectFactory.createTw();
				Start start = objectFactory.createTwTypeStart();
				start.setValue(twStart);
				End end = objectFactory.createTwTypeEnd();
				end.setValue(twEnd);
				tw.setStart(start);
				tw.setEnd(end);

				request.getTw().add(tw);
				request.setServiceTime(serviceTime);
				requests.getRequest().add(request);
			} else {
				profile.setMaxTravelTime(Double.valueOf(twEnd));
			}
		}

		network.setEuclidean(new Euclidean());
		network.setDecimals(0);
		network.setNodes(nodes);
		instance.setNetwork(network);
		instance.setFleet(fleet);
		instance.setRequests(requests);
		return instance;
	}

}
