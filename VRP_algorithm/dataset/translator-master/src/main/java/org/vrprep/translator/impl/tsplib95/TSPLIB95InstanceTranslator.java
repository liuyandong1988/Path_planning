package org.vrprep.translator.impl.tsplib95;

import java.math.BigInteger;
import java.nio.file.Path;
import java.util.List;

import static org.vrprep.translator.impl.tsplib95.TSPLIB95Keyword.*;

import org.vrprep.model.instance.Instance;
import org.vrprep.model.instance.Instance.Fleet;
import org.vrprep.model.instance.Instance.Info;
import org.vrprep.model.instance.Instance.Network;
import org.vrprep.model.instance.Instance.Requests;
import org.vrprep.model.instance.Instance.Fleet.VehicleProfile;
import org.vrprep.model.instance.ObjectFactory;
import org.vrprep.translator.impl.GlobalConverter;
import org.vrprep.translator.impl.InstanceTranslator;
import org.vrprep.translator.impl.ValueFetcher;
import org.vrprep.translator.util.io.FileLiner;

public class TSPLIB95InstanceTranslator implements InstanceTranslator {

	@Override
	public Instance getInstance(Path path){
		FileLiner liner = new FileLiner(path);
		ValueFetcher fetcher = new TSPLIB95ValueFetcher();
		GlobalConverter converter = new GlobalConverter();

		fetcher.initialize(liner.getLines());
		converter.convert(fetcher);

		ObjectFactory objectFactory = new ObjectFactory();
		Instance instance = objectFactory.createInstance();

		Info info = objectFactory.createInstanceInfo();
		String filename = (String) path.getFileName().toString();
		String instancename = filename.substring(0, filename.lastIndexOf("."));
		info.setName(instancename);
		info.setDataset((String) path.getParent().getFileName().toString());
		instance.setInfo(info);

		@SuppressWarnings("unchecked")
		List<Integer> depots = (List<Integer>) converter.get(DEPOT_SECTION);
		Fleet fleet = objectFactory.createInstanceFleet();
		//int vehicles = (Integer) converter.get(VEHICLES);
		double capacity = (Double) converter.get(CAPACITY);
		VehicleProfile profile = objectFactory.createInstanceFleetVehicleProfile();
		profile.setCapacity(capacity);
		for(int depot : depots) {
			profile.getDepartureNode().add(BigInteger.valueOf(depot));
			profile.getArrivalNode().add(BigInteger.valueOf(depot));
		}
		profile.setType(BigInteger.valueOf(0));

		String type = (String) converter.get(TYPE);
		if(type.equals("DCVRP")){
			double maxLength = (Double) converter.get(DISTANCE);
			profile.setMaxTravelDistance(maxLength);
			double servTime = (Double) converter.get(SERVICE_TIME);
			profile.setMaxTravelTime(servTime);
		}

		fleet.getVehicleProfile().add(profile);
		instance.setFleet(fleet);

		String edgeWeightType = (String) converter.get(EDGE_WEIGHT_TYPE);
		if(edgeWeightType.equals("EXPLICIT")){
			instance.setNetwork((Network) converter.get(EDGE_WEIGHT_SECTION));
		} else {
			instance.setNetwork((Network) converter.get(NODE_COORD_SECTION));
		}

		instance.setRequests((Requests) converter.get(DEMAND_SECTION));

		return instance;
	}

}
