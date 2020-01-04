package org.vrprep.translator.test.tsplib95;

import static org.junit.Assert.*;
import static org.vrprep.translator.impl.tsplib95.TSPLIB95Keyword.*;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;

import org.vrprep.model.instance.Instance.Network;
import org.vrprep.translator.converter.tsplib95.EdgeWeightConverter;
import org.vrprep.translator.exception.ConverterException;
import org.vrprep.translator.impl.Keyword;
import org.vrprep.translator.test.ConverterTest;
import org.junit.Test;
import org.junit.runners.Parameterized;

public class EdgeWeightConverterTest extends ConverterTest<Network> {

	private int numberOfNodes;
	private int numberOfLinks;

	public EdgeWeightConverterTest(String input, Map<Keyword, Object> anteriorValues, int numberOfNodes, int numberOfLinks)
			throws ConverterException {
		super(input, anteriorValues);
		this.converter = new EdgeWeightConverter();
		this.result = converter.getOutput(input, anteriorValues);
		this.numberOfNodes = numberOfNodes;
		this.numberOfLinks = numberOfLinks;
	}

	@Parameterized.Parameters
	public static Collection<?> data() {

		String input1 = String.join("\n", new String[]{
				"10    20    25    25    20    10",
				"12    20    25    30    20",
				"10    11    22    30",
				"2     11    25",
				"10    20",
				"12"
		});

		HashMap<Keyword, Object> options1 = new HashMap<Keyword, Object>();
		options1.put(DIMENSION, 7);
		options1.put(EDGE_WEIGHT_TYPE, "EXPLICIT");
		options1.put(EDGE_WEIGHT_FORMAT, "LOWER_COL");
		options1.put(DEPOT_SECTION, new ArrayList<Integer>(Arrays.asList(new Integer[]{1})));

		String input2 = String.join("\n", new String[]{
				"241",
				"276 212",
				"172  92 155",
				"233 161 353 200",
				"111 260 202 170 313",
				"160 281 404 261 170 271",
				"70 312 327 240 292 134 180",
				"202 380 280 288 427 120 355 180",
				"98 330 372 269 281 186 144  53 230",
				"220 462 458 390 424 256 276 150 226 143"
		});

		HashMap<Keyword, Object> options2 = new HashMap<Keyword, Object>();
		options2.put(DIMENSION, 11);
		options2.put(EDGE_WEIGHT_TYPE, "EXPLICIT");
		options2.put(EDGE_WEIGHT_FORMAT, "LOWER_ROW");
		options2.put(DEPOT_SECTION, new ArrayList<Integer>(Arrays.asList(new Integer[]{1})));

		return Arrays.asList(new Object[][] {
				{input1, options1, 7, (6*7)/2},
				{input2, options2, 11, (10*11)/2}
		});

	}

	@Test
	public void testNumberOfElements() {
		assertEquals(result.getNodes().getNode().size(), numberOfNodes);
		assertEquals(result.getLinks().getLink().size(), numberOfLinks);
	}

}
